# caja/views.py
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin # Para asegurar que solo usuarios logueados puedan abrir caja

from .models import Caja, EventoCaja, TipoEvento # Importa tus modelos y enumeraciones
from .forms import AperturaCajaForm # Importa el formulario que acabas de crear

class AbrirCajaView(LoginRequiredMixin, View):
    def get(self, request):
        # 1. Verificar si ya hay una caja abierta
        # Usamos .filter() para buscar instancias de Caja con esta_abierta=True
        # .exists() devuelve True/False si hay al menos una.
        # .first() obtiene el primer objeto que coincida, o None si no hay.
        caja_actual = Caja.objects.filter(esta_abierta=True).first()

        if caja_actual:
            # Si ya hay una caja abierta, no permitir abrir otra.
            # Puedes redirigir a una página de estado de caja o mostrar un mensaje.
            return render(request, 'caja/caja_abierta_info.html', {
                'caja_actual': caja_actual,
                'message': f"Ya existe una caja abierta (ID: {caja_actual.id}). No se puede abrir otra."
            })

        # Si no hay caja abierta, mostrar el formulario de apertura
        form = AperturaCajaForm()
        return render(request, 'caja/abrir_caja.html', {'form': form})

    def post(self, request):
        form = AperturaCajaForm(request.POST) # Cargar los datos enviados por el usuario
        if form.is_valid():
            # Los datos del formulario son válidos
            monto_inicial = form.cleaned_data['monto_inicial'] # Obtener el monto

            # 2. Verificar de nuevo si no hay una caja abierta (prevención de race condition si múltiples usuarios intentan abrir al mismo tiempo)
            if Caja.objects.filter(esta_abierta=True).exists():
                return render(request, 'caja/caja_abierta_info.html', {
                    'message': 'Error: Otra caja fue abierta justo antes. No se puede abrir más de una.'
                })

            # Crear la nueva instancia de Caja
            caja = Caja.objects.create(
                usuario_apertura=request.user, # Asignar el usuario actual logueado
                monto_inicial=monto_inicial,
                esta_abierta=True,
                monto_actual=monto_inicial # Asumimos que el monto actual inicial es el mismo que el inicial
            )

            # Registrar el evento de apertura de caja
            EventoCaja.objects.create(
                caja=caja,
                usuario=request.user,
                tipo_evento=TipoEvento.APERTURA,
                descripcion=f"Caja {caja.id} abierta por {request.user.username} con monto inicial: {monto_inicial}"
            )

            # Redirigir al usuario a una página de éxito o al panel de caja
            # Por ahora, redirigimos al admin para que puedas ver el resultado
            return redirect('admin:caja_caja_changelist') # Redirige a la lista de Cajas en el Admin

        # Si el formulario no es válido, volver a renderizar la página con errores
        return render(request, 'caja/abrir_caja.html', {'form': form})