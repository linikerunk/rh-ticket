from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Unidade, Funcionario, Ticket, Perfil

# Register your models here.

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    pass


@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ['nome']
    list_filter = ['nome']
    pass


@admin.register(Funcionario)
class FuncionarioAdmin(ImportExportModelAdmin):
    list_display = ['id', 'nome', 'unidade']
    list_filter = ['unidade']  


@admin.register(Ticket)
class TicketAdmin(ImportExportModelAdmin):
    list_display = ['id', 'funcionario', 'texto', 'data', 'finalizado']
    list_filter = ['funcionario__unidade']
