from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Unidade, Funcionario, Perfil

# Register your models here.

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'unidade', 'funcionario']
    list_filter = ['usuario']

@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ['nome']
    list_filter = ['nome']


@admin.register(Funcionario)
class FuncionarioAdmin(ImportExportModelAdmin):
    list_display = ['id', 'nome', 're_funcionario']
    list_filter = ['funcionario__unidade']  
