# Generated by Django 5.2.4 on 2025-07-14 02:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Caja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_apertura', models.DateTimeField(auto_now_add=True)),
                ('monto_inicial', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_cierre', models.DateTimeField(blank=True, null=True)),
                ('monto_cierre', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('diferencia', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('esta_abierta', models.BooleanField(default=True)),
                ('usuario_apertura', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cajas_abiertas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Cajas',
            },
        ),
        migrations.CreateModel(
            name='EventoCaja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_evento', models.CharField(choices=[('AP', 'Apertura de Caja'), ('CI', 'Cierre de Caja'), ('BL', 'Bloqueo de Caja'), ('DB', 'Desbloqueo de Caja'), ('ER', 'Error en Proceso')], max_length=2)),
                ('descripcion', models.TextField()),
                ('fecha_evento', models.DateTimeField(auto_now_add=True)),
                ('caja', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='eventos_caja', to='caja.caja')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Eventos de Caja',
                'ordering': ['-fecha_evento'],
            },
        ),
        migrations.CreateModel(
            name='IntentoCierre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_intento', models.DateTimeField(auto_now_add=True)),
                ('monto_declarado', models.DecimalField(decimal_places=2, max_digits=10)),
                ('diferencia_calculada', models.DecimalField(decimal_places=2, max_digits=10)),
                ('validado_ok', models.BooleanField(default=False)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('caja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intentos_cierre', to='caja.caja')),
                ('usuario_intento', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Intentos de Cierre',
            },
        ),
    ]
