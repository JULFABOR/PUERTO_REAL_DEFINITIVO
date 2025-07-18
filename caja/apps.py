from django.apps import AppConfig


class CajaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'caja'
# caja/admin.py
from django.contrib import admin
from .models import Caja, IntentoCierre, EventoCaja

admin.site.register(Caja)
admin.site.register(IntentoCierre)
admin.site.register(EventoCaja)