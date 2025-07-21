from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_ventas, name='lista_ventas'),
    path('crear/', views.crear_venta, name='crear_venta'),
    path('editar/<int:venta_id>/', views.editar_venta, name='editar_venta'),
    path('borrar/<int:venta_id>/', views.borrar_venta, name='borrar_venta')
]