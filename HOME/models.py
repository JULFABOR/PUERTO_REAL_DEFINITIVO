from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

#Eje central del sistema
class Categorias_Productos (models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=150)
    DELETE_CateP = models.BooleanField(default=False)
    def __str__(self):
        return self.nombre_categoria
class Unidad_Medida_Productos (models.Model):
    id_unidad_medida = models.AutoField(primary_key=True)
    nombre_unidad_medida = models.CharField(max_length=150)
    DELETE_UMP = models.BooleanField(default=False)
    def __str__(self):
        return self.nombre_unidad_medida
class Productos(models.Model):
    id_producto = models.BigAutoField(primary_key=True)
    fecha_registro_producto = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion_producto  = models.DateTimeField(auto_now=True)
    descripcion_producto = models.CharField(max_length=500)
    marca_producto = models.CharField(max_length=100)
    nombre_producto = models.CharField(max_length=200)
    precio_unitario_producto = models.DecimalField(max_digits=8, decimal_places=2)
    unidad_medida_producto = models.ForeignKey(Unidad_Medida_Productos, on_delete=models.CASCADE)
    categoria_producto = models.ForeignKey(Categorias_Productos, on_delete=models.CASCADE)
    DELETE_Prod = models.BooleanField(default=False)
    def __str__(self):
        return self.nombre_producto
class Productos_Descartados(models.Model):
    id_producto_descartado = models.BigAutoField(primary_key=True)
    producto_prod_desc = models.ForeignKey(Productos, on_delete=models.CASCADE)
    fecha_prod_desc = models.DateField()
    cantidad_prod_desc = models.PositiveIntegerField()
    descripcion_prod_desc = models.CharField(max_length=250)
    motivo_prod_desc = models.CharField(max_length=100, default="Vencimiento")
    DELETE_Prod_Desc = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.producto} - {self.cantidad} vencido(s)"
class Clientes(models.Model):
    user_cliente = models.OneToOneField(User, on_delete=models.CASCADE)
    id_cliente = models.BigAutoField(primary_key=True)
    dni_cliente = models.CharField(max_length=50)
    telefono_cliente = models.CharField(max_length=50)
    DELETE_Cli = models.BooleanField(default=False)
    def __str__(self):
        return self.user.get_full_name()
class Empleados(models.Model):
    user_empleado = models.OneToOneField(User, on_delete=models.CASCADE)
    id_empleado = models.BigAutoField(primary_key=True)
    dni_empleado = models.CharField(50)
    telefono_empleado = models.CharField(max_length=50)
    fecha_baja_empleado = models.DateTimeField()
    DELETE_Emple = models.BooleanField(default=False)
    def __str__(self):
        return self.user.get_full_name()
class Alertas(models.Model):
    id_alerta = models.AutoField(primary_key=True)
    nombre_alerta = models.CharField(max_length=100)
    mensaje_alerta = models.CharField(max_length=500)
    DELETE_Alerta = models.BooleanField(default=False)
    def __str__(self):
        return self.mensaje_alerta
class Tipos_Movimientos(models.Model):
    id_tipo_movimiento = models.AutoField(primary_key=True)
    nombre_movimiento = models.CharField(max_length=50)
    DELETE_TM = models.BooleanField(default=False)
    def __str__(self):
        return self.nombre_movimiento
class Estados(models.Model):
    id_estado = models.AutoField(primary_key=True)
    nombre_estado = models.CharField(max_length=50)
    DELETE_Estado = models.BooleanField(default=False)
    def __str__(self):
        return self.nombre_estado
#Control de Stocks 
class Stocks(models.Model):
    id_stock = models.BigAutoField(primary_key=True)
    cantidad_actual_stock = models.IntegerField()
    lote_stock = models.IntegerField()
    fecha_vencimiento = models.DateTimeField()
    observaciones_stock = models.CharField(max_length=300)
    producto_en_stock = models.ForeignKey(Productos, on_delete=models.CASCADE)
    DELETE_Stock = models.BooleanField(default=False)
    def __str__(self):
        return self.cantidad_actual_stock
class Historial_Stock(models.Model):
    id_historial_stock = models.BigAutoField(primary_key=True)
    cantidad_hstock = models.CharField(max_length=100)
    stock_hs = models.ForeignKey(Stocks, on_delete=models.CASCADE)
    empleado_hs = models.ForeignKey(Empleados,on_delete=models.CASCADE)
    tipo_movimiento_hs = models.ForeignKey(Tipos_Movimientos, on_delete=models.CASCADE)
    fecha_movimiento_hstock = models.DateTimeField(auto_now_add=True)
    stock_anterior_hstock = models.IntegerField()
    stock_nuevo_hstock = models.IntegerField()
    observaciones_hstock = models.CharField(max_length=300)
    DELETE_Hstock = models.BooleanField(default=False)
    def __str__(self):
        return self.fecha_movimiento_hstock
