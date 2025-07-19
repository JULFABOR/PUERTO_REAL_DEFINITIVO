from django.contrib import admin
from .models import MovimientoStock

@admin.register(MovimientoStock)
class MovimientoStockAdmin(admin.ModelAdmin):
    list_display = ('producto', 'tipo', 'cantidad', 'fecha', 'motivo')
    list_filter = ('tipo', 'fecha', 'producto')
    search_fields = ('producto__nombre', 'motivo')
