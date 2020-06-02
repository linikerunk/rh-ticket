# Generated by Django 3.0.4 on 2020-06-02 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('perfil', '0013_auto_20200601_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionario',
            name='usuario',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Perfil',
        ),
    ]
