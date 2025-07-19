from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_proveedor, name='registrar_proveedor'),
    path('editar/<int:proveedor_id>/', views.editar_proveedor, name='editar_proveedor'),
    path('listar/', views.listar_proveedores, name='listar_proveedores'),
    path('eliminar/<int:proveedor_id>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    path('exportar/csv/', views.exportar_proveedores_csv, name='exportar_proveedores_csv'),
    path('exportar/pdf/', views.exportar_proveedores_pdf, name='exportar_proveedores_pdf'),
    path('compras/<int:proveedor_id>/', views.compras_por_proveedor, name='compras_por_proveedor'),
    path('<int:proveedor_id>/compras/exportar/csv/', views.exportar_compras_por_proveedor_csv, name='exportar_compras_por_proveedor_csv'),
    path('<int:proveedor_id>/compras/exportar/pdf/', views.exportar_compras_por_proveedor_pdf, name='exportar_compras_por_proveedor_pdf'),
    path('<int:proveedor_id>/dashboard/', views.dashboard_proveedor, name='dashboard_proveedor'),
    path('<int:proveedor_id>/dashboard/exportar/pdf/', views.exportar_dashboard_proveedor_pdf, name='exportar_dashboard_proveedor_pdf'),
]