#Apertura/Cierre de Caja
class Cajas(models.Model):
    id_caja = models.AutoField(primary_key=True)
    total_gastos_caja = models.DecimalField(max_digits=10, decimal_places=2)
    total_ventas_caja = models.DecimalField(max_digits=10, decimal_places=2)
    apertura_caja = models.DateTimeField()
    cierre_caja = models.DateTimeField()
    monto_apertura_caja = models.DecimalField(max_digits=10, decimal_places=2)
    monto_cierre_caja = models.DecimalField(max_digits=10, decimal_places=2)
    monto_teorico_caja = models.DecimalField(max_digits=10, decimal_places=2)
    diferencia_caja = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones_caja = models.CharField(max_length=200)
    estado_caja = models.ForeignKey(Estados,on_delete=models.CASCADE)
    DELETE_Caja = models.BooleanField(default=False)
    def __str__(self):
        return self.monto_apertura_caja
class Tipo_Evento(models.Model):
    id_evento = models.AutoField(primary_key=True)
    nombre_evento = models.CharField(max_length=50)
    DELETE_Event = models.BooleanField(default=False)
    def __str__(self):
        return self.nombre_evento
class Evento_Caja(models.Model):    
    descripcion_evento_caja = models.CharField(max_length=200)
    fecha_evento_caja = models.DateTimeField(auto_now_add=True)
    caja_event_caja = models.ForeignKey(Cajas,on_delete=models.CASCADE)
    empleado_event_caja = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    tipo_event_caja = models.ForeignKey(Tipo_Evento,on_delete=models.CASCADE)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['caja_event_caja', 'empleado_event_caja', 'tipo_event_caja'], name='unique_evento_caja_combinacion')
            ]
    def __str__(self):
        return self.fecha_evento_caja
#Compras
class Proveedores(models.Model):
    id_proveedor = models.BigAutoField(primary_key=True)
    nombre_proveedor = models.CharField(max_length=100)
    razon_social_proveedor = models.CharField(max_length=100)
    telefono_proveedor = models.CharField(max_length=20)
    cuit_proveedor = models.CharField(max_length=100)
    correo_proveedor = models.EmailField(max_length=100)
    estado_proveedor = models.ForeignKey(Estados,on_delete=models.CASCADE)
    DELETE_Prov = models.BooleanField(default=False)
    def __str__(self):
        return self.nombre_proveedor
class Compras(models.Model):
    id_compra = models.BigAutoField(primary_key =True)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    total_compra = models.DecimalField(max_digits=10, decimal_places=2)
    proveedor_compra = models.ForeignKey(Proveedores, on_delete=models.CASCADE)
    estado_compra = models.ForeignKey(Estados, on_delete=models.CASCADE)
    DELETE_Comp = models.BooleanField(default=False)
    def __str__(self):
        return self.fecha_compra
class Detalle_Compras(models.Model):
    id_det_comp = models.BigAutoField(primary_key=True)
    precio_unidad_det_comp = models.DecimalField(max_digits=10, decimal_places=2)
    cant_det_comp = models.IntegerField()
    subtotal_det_comp = models.DecimalField(max_digits=10, decimal_places=2)
    producto_dt_comp = models.ForeignKey(Productos, on_delete=models.CASCADE)
    compra_dt_comp = models.ForeignKey(Compras, on_delete=models.CASCADE)
    DELETE_Det_Comp = models.BooleanField(default=False)
    def __str__(self):
        return self.subtotal_det_comp
class Proveedores_Productos(models.Model):
    id_prov_x_prod = models.BigAutoField(primary_key=True)
    precio_unitario_prov_x_prod = models.IntegerField()
    proveedor_prov_x_prod = models.ForeignKey(Proveedores, on_delete=models.CASCADE)
    producto_prov_x_prod = models.ForeignKey(Productos, on_delete=models.CASCADE)
    DELETE_Prov_X_Prod = models.BooleanField(default=False)
    def __str__(self):  
        return self.precio_unitario_prov_x_prod
class Ordenes_Compras(models.Model):
    id_orden_compra = models.BigAutoField(primary_key=True)
    fecha_orden_compra = models.DateTimeField(auto_now_add=True)
    proveedor_orden_compra = models.ForeignKey(Proveedores, on_delete=models.CASCADE)
    empleado_orden_compra = models.ForeignKey(Empleados, on_delete=models.CASCADE)    
    DELETE_Orden_Comp = models.BooleanField(default=False)
    def __str__(self):
        return self.fecha_orden_compra
