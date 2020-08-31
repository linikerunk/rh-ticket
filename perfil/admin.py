from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from django.contrib.auth.models import User 
from .models import Unidade, Funcionario, CentroDeCusto, Acesso, Item, Menu

from auditlog.admin import LogEntryAdmin
from auditlog.models import LogEntry

from .models import CustomLogEntry


@admin.register(CustomLogEntry)
class CustomLogEntryAdmin(LogEntryAdmin, ImportExportModelAdmin):
    list_display = ['timestamp', 'resource_url', 'action', 'msg_short', 'user_url']
    readonly_fields = ['created', 'resource_url', 'action', 'user_url', 'msg']
    list_display_links = None

admin.site.unregister(LogEntry)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['nome']
    list_filter = ['nome']


@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ['nome']
    list_filter = ['nome']


@admin.register(Funcionario)
class FuncionarioAdmin(ImportExportModelAdmin):
    list_display = ['id', 'nome', 're_funcionario']
    list_filter = ['unidade']  
    search_fields = ('re_funcionario', 'nome' )


@admin.register(CentroDeCusto)
class CentroDeCustoAdmin(ImportExportModelAdmin):
    list_display = ['id', 'numero', 'nome', 'responsaveis']
    list_filter = ['numero']


@admin.register(Acesso)
class Acesso(ImportExportModelAdmin):
    pass


@admin.register(Item)
class Item(ImportExportModelAdmin):
    list_display = ['nome']
    list_filter = ['nome']
