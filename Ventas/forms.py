from django import forms
from HOME.models import Ventas

class VentaForm(forms.ModelForm):
    class Meta:
        model = Ventas
        fields = '__all__'