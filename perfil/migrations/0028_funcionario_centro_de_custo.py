# Generated by Django 2.2.9 on 2020-07-28 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0027_auto_20200724_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionario',
            name='centro_de_custo',
            field=models.CharField(default=1, max_length=12, verbose_name='Centro de Custo'),
            preserve_default=False,
        ),
    ]
