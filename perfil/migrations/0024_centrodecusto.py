# Generated by Django 2.2.9 on 2020-07-21 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0023_customlogentry'),
    ]

    operations = [
        migrations.CreateModel(
            name='CentroDeCusto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=12, verbose_name='Número Centro de Custo')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome do Centro de Custo')),
                ('responsaveis', models.ManyToManyField(related_name='funcionarios', to='perfil.Funcionario')),
            ],
        ),
    ]
