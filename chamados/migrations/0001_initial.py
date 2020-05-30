# Generated by Django 3.0.4 on 2020-05-28 18:01

import chamados.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('perfil', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategorias', to='chamados.Categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=55, verbose_name='Funcionário : ')),
                ('texto', models.TextField(verbose_name='Descrição : ')),
                ('resposta', models.TextField(blank=True, null=True)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('data_finalizada', models.DateTimeField(blank=True, null=True, verbose_name='Data Finalizada : ')),
                ('finalizado', models.BooleanField(choices=[(True, 'Sim'), (False, 'Não')], default=False)),
                ('upload_arquivo', models.FileField(blank=True, upload_to=chamados.models.update_filename, verbose_name='Anexar Arquivos : ')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='chamados.Categoria')),
                ('funcionario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tickets', to='perfil.Funcionario')),
                ('subcategoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='chamados.SubCategoria')),
            ],
        ),
    ]
