# Generated by Django 2.2.9 on 2020-07-23 18:38
# Sincronizando banco
from django.db import migrations, models


def centro_de_custo_link(apps, schema_editor):
    Funcionario = apps.get_model('perfil', 'Funcionario')
    CentroDeCusto = apps.get_model('perfil', 'CentroDeCusto')

    
    for funcionario in Funcionario.objects.all():
        print('funcionario :', funcionario.centro_de_custo)
        
        centro_de_custo = CentroDeCusto.objects.get(numero=funcionario.centro_de_custo)
        print("Centro de custo : ", centro_de_custo.numero)
        funcionario.centro_de_custo_link = centro_de_custo
        funcionario.save()


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0027_auto_20200724_1051'),
    ]

    operations = [
        migrations.RunPython(centro_de_custo_link),
    ]