from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='home_dashboard'),
    path('register/', views.register, name='register'),
]