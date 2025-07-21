from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashboard, name='home_dashboard'),
    path('ventas/', include('Ventas.urls')),
]