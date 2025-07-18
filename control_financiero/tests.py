from django.test import TestCase
from .models import MovimientoFinanciero

class MovimientoFinancieroTest(TestCase):
    def test_crear_movimiento(self):
        mov = MovimientoFinanciero.objects.create(
            monto=1000,
            tipo='ingreso',
            motivo='Venta',
        )
        self.assertEqual(str(mov), f"ingreso - 1000.00 ({mov.fecha.date()})")