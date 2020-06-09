from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from django.contrib.auth.models import User 
from .models import Unidade, Funcionario

# Register your models here.

@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ['nome']
    list_filter = ['nome']


@admin.register(Funcionario)
class FuncionarioAdmin(ImportExportModelAdmin):
    list_display = ['id', 'nome', 're_funcionario']
    list_filter = ['unidade']  

# class UserResource(resources.ModelResource):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'password')

# class UserAdmin(BaseAdmin, ImportExportModelAdmin):
#     resource_class = UserResource

# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)