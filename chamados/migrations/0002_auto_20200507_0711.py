# Generated by Django 3.0.4 on 2020-05-07 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chamados', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='resposta',
            field=models.TextField(blank=True, null=True),
        ),
    ]
