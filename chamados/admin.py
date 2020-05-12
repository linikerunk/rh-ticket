# -*- coding: utf-8 -*-

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Ticket
from perfil.models import Perfil, Funcionario
# Register your models here.

@admin.register(Ticket)
class TicketAdmin(ImportExportModelAdmin):
    list_display = ['id', 'funcionario', 'texto', 'data', 'finalizado']
    list_filter = ['funcionario__perfil__unidade']
