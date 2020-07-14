# -*- coding: utf-8 -*-

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (
Ticket,
Categoria,
SubCategoria,
HistoricoTicket,
)
from perfil.models import Funcionario
from .forms import TicketForm

# Register your models here.

@admin.register(Ticket)
class TicketAdmin(ImportExportModelAdmin):
    list_display = ['id', 'funcionario', 'data', 'finalizado']
    list_filter = ['funcionario__unidade']
    form = TicketForm


@admin.register(Categoria)
class CategoriaAdmin(ImportExportModelAdmin):
    fields = ['nome']


@admin.register(SubCategoria)
class SubCategoriaAdmin(ImportExportModelAdmin):
    fields = ['nome', 'categoria']


@admin.register(HistoricoTicket)
class HistoricoTicketAdmin(ImportExportModelAdmin):
    list_display = ['funcionario', 'ticket', 'data_mensagem']
    fields = ['data_mensagem', 'mensagem', 'ticket', 'funcionario']



# class ModeloFormularioCampoInline(admin.TabularInline):
#     model = ModeloFormularioCampo
#     extra = 1


# @admin.register(ModeloFormulario)
# class ModeloFormularioAdmin(admin.ModelAdmin):
#     inlines = [ModeloFormularioCampoInline]

#     def get_readonly_fields(self, request, obj):
#         fields = ['created', 'modified']
        
#         return fields



# @admin.register(Campo)
# class CampoAdmin(ImportExportModelAdmin):
#     pass