from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from HOME.models import Proveedores, Estados, Compras  # Ajustá si es necesario
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.utils.timezone import now
from datetime import timedelta
import json
import calendar
import csv
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
@login_required
def registrar_proveedor(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_proveedor')
        razon_social = request.POST.get('razon_social_proveedor')
        telefono = request.POST.get('telefono_proveedor')
        cuit = request.POST.get('cuit_proveedor')
        correo = request.POST.get('correo_proveedor')
        estado_id = request.POST.get('estado_proveedor')

        # Validación básica
        if not all([nombre, razon_social, cuit, estado_id]):
            messages.error(request, "Faltan campos obligatorios.")
            return redirect('registrar_proveedor')

        if Proveedores.objects.filter(cuit_proveedor=cuit, DELETE_Prov=False).exists():
            messages.warning(request, f"Ya existe un proveedor con CUIT {cuit}.")
            return redirect('registrar_proveedor')

        # Crear proveedor
        try:
            estado = Estados.objects.get(id=estado_id)

            Proveedores.objects.create(
                nombre_proveedor=nombre,
                razon_social_proveedor=razon_social,
                telefono_proveedor=telefono,
                cuit_proveedor=cuit,
                correo_proveedor=correo,
                estado_proveedor=estado
            )

            messages.success(request, "Proveedor registrado exitosamente.")
            return redirect('listar_proveedores')  # o donde quieras

        except Estados.DoesNotExist:
            messages.error(request, "Estado seleccionado no válido.")
            return redirect('registrar_proveedor')

    # GET → Mostrar formulario
    estados = Estados.objects.all()
    return render(request, 'proveedores/registrar_proveedor.html', {
        'estados': estados
    })


@login_required
def editar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedores, id_proveedor=proveedor_id, DELETE_Prov=False)

    if request.method == 'POST':
        proveedor.nombre_proveedor = request.POST.get('nombre_proveedor')
        proveedor.razon_social_proveedor = request.POST.get('razon_social_proveedor')
        proveedor.telefono_proveedor = request.POST.get('telefono_proveedor')
        proveedor.cuit_proveedor = request.POST.get('cuit_proveedor')
        proveedor.correo_proveedor = request.POST.get('correo_proveedor')

        estado_id = request.POST.get('estado_proveedor')
        try:
            proveedor.estado_proveedor = Estados.objects.get(id=estado_id)
        except Estados.DoesNotExist:
            messages.error(request, "Estado inválido.")
            return redirect('editar_proveedor', proveedor_id=proveedor.id_proveedor)

        proveedor.save()
        messages.success(request, "Proveedor actualizado correctamente.")
        return redirect('listar_proveedores')

    estados = Estados.objects.all()
    return render(request, 'proveedores/editar_proveedor.html', {
        'proveedor': proveedor,
        'estados': estados
    })


@login_required
def listar_proveedores(request):
    query = request.GET.get('q', '').strip()
    proveedores_qs = Proveedores.objects.filter(DELETE_Prov=False)

    if query:
        proveedores_qs = proveedores_qs.filter(
            Q(nombre_proveedor__icontains=query) |
            Q(cuit_proveedor__icontains=query)
        )

    proveedores_qs = proveedores_qs.order_by('nombre_proveedor')

    paginator = Paginator(proveedores_qs, 10)  # 10 por página
    page = request.GET.get('page')
    proveedores = paginator.get_page(page)

    return render(request, 'proveedores/listar_proveedores.html', {
        'proveedores': proveedores,
        'query': query
    })
@login_required
def eliminar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedores, id_proveedor=proveedor_id, DELETE_Prov=False)
    
    proveedor.DELETE_Prov = True
    proveedor.save()

    messages.success(request, f"Proveedor '{proveedor.nombre_proveedor}' eliminado correctamente.")
    return redirect('listar_proveedores')


@login_required
def exportar_proveedores_csv(request):
    proveedores = Proveedores.objects.filter(DELETE_Prov=False).select_related('estado_proveedor')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="proveedores.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nombre', 'Razón Social', 'CUIT', 'Teléfono', 'Correo', 'Estado'])

    for p in proveedores:
        writer.writerow([
            p.nombre_proveedor,
            p.razon_social_proveedor,
            p.cuit_proveedor,
            p.telefono_proveedor,
            p.correo_proveedor,
            p.estado_proveedor.nombre_estado
        ])
    return response
@login_required
def exportar_proveedores_pdf(request):
    proveedores = Proveedores.objects.filter(DELETE_Prov=False).select_related('estado_proveedor')
    html = render_to_string('proveedores/pdf_proveedores.html', {'proveedores': proveedores})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="proveedores.pdf"'

    pisa.CreatePDF(BytesIO(html.encode('UTF-8')), dest=response)
    return response
