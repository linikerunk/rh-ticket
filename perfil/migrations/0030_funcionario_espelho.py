# Generated by Django 2.2.9 on 2020-07-29 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0029_remove_funcionario_centro_de_custo'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionario',
            name='espelho',
            field=models.ImageField(default='0000.jpg', max_length=200, upload_to='espelhos', verbose_name='Fotos Funcionários'),
        ),
    ]
