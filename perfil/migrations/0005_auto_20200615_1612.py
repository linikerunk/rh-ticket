# Generated by Django 3.0.4 on 2020-06-15 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0004_auto_20200615_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='admissao',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Data de Admissão : '),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='demissao',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Data de Demissão : '),
        ),
    ]
