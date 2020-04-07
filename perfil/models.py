from django.db import models
from datetime import datetime
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings


# Create your models here.

class Unidade(models.Model):
    nome = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.nome


class Perfil(models.Model):
    unidade = models.ForeignKey(Unidade, related_name="+", on_delete=models.PROTECT)
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'usuário : {self.usuario} da unidade : {self.unidade}'


class Funcionario(models.Model):
    re_funcionario = models.CharField(max_length=5, verbose_name="RE")
    nome = models.CharField(max_length=55, verbose_name="Nome do Funcionário")
    centro_de_custo = models.CharField(max_length=10)
    ramal = models.CharField(max_length=4, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True, verbose_name="Email Funcionário")
    perfil = models.ForeignKey(Perfil, related_name="funcionarios", on_delete=models.PROTECT)

    class Meta:
        unique_together = ['re_funcionario']
    
    def __str__(self):
        return f'Funcionário : {self.re_funcionario} - {self.perfil.unidade}'

    def save(self, *args, **kwargs): 
        self.nome = self.nome.upper() 
        super(Funcionario, self).save(*args, **kwargs) 