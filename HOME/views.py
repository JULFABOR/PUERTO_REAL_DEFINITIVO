from django.shortcuts import render,redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Empleados, Clientes
from django.contrib.auth.models import User

@login_required
def dashboard(request):
    rol = "invitado"
    user = request.user

    if hasattr(user, 'empleado'):
        rol = "empleado"
    elif hasattr(user, 'cliente'):
        rol = "cliente"
    elif user.is_superuser:
        rol = "admin"

    return render(request, 'home/dashboard.html', {
        'rol': rol
    })
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()

            rol = form.cleaned_data['rol']

            if rol == 'empleado':
                Empleados.objects.create(user_empleado=user)
            elif rol == 'cliente':
                Clientes.objects.create(user_cliente=user)

            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})