# Generated by Django 3.0.4 on 2020-05-29 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0008_auto_20200529_0853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='cpf',
            field=models.CharField(max_length=11, null=True, verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='email',
            field=models.EmailField(max_length=254, null=True, verbose_name='Email Pessoal'),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='email_corporativo',
            field=models.EmailField(max_length=254, null=True, verbose_name='Email Corporativo'),
        ),
    ]
