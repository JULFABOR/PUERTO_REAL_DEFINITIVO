from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('cliente', 'Cliente'),
        ('empleado', 'Empleado'),
    )

    email = forms.EmailField(required=True)
    rol = forms.ChoiceField(choices=ROLE_CHOICES, label="Rol del usuario")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'rol']