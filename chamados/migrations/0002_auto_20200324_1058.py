# Generated by Django 3.0.3 on 2020-03-24 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chamados', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='ramal',
            field=models.CharField(max_length=4, null=True),
        ),
    ]
