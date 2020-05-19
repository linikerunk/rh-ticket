# -*- coding: utf-8 -*-
import os 
from datetime import datetime

from django.db import models

from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings


from perfil.models import Funcionario

# Create your models here.
def update_filename(instance, filename):
    path=f'documents/{instance.funcionario.unidade}/{instance.funcionario.re_funcionario}/'
    #instance.funcionario.perfil.unidade
    output = ""
    for i in range(len(filename)):
        if ord(filename[i]) < 127:
            output += (filename[i])
    filename = output
    path = path.replace('ç', 'c').replace('ã', 'a').replace('´', '')
    return os.path.join(path, filename)


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

class Ticket(models.Model):
    categoria = models.CharField(
        default = "--------------------------------",
        max_length = 23,
        choices = CATEGORIA
    )
    nome = models.CharField(max_length=55, verbose_name="Funcionário : ")
    texto = models.TextField(blank=False, verbose_name="Descrição : ")
    resposta = models.TextField(blank=True, null=True)
    data = models.DateTimeField(auto_now_add=True)
    data_finalizada = models.DateTimeField(null=True, blank=True, verbose_name="Data Finalizada : ")
    finalizado = models.BooleanField(default=False, choices=BOOL_CHOICES)
    upload_arquivo = models.FileField(blank=True, upload_to=update_filename, verbose_name="Anexar Arquivos : ")
    funcionario = models.ForeignKey(Funcionario, related_name="tickets", on_delete=models.PROTECT)
    
    
    def save(self, *args, **kwargs):
        if self.finalizado:
            if not self.data_finalizada:
                self.data_finalizada = timezone.now()
        return super(Ticket, self).save(*args, **kwargs)
    
    def tempo_aberto(self):
        tempo = timezone.now() - self.data
        tempo = tempo.days
        if tempo == 0: #Ajuste no tempo
            tempo = 1
        print(tempo)
        return tempo
    
    def tempo_finalizado(self):
        print(self.data_finalizada)
        if self.data_finalizada:
            tempo_finalizado =  self.data_finalizada - self.data
            if abs(tempo_finalizado.days) == 0:
                tempo_finalizada = 1
                return abs(tempo_finalizada)
            return abs(tempo_finalizado.days)
        return 1
        

    
    def __str__(self):
        return  f'Ticket Número {self.id}, Re funcionário {self.funcionario.re_funcionario}, data {self.data}'
