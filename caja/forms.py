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

#  cierre de caja
class CierreCajaForm(forms.Form):
    monto_declarado = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        label="Monto Final Declarado en Caja",
        help_text="Ingrese el monto total de dinero que hay en la caja."
    )
    observaciones = forms.CharField(
        widget=forms.Textarea, # Campo de texto multilinea
        required=False,       # El campo no es obligatorio
        label="Observaciones",
        help_text="Cualquier nota adicional sobre el cierre de caja."
    )

