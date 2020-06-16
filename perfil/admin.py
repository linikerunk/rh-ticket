from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from django.contrib.auth.models import User 
from .models import Unidade, Funcionario, RegistroAutorizacao

# Register your models here.

@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ['nome']
    list_filter = ['nome']


@admin.register(Funcionario)
class FuncionarioAdmin(ImportExportModelAdmin):
    list_display = ['id', 'nome', 're_funcionario']
    list_filter = ['unidade']  


@admin.register(RegistroAutorizacao)
class RegistroAutorizacaoAdmin(ImportExportModelAdmin):
    list_display = ['funcionario', 'get_funcionario_id', 'get_user', 'data_atualizacao', 'acao', ]
    list_filter = ['funcionario']
    search_fields = ['funcionario__re_funcionario']

    def get_user(self, obj):
        return obj.funcionario.usuario
    get_user.short_description = 'Usuário'
    get_user.admin_order_field = 'funcionario__usuario'
    
    def get_funcionario_id(self, obj):
        return obj.funcionario.id
    get_funcionario_id.short_description = 'Id'
    get_funcionario_id.admin_order_field = 'funcionario__id'

# class UserResource(resources.ModelResource):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'password')

# class UserAdmin(BaseAdmin, ImportExportModelAdmin):
#     resource_class = UserResource

# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)