@login_required
def compras_por_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedores, id_proveedor=proveedor_id, DELETE_Prov=False)

    compras = Compras.objects.filter(proveedor=proveedor, DELETE=False).order_by('-fecha_compra')

    return render(request, 'proveedores/compras_por_proveedor.html', {
        'proveedor': proveedor,
        'compras': compras
    })
@login_required
def exportar_compras_por_proveedor_csv(request, proveedor_id):
    proveedor = get_object_or_404(Proveedores, id_proveedor=proveedor_id, DELETE_Prov=False)
    compras = Compras.objects.filter(proveedor=proveedor, DELETE=False).order_by('-fecha_compra')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="compras_{proveedor.nombre_proveedor}.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Fecha', 'Total', 'Estado'])

    for compra in compras:
        writer.writerow([
            compra.id,
            compra.fecha_compra.strftime('%d/%m/%Y %H:%M'),
            f"{compra.total_compra:.2f}",
            compra.estado
        ])

    return response
@login_required
def exportar_compras_por_proveedor_pdf(request, proveedor_id):
    proveedor = get_object_or_404(Proveedores, id_proveedor=proveedor_id, DELETE_Prov=False)
    compras = Compras.objects.filter(proveedor=proveedor, DELETE=False).order_by('-fecha_compra')

    html = render_to_string('proveedores/pdf_compras_por_proveedor.html', {
        'proveedor': proveedor,
        'compras': compras
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="compras_{proveedor.nombre_proveedor}.pdf"'

    pisa.CreatePDF(BytesIO(html.encode('UTF-8')), dest=response)
    return response
@login_required
def dashboard_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedores, id_proveedor=proveedor_id, DELETE_Prov=False)
    compras = Compras.objects.filter(proveedor=proveedor, DELETE=False)

    total_gastado = compras.aggregate(Sum('total_compra'))['total_compra__sum'] or 0
    cantidad_compras = compras.count()
    ultima_compra = compras.order_by('-fecha_compra').first()

    # Compras por mes (últimos 6 meses)
    hoy = now().date()
    hace_6_meses = hoy - timedelta(days=180)
    compras_filtradas = compras.filter(fecha_compra__date__gte=hace_6_meses)

    compras_por_mes = {}
    for i in range(6):
        mes = (hoy.replace(day=1) - timedelta(days=30 * i)).replace(day=1)
        key = mes.strftime('%b %Y')
        compras_por_mes[key] = 0

    for c in compras_filtradas:
        key = c.fecha_compra.strftime('%b %Y')
        if key in compras_por_mes:
            compras_por_mes[key] += float(c.total_compra)

    meses = list(reversed(list(compras_por_mes.keys())))
    totales = list(reversed(list(compras_por_mes.values())))

    return render(request, 'proveedores/dashboard_proveedor.html', {
        'proveedor': proveedor,
        'total_gastado': total_gastado,
        'cantidad_compras': cantidad_compras,
        'ultima_compra': ultima_compra,
        'meses': json.dumps(meses),
        'totales': json.dumps(totales),
    })
@login_required
def exportar_dashboard_proveedor_pdf(request, proveedor_id):
    proveedor = get_object_or_404(Proveedores, id_proveedor=proveedor_id, DELETE_Prov=False)
    compras = Compras.objects.filter(proveedor=proveedor, DELETE=False)

    total_gastado = compras.aggregate(Sum('total_compra'))['total_compra__sum'] or 0
    cantidad_compras = compras.count()
    ultima_compra = compras.order_by('-fecha_compra').first()

    hoy = now().date()
    hace_6_meses = hoy - timedelta(days=180)
    compras_filtradas = compras.filter(fecha_compra__date__gte=hace_6_meses)

    compras_por_mes = {}
    for i in range(6):
        mes = (hoy.replace(day=1) - timedelta(days=30 * i)).replace(day=1)
        key = mes.strftime('%b %Y')
        compras_por_mes[key] = 0

    for c in compras_filtradas:
        key = c.fecha_compra.strftime('%b %Y')
        if key in compras_por_mes:
            compras_por_mes[key] += float(c.total_compra)

    meses = list(reversed(list(compras_por_mes.keys())))
    totales = list(reversed(list(compras_por_mes.values())))

    html = render_to_string('proveedores/pdf_dashboard_proveedor.html', {
        'proveedor': proveedor,
        'total_gastado': total_gastado,
        'cantidad_compras': cantidad_compras,
        'ultima_compra': ultima_compra,
        'meses': meses,
        'totales': totales,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="dashboard_{proveedor.nombre_proveedor}.pdf"'
    pisa.CreatePDF(BytesIO(html.encode('UTF-8')), dest=response)
    return response