# Generated by Django 2.2.9 on 2020-06-26 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chamados', '0010_auto_20200626_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modeloformulario',
            name='texto',
            field=models.TextField(verbose_name='Descrição'),
        ),
    ]
