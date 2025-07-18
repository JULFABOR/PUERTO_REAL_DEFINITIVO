from django.test import TestCase
from .models import Categoria, Producto, MovimientoStock

class CategoriaModelTest(TestCase):
    def test_crear_categoria(self):
        categoria = Categoria.objects.create(nombre='Bebidas')
        self.assertEqual(str(categoria), 'Bebidas')