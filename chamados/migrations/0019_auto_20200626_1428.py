# Generated by Django 2.2.9 on 2020-06-26 17:28
# testando

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chamados', '0018_modeloformulario_ticket'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modeloformulario',
            name='ticket',
        ),
        migrations.AddField(
            model_name='ticket',
            name='modelo_formulario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='tickets', to='chamados.ModeloFormulario'),
            preserve_default=False,
        ),
    ]
