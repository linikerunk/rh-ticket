# Generated by Django 2.2.9 on 2020-06-26 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chamados', '0007_modeloformulariocampo_texto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modeloformulariocampo',
            name='texto',
        ),
        migrations.AddField(
            model_name='modeloformulario',
            name='texto',
            field=models.TextField(default=1, verbose_name='Descrição : '),
            preserve_default=False,
        ),
    ]
