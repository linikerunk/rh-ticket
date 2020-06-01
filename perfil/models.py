from django.db import models
from datetime import datetime
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings


# Create your models here.

class Unidade(models.Model):
    nome = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.nome


class Funcionario(models.Model):
    re_funcionario = models.CharField(max_length=9, verbose_name="RE")
    nome = models.CharField(max_length=55, verbose_name="Funcionário :")
    cpf = models.CharField(max_length=11, verbose_name="CPF")
    centro_de_custo = models.CharField(max_length=10)
    ramal = models.CharField(max_length=9, blank=True, null=True, verbose_name="Ramal")
    telefone = models.CharField(max_length=11, blank=True, verbose_name="Telefone")
    email_corporativo = models.EmailField(max_length=254, verbose_name="Email Corporativo", blank=True, null=True)
    email = models.EmailField(max_length=254, verbose_name="Email Pessoal", blank=True, null=True)
    unidade = models.ForeignKey(Unidade, related_name="funcionarios", on_delete=models.PROTECT)

    class Meta:
        unique_together = ['re_funcionario', 'unidade']
    
    def __str__(self):
        return f'Funcionário : {self.re_funcionario} '

    def save(self, *args, **kwargs): 
        self.nome = self.nome.upper() 
        super(Funcionario, self).save(*args, **kwargs) 

class Perfil(models.Model):
    unidade = models.ForeignKey(Unidade, related_name="+", on_delete=models.PROTECT)
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="perfil_usuario", on_delete=models.CASCADE)
    funcionario = models.OneToOneField(Funcionario, related_name="perfil", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'usuário : {self.usuario} da unidade : {self.unidade}'

    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            Perfil.objects.create(user=instance)
        instance.perfil.save()
    
        
