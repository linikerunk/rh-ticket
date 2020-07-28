from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from .views import (
enviar_justificativa_ausencia,
enviar_agendamento_ferias,
)

app_name = "formularios"


urlpatterns = [
    path('formularios/justificativa_ausencia/', enviar_justificativa_ausencia, name='enviar_justificativa_ausencia'),
    path('formularios/agendamento_ferias/', enviar_agendamento_ferias, name='enviar_agendamento_ferias'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
