from django.shortcuts import render
from HOME.models import Proveedores, Productos

def registrar_compra(request):
    if request.method == 'GET':
        proveedores = Proveedores.objects.filter(estado_proveedor=True)
        productos = Productos.objects.filter(activo=True)
        return render(request, 'compras/registrar_compra.html', {
            'proveedores': proveedores,
            'productos': productos
        })

