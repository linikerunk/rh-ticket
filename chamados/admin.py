# -*- coding: utf-8 -*-

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Ticket, Categoria, SubCategoria
from perfil.models import Funcionario
# Register your models here.

@admin.register(Ticket)
class TicketAdmin(ImportExportModelAdmin):
    list_display = ['id', 'funcionario', 'texto', 'data', 'finalizado']
    list_filter = ['funcionario__unidade']

    

@admin.register(Categoria)
class CategoriaAdmin(ImportExportModelAdmin):
    fields = ['nome']


@admin.register(SubCategoria)
class SubCategoriaAdmin(ImportExportModelAdmin):
    fields = ['nome', 'categoria']