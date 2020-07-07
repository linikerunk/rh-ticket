from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import JustificativaAusencia

# Register your models here.

@admin.register(JustificativaAusencia)
class JustificativaAusencia(ImportExportModelAdmin):
    pass
