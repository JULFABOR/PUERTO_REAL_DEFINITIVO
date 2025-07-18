from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse # Importar reverse para construir URLs dinámicamente
from django.utils import timezone # Importar timezone para usar timezone.now()

# Importa tus modelos y formularios
from .models import Caja, EventoCaja, IntentoCierre, TipoEvento
from .forms import AperturaCajaForm, CierreCajaForm

# =========================================================================
# Vista: Abrir Caja
# =========================================================================
class AbrirCajaView(LoginRequiredMixin, View):
    def get(self, request):
        # 1. Verificar si ya hay una caja abierta
        caja_actual = Caja.objects.filter(esta_abierta=True).first()

        if caja_actual:
            # Si ya hay una caja abierta, no permitir abrir otra.
            return render(request, 'caja/caja_abierta_info.html', {
                'caja_actual': caja_actual,
                'message': f"Ya existe una caja abierta (ID: {caja_actual.id}). No se puede abrir otra."
            })

        # Si no hay caja abierta, mostrar el formulario de apertura
        form = AperturaCajaForm()
        return render(request, 'caja/abrir_caja.html', {'form': form})

    def post(self, request):
        form = AperturaCajaForm(request.POST)
        if form.is_valid():
            monto_inicial = form.cleaned_data['monto_inicial']

            # 2. Verificar de nuevo si no hay una caja abierta (prevención de race condition)
            if Caja.objects.filter(esta_abierta=True).exists():
                return render(request, 'caja/caja_abierta_info.html', {
                    'message': 'Error: Otra caja fue abierta justo antes. No se puede abrir más de una.'
                })

            # Crear la nueva instancia de Caja
            caja = Caja.objects.create(
                usuario_apertura=request.user,
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
            return redirect('admin:caja_caja_changelist') # Redirige a la lista de Cajas en el Admin

        # Si el formulario no es válido, volver a renderizar la página con errores
        return render(request, 'caja/abrir_caja.html', {'form': form})


# =========================================================================
# Vista: Cerrar Caja
# =========================================================================
class CerrarCajaView(LoginRequiredMixin, View):
    def get(self, request):
        # Obtener la caja actualmente abierta
        caja_actual = Caja.objects.filter(esta_abierta=True).first()

        if not caja_actual:
            # Si no hay caja abierta, redirigir o mostrar un mensaje
            return render(request, 'caja/no_caja_abierta_info.html', {
                'message': 'No hay ninguna caja abierta para cerrar.'
            })

        form = CierreCajaForm()
        context = {
            'form': form,
            'caja': caja_actual,
            'message': 'Ingrese el monto final para cerrar la caja.'
        }
        return render(request, 'caja/cerrar_caja.html', context)

    def post(self, request):
        caja_actual = Caja.objects.filter(esta_abierta=True).first()

        if not caja_actual:
            return render(request, 'caja/no_caja_abierta_info.html', {
                'message': 'Error: No hay ninguna caja abierta para cerrar.'
            })

        form = CierreCajaForm(request.POST)
        if form.is_valid():
            monto_declarado = form.cleaned_data['monto_declarado']
            observaciones = form.cleaned_data.get('observaciones', '')

            # 1. Calcular la diferencia (TEMPORAL: Ajustar esto con el monto real de transacciones)
            # Para el ejemplo, usaremos monto_inicial para simular el monto_actual.
            # En un sistema real, 'monto_actual' debería ser el saldo real sumando/restando ventas/gastos.
            monto_actual_calculado = caja_actual.monto_inicial # Aquí se integraría la lógica de ventas/gastos

            diferencia_calculada = monto_declarado - monto_actual_calculado

            # 2. Registrar el intento de cierre
            intento_cierre = IntentoCierre.objects.create(
                caja=caja_actual,
                usuario_intento=request.user,
                monto_declarado=monto_declarado,
                diferencia_calculada=diferencia_calculada,
                observaciones=observaciones
            )

            # 3. Lógica de Validación de Cierre
            if diferencia_calculada == 0:
                intento_cierre.validado_ok = True
                intento_cierre.save()

                # Si la validación es exitosa, cerrar la caja principal
                caja_actual.fecha_cierre = timezone.now()
                caja_actual.monto_cierre = monto_declarado
                caja_actual.diferencia = diferencia_calculada
                caja_actual.esta_abierta = False
                caja_actual.save()

                # Registrar evento de CIERRE exitoso
                EventoCaja.objects.create(
                    caja=caja_actual,
                    usuario=request.user,
                    tipo_evento=TipoEvento.CIERRE,
                    descripcion=f"Caja {caja_actual.id} cerrada correctamente por {request.user.username}. Monto final: {monto_declarado}. Diferencia: {diferencia_calculada}"
                )
                return redirect(reverse('admin:caja_caja_changelist')) # Redirigir al historial de Cajas en el Admin (puedes cambiar esto a tu historial de cajas personalizado más adelante)
            else:
                # Si hay diferencia, la caja NO se cierra automáticamente
                intento_cierre.validado_ok = False
                intento_cierre.save()

                # Registrar evento de CIERRE con diferencia/error
                EventoCaja.objects.create(
                    caja=caja_actual,
                    usuario=request.user,
                    tipo_evento=TipoEvento.ERROR, # O un tipo específico como 'Diferencia' si lo defines
                    descripcion=f"Intento de cierre de Caja {caja_actual.id} por {request.user.username} con DIFERENCIA: {diferencia_calculada}. Monto declarado: {monto_declarado}"
                )
                # Mostrar mensaje de error en la misma página de cierre
                context = {
                    'form': form,
                    'caja': caja_actual,
                    'message': f'Error en el cierre: Existe una diferencia de ${diferencia_calculada}. La caja no se cerró automáticamente.',
                    'error_diferencia': True # Una bandera para la plantilla HTML
                }
                return render(request, 'caja/cerrar_caja.html', context)
        else:
            # Si el formulario no es válido, volver a renderizar con errores
            context = {
                'form': form,
                'caja': caja_actual,
                'message': 'Por favor, corrija los errores del formulario.'
            }
            return render(request, 'caja/cerrar_caja.html', context)