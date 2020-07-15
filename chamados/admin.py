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
    # save_on_top = True
    # form = TicketForm

    
    # def save_model(self, request, obj, form, change):
    #     if not obj.pk: # call super method if object has no primary key 
    #         super(TicketAdmin, self).save_model(request, obj, form, change)
    #     else:
    #         pass # don't actually save the parent instance

    # def save_related(self, request, form, formsets, change):
    #     pass
        

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