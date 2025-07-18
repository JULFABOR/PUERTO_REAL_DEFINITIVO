from django.test import TestCase
from django.contrib.auth import get_user_model # Para obtener el modelo de usuario
from .models import Caja, EventoCaja, IntentoCierre, TipoEvento # Importa tus modelos

User = get_user_model() # Obtiene el modelo de usuario activo en tu proyecto

class CajaModelTest(TestCase):
    def setUp(self):
        # Este método se ejecuta antes de cada prueba.
        # Aquí puedes crear datos de prueba necesarios.
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_caja_creation(self):
        # Prueba que una Caja se crea correctamente con los valores esperados
        caja = Caja.objects.create(
            usuario_apertura=self.user,
            monto_inicial=100.50
            # esta_abierta es True por defecto
        )
        self.assertEqual(caja.usuario_apertura, self.user)
        self.assertEqual(caja.monto_inicial, 100.50)
        self.assertTrue(caja.esta_abierta)
        self.assertIsNotNone(caja.fecha_apertura) # Verifica que se haya asignado una fecha

        # Prueba la representación __str__
        self.assertEqual(str(caja), f"Caja abierta por {self.user.username} el {caja.fecha_apertura.strftime('%Y-%m-%d %H:%M')}")


class EventoCajaModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser2', password='password456')
        self.caja = Caja.objects.create(
            usuario_apertura=self.user,
            monto_inicial=200.00
        )

    def test_evento_caja_creation(self):
        evento = EventoCaja.objects.create(
            caja=self.caja,
            usuario=self.user,
            tipo_evento=TipoEvento.APERTURA,
            descripcion="Se abrió la caja con éxito."
        )
        self.assertEqual(evento.caja, self.caja)
        self.assertEqual(evento.usuario, self.user)
        self.assertEqual(evento.tipo_evento, 'AP') # Verifica el valor del choice
        self.assertEqual(evento.descripcion, "Se abrió la caja con éxito.")
        self.assertIsNotNone(evento.fecha_evento)

        # Prueba la representación __str__
        self.assertIn("AP", str(evento))
        self.assertIn("Se abrió la caja con éxito.", str(evento))