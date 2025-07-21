from django.contrib import admin
from HOME.models import Ventas, Detalle_Ventas, Metodos_Pago, Venta_MetodoPago 
# Register your models here.

admin.site.register(Ventas)
admin.site.register(Detalle_Ventas)
admin.site.register(Metodos_Pago)
admin.site.register(Venta_MetodoPago)
