# caja/models.py
from django.db import models
from django.contrib.auth.models import User # Necesario si usas el modelo de usuario de Django

# ====================
# Modelo: Caja
# ====================
class Caja(models.Model):
    usuario_apertura = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='cajas_abiertas')
    fecha_apertura = models.DateTimeField(auto_now_add=True)
    monto_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    monto_cierre = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    diferencia = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    esta_abierta = models.BooleanField(default=True)
    # Puedes añadir un campo para el monto actual si lo necesitas en tiempo real
    # monto_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        # Asegúrate de que usuario_apertura no sea None antes de acceder a .username
        username = self.usuario_apertura.username if self.usuario_apertura else "N/A"
        return f"Caja abierta por {username} el {self.fecha_apertura.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name_plural = "Cajas"

# ====================
# Modelo: IntentoCierre
# ====================
class IntentoCierre(models.Model):
    caja = models.ForeignKey(Caja, on_delete=models.CASCADE, related_name='intentos_cierre')
    usuario_intento = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_intento = models.DateTimeField(auto_now_add=True)
    monto_declarado = models.DecimalField(max_digits=10, decimal_places=2)
    diferencia_calculada = models.DecimalField(max_digits=10, decimal_places=2)
    validado_ok = models.BooleanField(default=False) # Si el intento de cierre fue exitoso
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        # Asegúrate de que usuario_intento no sea None antes de acceder a .username
        username = self.usuario_intento.username if self.usuario_intento else "N/A"
        return f"Intento de cierre para Caja {self.caja.id} por {username} el {self.fecha_intento.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name_plural = "Intentos de Cierre"

# ====================
# Modelo: EventoCaja
# ====================
class TipoEvento(models.TextChoices):
    APERTURA = 'AP', 'Apertura de Caja'
    CIERRE = 'CI', 'Cierre de Caja'
    BLOQUEO = 'BL', 'Bloqueo de Caja'
    DESBLOQUEO = 'DB', 'Desbloqueo de Caja'
    ERROR = 'ER', 'Error en Proceso'
    # Puedes añadir más tipos de eventos según necesites

class EventoCaja(models.Model):
    caja = models.ForeignKey(Caja, on_delete=models.CASCADE, related_name='eventos_caja', null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    tipo_evento = models.CharField(max_length=2, choices=TipoEvento.choices)
    descripcion = models.TextField()
    fecha_evento = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.fecha_evento.strftime('%Y-%m-%d %H:%M')}] {self.tipo_evento} - {self.descripcion}"

    class Meta:
        ordering = ['-fecha_evento'] # Ordenar por fecha descendente
        verbose_name_plural = "Eventos de Caja"