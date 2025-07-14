from .models import Caja

def hay_caja_abierta():
    """
    Verifica si existe una caja actualmente marcada como abierta.
    Retorna el objeto Caja si hay una abierta, None si no.
    """
    return Caja.objects.filter(esta_abierta=True).first()

def obtener_monto_actual_caja():
    """
    Retorna el monto actual de la caja abierta, o 0 si no hay caja abierta.
    Nota: Esto asume que el campo 'monto_actual' en Caja es el que lleva el saldo.
    Si no, esta función debería calcularlo de otra formañp.
    """
    caja = hay_caja_abierta()
    if caja:
        # Si tienes un campo 'monto_actual' en tu modelo Caja y lo mantienes actualizado
        return caja.monto_actual
        # Si el monto se calcula a partir de transacciones, esta lógica sería más compleja
        # Por ahora, si no tienes monto_actual, puedes devolver caja.monto_inicial o None
    return 0.00