# caja/urls.py
from django.urls import path
from . import views # Importa tus vistas

app_name = 'caja' # Define el nombre de la app para usarlo en las URLs (ej. 'caja:abrir_caja')

urlpatterns = [
    path('abrir/', views.AbrirCajaView.as_view(), name='abrir_caja'),
    # Aquí irán más URLs de caja (cerrar, historial, etc.)
]
