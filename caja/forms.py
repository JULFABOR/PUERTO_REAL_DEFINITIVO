# caja/forms.py
from django import forms

class AperturaCajaForm(forms.Form):
    monto_inicial = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        label="Monto Inicial de Caja",
        help_text="Ingrese el monto con el que se abre la caja."
    )