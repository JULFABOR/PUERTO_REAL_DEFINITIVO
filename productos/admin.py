from django.contrib import admin
from .models import Categoria, Producto, MovimientoStock

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(MovimientoStock)