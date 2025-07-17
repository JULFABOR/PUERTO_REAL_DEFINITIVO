from django.urls import path
from . import views

urlpatterns = [
    # Registrar nueva compra
    path('registrar/', views.registrar_compra, name='registrar_compra'),

    # Historial de compras con filtros y paginación
    path('historial/', views.historial_compras, name='historial_compras'),

    # Anular compra con confirmación
    path('anular/<int:compra_id>/', views.anular_compra, name='anular_compra'),

    # Exportar historial a CSV
    path('exportar/csv/', views.exportar_compras_csv, name='exportar_compras_csv'),

    # Exportar historial a PDF
    path('exportar/pdf/', views.exportar_compras_pdf, name='exportar_compras_pdf'),
    
    # Detalle de compra
    path('detalle/<int:compra_id>/', views.detalle_compra, name='detalle_compra'),

    # Exportar detalle de compra a PDF
    path('detalle/<int:compra_id>/pdf/', views.detalle_compra_pdf, name='detalle_compra_pdf'),

]