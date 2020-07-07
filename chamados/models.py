# -*- coding: utf-8 -*-
import os 
from datetime import datetime

from django.db import models

from django.utils import timezone
from model_utils.models import TimeStampedModel
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings


from perfil.models import Funcionario

BOOL_CHOICES = ((True, 'Sim'), (False, 'Não'))


def update_filename(instance, filename):
    path=f'documents/{instance.funcionario.unidade}/{instance.funcionario.re_funcionario}/'
    output = ""
    for i in range(len(filename)):
        if ord(filename[i]) < 127:
            output += (filename[i])
    filename = output
    path = path.replace('ç', 'c').replace('ã', 'a').replace('´', '')
    return os.path.join(path, filename)


class Categoria(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.nome


class SubCategoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    categoria = models.ForeignKey(Categoria, related_name='subcategorias', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Ticket(models.Model):
    texto = models.TextField(blank=False, verbose_name="Descrição")
    resposta = models.TextField(blank=True, null=True, verbose_name="Resposta :")
    data = models.DateTimeField(auto_now_add=True)
    data_finalizada = models.DateTimeField(null=True, blank=True, verbose_name="Data Finalizada : ")
    finalizado = models.BooleanField(default=False, choices=BOOL_CHOICES)
    upload_arquivo = models.FileField(blank=True, upload_to=update_filename, verbose_name="Anexar Arquivos : ")
    funcionario = models.ForeignKey(Funcionario, related_name="tickets", on_delete=models.PROTECT)
    categoria = models.ForeignKey(Categoria, related_name='tickets', on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(SubCategoria, related_name='tickets', on_delete=models.CASCADE)
    
    
    def save(self, *args, **kwargs):
        if self.finalizado:
            if not self.data_finalizada:
                pass
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




# class Campo(TimeStampedModel):
#     nome = models.CharField(verbose_name="Nome do Campo", max_length=100, unique=True)

#     class Meta:
#         ordering = ['-created']
#         verbose_name = 'Campo'
#         verbose_name_plural = 'Campos'

#     def __str__(self):
#         return self.nome


# class ModeloFormulario(TimeStampedModel):
#     campo = models.ManyToManyField(
#         Campo, through='ModeloFormularioCampo', related_name='campo'
#     )

#     texto = models.TextField(verbose_name="Observação", blank = True)
    
#     subcategoria = models.ForeignKey(SubCategoria, related_name='modelo_formulario', on_delete=models.CASCADE)


#     class Meta:
#         verbose_name = 'Modelo de Formulários'
#         verbose_name_plural = 'Modelos de Formulários'
#         ordering = ['-created']

#     def __str__(self):
#         return f'Formulário da subcategoria : {self.subcategoria}'


# class ModeloFormularioCampo(models.Model):
#     modelo_formulario = models.ForeignKey(
#         ModeloFormulario,
#         verbose_name = 'Formulário',
#         related_name = 'modelo_formulario',
#         on_delete=models.CASCADE
#     )

#     campo = models.ForeignKey(
#         Campo,
#         verbose_name = 'Campos',
#         related_name = 'modelo_formulario',
#         on_delete=models.CASCADE
#     )

#     valor_campo = models.CharField(verbose_name="Valor do Campo", max_length=250, blank=True)

#     class Meta:
#         verbose_name = 'Formulário e Campo'
#         verbose_name_plural = 'Formulários e Campos'
#         ordering = ['-campo__nome']
#         unique_together = ['modelo_formulario', 'campo']
    
#     def __str__(self):
#         return f'{self.id}'