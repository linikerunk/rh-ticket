# Generated by Django 2.2.9 on 2020-06-29 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formularios', '0003_auto_20200629_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='justificativaausencia',
            name='justificativa',
            field=models.CharField(choices=[('Débido em Banco de HS', 'Débido em Banco de HS'), ('Descanso de Jornadas', 'Descanso de Jornadas'), ('Serviço Externo', 'Serviço Externo'), ('Viagem à Trabalho', 'Viagem à Trabalho'), ('Treinamento Externo', 'Treinamento Externo'), ('Folga TRE', 'Folga TRE')], max_length=21, verbose_name='Justificativa'),
        ),
        migrations.AlterField(
            model_name='justificativaausencia',
            name='tipo_de_ausencia',
            field=models.CharField(choices=[('Falta', 'Falta'), ('Atraso', 'Atraso'), ('Saída Antecipada', 'Saida Antecipada'), ('Saída Intermediária', 'Saída Intermediária')], max_length=19, verbose_name='Tipo de Ausência'),
        ),
    ]
