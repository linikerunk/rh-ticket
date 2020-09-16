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
    path = f'documents/{instance.funcionario.unidade}/{instance.funcionario.re_funcionario}/'
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
    categoria = models.ForeignKey(
        Categoria, related_name='subcategorias', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class ResponsavelCategoria(models.Model):
    responsavel = models.ForeignKey(
        Funcionario, related_name="responsavel", on_delete=models.PROTECT)
    subcategoria = models.ForeignKey(
        SubCategoria, related_name="responsavel", on_delete=models.PROTECT)


class Ticket(models.Model):
    texto = models.TextField(blank=False, verbose_name="Descrição")
    resposta = models.TextField(
        blank=True, null=True, verbose_name="Resposta :")
    data = models.DateTimeField(auto_now_add=True)
    data_finalizada = models.DateTimeField(
        null=True, blank=True, verbose_name="Data Finalizada : ")
    finalizado = models.BooleanField(default=False, choices=BOOL_CHOICES)
    upload_arquivo = models.FileField(
        blank=True, upload_to=update_filename, verbose_name="Anexar Arquivos : ")
    funcionario = models.ForeignKey(
        Funcionario, related_name="tickets", on_delete=models.PROTECT)
    categoria = models.ForeignKey(
        Categoria, related_name='tickets', on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(
        SubCategoria, related_name='tickets', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.finalizado:
            if not self.data_finalizada:
                pass
                self.data_finalizada = timezone.now()
        return super(Ticket, self).save(*args, **kwargs)

    def tempo_aberto(self):
        tempo = timezone.now() - self.data
        tempo = tempo.days
        if tempo == 0:  # Ajuste no tempo
            tempo = 1
        print(tempo)
        return tempo

    def tempo_finalizado(self):
        print(self.data_finalizada)
        if self.data_finalizada:
            tempo_finalizado = self.data_finalizada - self.data
            if abs(tempo_finalizado.days) == 0:
                tempo_finalizada = 1
                return abs(tempo_finalizada)
            return abs(tempo_finalizado.days)
        return 1

    def __str__(self):
        return f'Ticket Número {self.id}, Funcionário {self.funcionario.re_funcionario}'


class HistoricoTicket(models.Model):
    data_mensagem = models.DateTimeField()
    mensagem = models.TextField(
        blank=True, null=True, verbose_name="Mensagem :")
    ticket = models.ForeignKey(
        Ticket, related_name='historico', on_delete=models.CASCADE)
    funcionario = models.ForeignKey(
        Funcionario, related_name="historico", on_delete=models.PROTECT)

    def __str__(self):
        return f'Mensagem de {self.funcionario} referênte ao Ticket {self.ticket.id}, data :{self.data_mensagem}'
