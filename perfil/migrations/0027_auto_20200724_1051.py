# Generated by Django 2.2.9 on 2020-07-24 13:51
# sincronizando
from django.db import migrations, models #


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0026_auto_20200724_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='centrodecusto',
            name='responsaveis',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Responsaveis'),
        ),
    ]
