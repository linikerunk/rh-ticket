# Generated by Django 2.2.9 on 2020-10-20 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chamados', '0026_auto_20201020_1410'),
        ('perfil', '0040_auto_20200922_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='unidade',
            name='categoria',
            field=models.ManyToManyField(to='chamados.Categoria'),
        ),
    ]