class Detalle_Pedidos(models.Model):
    id_det_pedi = models.BigAutoField(primary_key=True)
    cantidad_det_pedi = models.IntegerField()
    precio_unitario_det_pedi = models.DecimalField(max_digits=10, decimal_places=2)
    provxprod_det_pedi = models.ForeignKey(Proveedores_Productos,on_delete=models.CASCADE)
    orden_compra_det_pedi = models.ForeignKey(Ordenes_Compras,on_delete=models.CASCADE)
    DELETE_Det_Pedi = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.producto} x{self.cantidad}"
class Historial_Precio_Producto(models.Model):
    id_histo_precio_prod = models.BigIntegerField(primary_key=True)
    producto_histo_precio_prod = models.ForeignKey(Productos, on_delete=models.CASCADE)
    fecha_histo_precio_prod = models.DateTimeField(auto_now_add=True)
    precio_anterior_histo_precio_prod = models.DecimalField(max_digits=10, decimal_places=2)
    precio_nuevo_histo_precio_prod = models.DecimalField(max_digits=10, decimal_places=2)
    empleado_histo_precio_prod = models.ForeignKey(Empleados,on_delete=models.CASCADE)    
    DELETE_Histo_Precio_Prod = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.producto_histo_precio_prod} - {self.fecha_histo_precio_prod}"
class Historial_Cajas_Compras(models.Model):
    id_histo_caja_compras = models.BigAutoField(primary_key=True)
    compra_histo_caja_comp = models.ForeignKey(Compras,on_delete=models.CASCADE)
    caja_histo_caja_comp = models.ForeignKey(Cajas,on_delete=models.CASCADE)
    empleado_histo_caja_comp = models.ForeignKey(Empleados,on_delete=models.CASCADE)    
    DELETE_Histo_Caja_Comp = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.compra_histo_caja_comp} - {self.caja_histo_caja_comp} - {self.empleado_histo_caja_comp}"
#Fidelizacion de Cliente
class Cupones_Descuento(models.Model):
    id_cupon_desc = models.BigAutoField(primary_key=True)
    descuento_porcentaje_cupon_desc = models.DecimalField(max_digits=10, decimal_places=2)
    descuento_monto_cupon_desc = models.DecimalField(max_digits=10, decimal_places=2)
    puntos_requeridos_cupon_desc = models.IntegerField()
    nombre_cupon_desc = models.CharField(max_length=100)
    descripcion_cupon_desc = models.CharField(max_length=300)
    fecha_inicio_cupon_desc = models.DateField()
    fecha_vencimiento_cupon_desc = models.DateField()
    estado_cupon_desc = models.ForeignKey(Estados, on_delete=models.CASCADE)
    DELETE_Cupon_Desc = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.nombre_cupon_desc} ({self.descuento_porcentaje_cupon_desc}%)"
class Cupones_Canjeado (models.Model):
    id_cupon_canje = models.BigAutoField(primary_key=True)
    fecha_utilizado_canje = models.DateTimeField(auto_now_add=True)
    cliente_cupon_canje = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    cupon_descuento_cupon_canje = models.ForeignKey(Cupones_Descuento, on_delete=models.CASCADE)
    DELETE_Cupon_Canje = models.BooleanField(default=False)
    def __str__(self):
        return self.fecha_utilizado_canje
class Origen_Puntos(models.Model):
    id_origen_puntos = models.AutoField(primary_key=True)
    nombre_origen = models.CharField(max_length=50)
    DELETE_OP = models.BooleanField(default=False)
    def __str__(self):
        return self.nombre_origen
class Transacciones_Puntos(models.Model):
    id_transaccion = models.AutoField(primary_key=True)
    fecha_obtencion = models.DateTimeField(auto_now_add=True)
    cliente_transaccion = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    origen_puntos_transaccion = models.ForeignKey(Origen_Puntos, on_delete=models.CASCADE)
    DELETE_Trans = models.BooleanField(default=True)
    def __str__(self):
        return self.fecha_obtencion
class Puntajes(models.Model):
    id_puntaje = models.BigAutoField(primary_key=True)
    puntos_acumulados = models.BigIntegerField()
    puntos_utilizados = models.BigIntegerField()
    transaccion_puntaje = models.ForeignKey(Transacciones_Puntos, on_delete=models.CASCADE)
    DELETE_Puntaje = models.BooleanField(default=False)
    def _str_(self):
        return self.puntos_acumulados
#Ventas
class Ventas(models.Model):
    id_venta = models.BigAutoField(primary_key = True)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    observaciones_venta = models.CharField(max_length=200)
    cliente_venta = models.ForeignKey(Clientes, on_delete= models.CASCADE)
    empleado_venta = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    estado_venta = models.ForeignKey(Estados, on_delete=models.CASCADE)
    caja_venta = models.ForeignKey(Cajas,on_delete=models.CASCADE)
    DELETE_Vent = models.BooleanField(default=False)
    def __str__(self):
        return self.total_venta
