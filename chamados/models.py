from django.db import models
from datetime import datetime
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

# Create your models here.

BOOL_CHOICES = ((True, 'Sim'), (False, 'Não'))
CATEGORIA = (
            ('', ''),
            ('Benefícios', 'Benefícios'),
            ('Cargos e Salários', 'Cargos e Sálarios'),
            ('Férias', 'Férias'),
            ('Folha de Pagamento', 'Folha de Pagamento'),
            ('Ponto', 'Ponto'),
            ('Treinamento', 'Treinamento'),
        )

class Unidade(models.Model):
    nome = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.nome


class Perfil(models.Model):
    unidade = models.ForeignKey(Unidade, related_name="+", on_delete=models.PROTECT)
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 

class Funcionario(models.Model):
    re_funcionario = models.CharField(max_length=5, verbose_name="RE")
    nome = models.CharField(max_length=55, verbose_name="Nome do Funcionário")
    centro_de_custo = models.CharField(max_length=10)
    ramal = models.CharField(max_length=4, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True, verbose_name="Email Funcionário")
    unidade = models.ForeignKey(Unidade, related_name="funcionarios", on_delete=models.PROTECT)

    class Meta:
        unique_together = ['re_funcionario', 'unidade']
    
    def __str__(self):
        return f'Funcionário : {self.re_funcionario} - {self.unidade}'

    def save(self, *args, **kwargs): 
        self.nome = self.nome.upper() 
        super(Funcionario, self).save(*args, **kwargs) 


class Ticket(models.Model):
    categoria = models.CharField(
        default = "--------------------------------",
        max_length = 23,
        choices = CATEGORIA
    )
    nome = models.CharField(max_length=55, verbose_name="Nome do Funcionário")
    texto = models.TextField(blank=False, verbose_name="Descrição")
    resposta = models.TextField(blank=True)
    data = models.DateTimeField(auto_now_add=True)
    data_finalizada = models.DateTimeField(null=True, blank=True, verbose_name="Data Finalizada ")
    finalizado = models.BooleanField(default=False, choices=BOOL_CHOICES)
    funcionario = models.ForeignKey(Funcionario, related_name="tickets", on_delete=models.PROTECT)
    upload_arquivo = models.FileField(blank=True, upload_to='documents/%Y/%m/%d')
    
    def save(self, *args, **kwargs):
        if self.finalizado:
            if not self.data_finalizada:
                self.data_finalizada = timezone.now()
        return super(Ticket, self).save(*args, **kwargs)
    
    def tempo_aberto(self):
        tempo = self.data - timezone.now()
        tempo = tempo.days
        return abs(tempo)
    
    def tempo_finalizado(self):
        if self.data_finalizada:
            tempo_finalizado =  timezone.now() - self.data_finalizada 
            if abs(tempo_finalizado.days) == 0:
                tempo_finalizada = 1
                return abs(tempo_finalizada)
            return abs(tempo_finalizado.days)
        return 1
        

    
    def __str__(self):
        return  f'Ticket Número {self.id}, Re funcionário {self.funcionario.re_funcionario}, data {self.data}'
