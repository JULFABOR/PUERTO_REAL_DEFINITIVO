from django.shortcuts import render, get_object_or_404 ,redirect 
from .forms import VentaForm
from HOME.models import Ventas
# Create your views here.
def lista_ventas(request):
    ventas = Ventas.objects.all()
    return render(request, 'ventas/ventas_index.html', {'ventas' : ventas})

def crear_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_ventas')
    else:
        form = VentaForm()
    return render(request, 'ventas/ventas_index.html', {'form': form})

def editar_venta(request, venta_id):
    venta = get_object_or_404(Ventas, id_venta=venta_id)
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            return redirect('lista_ventas')
        else:
            form = VentaForm(instance=venta)
    return render(request, 'ventas/venta_index.html', {'form':form})

def borrar_venta(request, venta_id):
    venta = get_object_or_404(Ventas, id_venta= venta_id)
    if request.method == 'POST':
        venta.delete()
        return redirect('lista_ventas')
    return render(request, 'ventas/borrar_ventas.html',{'venta': venta})

