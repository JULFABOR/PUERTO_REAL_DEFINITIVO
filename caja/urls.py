from django.urls import path
from . import views # Importa tus vistas

app_name = 'caja' # Define el nombre de la app para usarlo en las URLs (ej. 'caja:abrir_caja')

urlpatterns = [
    path('abrir/', views.AbrirCajaView.as_view(), name='abrir_caja'),
    path('cerrar/', views.CerrarCajaView.as_view(), name='cerrar_caja'), # Asegúrate de que esta línea esté
]