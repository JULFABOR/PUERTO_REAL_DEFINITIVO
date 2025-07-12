from .models import Empleados, Clientes

def user_role(request):
    rol = "invitado"
    user = request.user

    if user.is_authenticated:
        if hasattr(user, 'empleado'):
            rol = "empleado"
        elif hasattr(user, 'cliente'):
            rol = "cliente"
        elif user.is_superuser:
            rol = "admin"

    return {'rol': rol}