class Detalle_Ventas(models.Model):
    id_det_vent = models.BigAutoField(primary_key=True)
    precio_unitario_det_vent = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_det_vent = models.IntegerField()
    subtotal_det_vent = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion_det_vent = models.CharField(max_length=200)
    producto_det_vent = models.ForeignKey(Productos, on_delete=models.CASCADE)
    venta_det_vent = models.ForeignKey(Ventas, on_delete=models.CASCADE)
    cupon_canje_det_vent = models.ForeignKey(Cupones_Canjeado, on_delete=models.CASCADE)
    DELETE_Det_Vent = models.BooleanField(default=False)
    def __str__(self):
        return self.subtotal_det_vent
class Metodos_Pago(models.Model):
    id_metodo = models.AutoField(primary_key=True)
    nombre_metodo = models.CharField(max_length=200)
    DELETE_Met = models.BooleanField(default=False)
    def __str__(self):
        return self.nombre_metodo
class Venta_MetodoPago(models.Model):
    metodopago_vent_metpag = models.ForeignKey(Metodos_Pago, on_delete=models.CASCADE)
    venta_vent_metpag = models.ForeignKey(Ventas, on_delete=models.CASCADE)
    DELETE_Vent_MetPag = models.BooleanField(default=False)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['metodopago_vent_metpag', 'venta_vent_metpag'], name='unique_venta_metodopago_combinacion')
        ]
    def __str__(self):
        return self.metodopago_vent_metpag
#Devolucion
class Devoluciones(models.Model):
    id_devolucion = models.BigAutoField(primary_key=True)
    fecha_devolucion = models.DateTimeField(auto_now_add=True)
    DELETE_Devo = models.BooleanField(default=False)
    def __str__(self):
        return self.fecha_devolucion
class Detalle_Devoluciones(models.Model):
     id_det_devo = models.BigAutoField(primary_key=True)
     subtotal_det_devo = models.DecimalField(max_digits=10, decimal_places=2)
     descripcion_det_devo = models.CharField(max_length=200)
     producto_det_devo = models.ForeignKey(Productos, on_delete=models.CASCADE)
     devolucion_det_devo = models.ForeignKey(Devoluciones, on_delete=models.CASCADE)
     DELETE_Det_Devo = models.BooleanField(default=False)
#Direcciones
class Provincias(models.Model):
    id_provin = models.AutoField(primary_key=True)
    nombre_provincia = models.CharField(max_length=100)
    DELETE_Provin = models.BooleanField(default=False)
    def __str__(self):
        return self.nombre_provincia
class Ciudades(models.Model):
    id_ciudad = models.AutoField(primary_key=True) 
    nombre_ciudad = models.CharField(max_length=100)
    provincia_ciudad = models.ForeignKey(Provincias, on_delete=models.CASCADE)
    DELETE_Ciud = models.BooleanField(default=False)
    def __str__(self):
        return self.nombre_ciudad
class Barrios(models.Model):
    id_barrio = models.AutoField(primary_key=True)
    nombre_barrio= models.CharField(max_length=100)
    ciudad_barrio = models.ForeignKey(Ciudades, on_delete=models.CASCADE)
    DELETE_Barrio = models.BooleanField(default=False)
    def __str__(self):
        return self.nombre_barrio
class Calles(models.Model):
    id_calle = models.AutoField(primary_key=True)
    nombre_calle = models.CharField(max_length=100)
    barrio_calle = models.ForeignKey(Barrios, on_delete=models.CASCADE)
    DELETE_Calle = models.BooleanField(default=False)
    def __str__(self):
        return self.nombre_calle
class Direcciones (models.Model):
    id_direccion = models.AutoField(primary_key=True)
    nombre_direccion = models.CharField(max_length=100)
    departamento_direccion = models.CharField(max_length=100)
    referecia_direccion = models.CharField(max_length=100)
    calle_direccion = models.ForeignKey(Calles, on_delete=models.CASCADE)
    usuario_direccion = models.ForeignKey(User, on_delete=models.CASCADE)
    DELETE_Dir = models.BooleanField(default=False)
    def __str__(self):
        return self.nombre_direccion
#Control Ingresos y Egresos
class Movimientos_Financieros(models.Model):
    id_movi_finan = models.BigAutoField(primary_key=True)
    fecha_movimiento = models.DateTimeField()
    total_movimiento = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion_movimiento = models.CharField(max_length=300)
    DELETE_Movi_Finan = models.BooleanField(default=False)
    def __str__(self):
        return self.fecha_movimiento
