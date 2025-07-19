from django.db import models

class MovimientoFinanciero(models.Model):
    TIPO_CHOICES = (
        ('ingreso', 'Ingreso'),
        ('egreso', 'Egreso'),
    )
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    fecha = models.DateTimeField(auto_now_add=True)
    motivo = models.CharField(max_length=200)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"{self.tipo} - {self.monto} ({self.fecha.date()})"