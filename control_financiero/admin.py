from django.contrib import admin
from .models import MovimientoFinanciero

@admin.register(MovimientoFinanciero)
class MovimientoFinancieroAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'monto', 'fecha', 'descripcion')
    list_filter = ('tipo', 'fecha')
    search_fields = ('descripcion',)