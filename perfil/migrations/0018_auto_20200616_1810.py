# Generated by Django 3.0.4 on 2020-06-16 21:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('perfil', '0017_auto_20200616_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='admissao',
            field=models.CharField(blank=True, default='', max_length=20, verbose_name='Data de Admissão : '),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='demissao',
            field=models.CharField(blank=True, default='', max_length=20, verbose_name='Data de Demissão : '),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254, verbose_name='Email Pessoal'),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='email_corporativo',
            field=models.EmailField(blank=True, default='', max_length=254, verbose_name='Email Corporativo'),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='ramal',
            field=models.CharField(blank=True, default='', max_length=9, verbose_name='Ramal'),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='telefone',
            field=models.CharField(blank=True, default='', max_length=11, verbose_name='Telefone'),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
