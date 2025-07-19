from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.dateparse import parse_date
from xhtml2pdf import pisa
from io import BytesIO
import csv

# Modelos
from HOME.models import Compras, Detalle_Compras, Productos, Proveedores

# -----------------------------
# Registrar una nueva compra
# -----------------------------
@login_required
def registrar_compra(request):
    if request.method == 'POST':
        proveedor_id = request.POST.get('proveedor')
        total = request.POST.get('total_compra')

        try:
            proveedor = Proveedores.objects.get(id=proveedor_id)
        except Proveedores.DoesNotExist:
            messages.error(request, 'Proveedor inválido.')
            return redirect('registrar_compra')

        try:
            from django.db import transaction
            with transaction.atomic():
                compra = Compras.objects.create(
                    proveedor=proveedor,
                    total_compra=total,
                    estado='pendiente'
                )

                productos = []
                for key in request.POST:
                    if key.startswith('producto_'):
                        index = key.split('_')[1]
                        nombre_producto = request.POST.get(f'producto_{index}')
                        cantidad = int(request.POST.get(f'cantidad_{index}', 0))
                        precio_unitario = float(request.POST.get(f'precio_{index}', 0))

                        try:
                            producto = Productos.objects.get(nombre=nombre_producto, DELETE=False)
                        except Productos.DoesNotExist:
                            messages.warning(request, f"Producto '{nombre_producto}' no encontrado.")
                            continue

                        subtotal = cantidad * precio_unitario

                        detalle = Detalle_Compras(
                            compra=compra,
                            producto=producto,
                            cantidad=cantidad,
                            precio_unitario=precio_unitario,
                            subtotal=subtotal
                        )
                        productos.append(detalle)

                Detalle_Compras.objects.bulk_create(productos)
                messages.success(request, 'Compra registrada con éxito.')
                return redirect('historial_compras')

        except Exception as e:
            messages.error(request, f'Ocurrió un error al guardar la compra: {e}')
            return redirect('registrar_compra')

    proveedores = Proveedores.objects.filter(DELETE=False)
    return render(request, 'compras/registrar_compra.html', {'proveedores': proveedores})

# -----------------------------
# Vista general con filtros + paginación
# -----------------------------
@login_required
def historial_compras(request):
    compras_list = Compras.objects.filter(DELETE=False).select_related('proveedor')

    # Filtros
    proveedor_id = request.GET.get('proveedor')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    orden = request.GET.get('orden', 'desc')

    if proveedor_id:
        compras_list = compras_list.filter(proveedor_id=proveedor_id)
    if fecha_inicio:
        compras_list = compras_list.filter(fecha_compra__date__gte=parse_date(fecha_inicio))
    if fecha_fin:
        compras_list = compras_list.filter(fecha_compra__date__lte=parse_date(fecha_fin))
    if orden == 'asc':
        compras_list = compras_list.order_by('fecha_compra')
    else:
        compras_list = compras_list.order_by('-fecha_compra')

    # Paginación
    paginator = Paginator(compras_list, 10)
    page = request.GET.get('page')
    try:
        compras = paginator.page(page)
    except PageNotAnInteger:
        compras = paginator.page(1)
    except EmptyPage:
        compras = paginator.page(paginator.num_pages)

    proveedores = Proveedores.objects.filter(DELETE=False)

    return render(request, 'compras/historial_compras.html', {
        'compras': compras,
        'proveedores': proveedores,
        'filtros': {
            'proveedor': proveedor_id,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'orden': orden,
        }
    })

# -----------------------------
# Anular compra con validación
# -----------------------------
@login_required
def anular_compra(request, compra_id):
    compra = get_object_or_404(Compras, id=compra_id, DELETE=False)

    # No permitir anular entregadas o cerradas
    if compra.estado in ['entregada', 'cerrada']:
        messages.error(request, f"No se puede anular una compra con estado '{compra.estado}'.")
        return redirect('historial_compras')

    # Si se puede anular
    if compra.estado != 'anulada':
        compra.estado = 'anulada'
        compra.DELETE = True
        compra.save()
        messages.success(request, f'Compra #{compra.id} anulada correctamente.')
    else:
        messages.warning(request, f'La compra #{compra.id} ya estaba anulada.')

    return redirect('historial_compras')

# -----------------------------
# Exportar historial a CSV
# -----------------------------
@login_required
def exportar_compras_csv(request):
    compras = Compras.objects.filter(DELETE=False).select_related('proveedor').order_by('-fecha_compra')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="historial_compras.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Proveedor', 'Fecha', 'Total', 'Estado'])

    for compra in compras:
        writer.writerow([
            compra.id,
            compra.proveedor.nombre,
            compra.fecha_compra.strftime('%d/%m/%Y %H:%M'),
            f"{compra.total_compra:.2f}",
            compra.estado,
        ])

    return response

# -----------------------------
# Exportar historial a PDF
# -----------------------------
@login_required
def exportar_compras_pdf(request):
    compras = Compras.objects.filter(DELETE=False).select_related('proveedor').order_by('-fecha_compra')

    html = render_to_string('compras/pdf_compras.html', {'compras': compras})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="historial_compras.pdf"'

    pisa.CreatePDF(BytesIO(html.encode('UTF-8')), dest=response)
    return response
@login_required
def detalle_compra(request, compra_id):
    compra = get_object_or_404(Compras, id=compra_id)

    if compra.DELETE:
        messages.warning(request, f'Esta compra fue anulada.')

    detalles = Detalle_Compras.objects.filter(compra=compra).select_related('producto')

    return render(request, 'compras/detalle_compra.html', {
        'compra': compra,
        'detalles': detalles
    })
@login_required
def detalle_compra_pdf(request, compra_id):
    compra = get_object_or_404(Compras, id=compra_id)
    detalles = Detalle_Compras.objects.filter(compra=compra).select_related('producto')

    html = render_to_string('compras/pdf_detalle_compra.html', {
        'compra': compra,
        'detalles': detalles
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="compra_{compra.id}.pdf"'

    pisa.CreatePDF(BytesIO(html.encode('UTF-8')), dest=response)
    return response