# Generated by Django 3.0.4 on 2020-05-07 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('perfil', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.CharField(choices=[('', ''), ('Benefícios', 'Benefícios'), ('Cargos e Salários', 'Cargos e Sálarios'), ('Férias', 'Férias'), ('Folha de Pagamento', 'Folha de Pagamento'), ('Ponto', 'Ponto'), ('Treinamento', 'Treinamento')], default='--------------------------------', max_length=23)),
                ('nome', models.CharField(max_length=55, verbose_name='Nome do Funcionário')),
                ('texto', models.TextField(verbose_name='Descrição')),
                ('resposta', models.TextField(blank=True, null=True)),
                ('data', models.DateTimeField()),
                ('data_finalizada', models.DateTimeField(blank=True, null=True, verbose_name='Data Finalizada ')),
                ('finalizado', models.BooleanField(choices=[(True, 'Sim'), (False, 'Não')], default=False)),
                ('upload_arquivo', models.FileField(blank=True, upload_to='documents/%Y/%m/%d')),
                ('funcionario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tickets', to='perfil.Funcionario')),
            ],
        ),
    ]
