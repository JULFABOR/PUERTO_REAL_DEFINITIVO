function mostrarCrearVenta() {
    document.getElementById('modalCrearVenta').style.display = 'block';
}
function cerrarCrearVenta() {
    document.getElementById('modalCrearVenta').style.display = 'none';
}
function mostrarEditarVenta(id) {
    // Aquí podrías usar AJAX para cargar el formulario de edición si lo deseas
    document.getElementById('modalEditarVenta').style.display = 'block';
    // Ejemplo: cargar el formulario por AJAX y ponerlo en editarFormContainer
}
function cerrarEditarVenta() {
    document.getElementById('modalEditarVenta').style.display = 'none';
}
function mostrarBorrarVenta(id) {
    document.getElementById('modalBorrarVenta').style.display = 'block';
    // Puedes guardar el id en un input oculto si lo necesitas
}
function cerrarBorrarVenta() {
    document.getElementById('modalBorrarVenta').style.display = 'none';
}
