# Generated by Django 2.2.9 on 2020-06-25 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chamados', '0004_auto_20200625_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='campo',
            name='nome',
            field=models.CharField(default=1, max_length=100, unique=True, verbose_name='Nome do Campo'),
            preserve_default=False,
        ),
    ]
