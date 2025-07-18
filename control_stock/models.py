from django.db import models
from productos.models import Producto
from django.utils import timezone

class MovimientoStock(models.Model):
    TIPO_CHOICES = (
        ('ingreso', 'Ingreso'),
        ('egreso', 'Egreso'),
    )

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(default=timezone.now)
    motivo = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            if self.tipo == 'ingreso':
                self.producto.stock_actual += self.cantidad
            elif self.tipo == 'egreso':
                self.producto.stock_actual -= self.cantidad
            self.producto.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} ({self.cantidad})"