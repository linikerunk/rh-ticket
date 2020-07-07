from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from .views import (
enviar_justificativa_ausencia,
)

app_name = "formularios"


urlpatterns = [
    path('formularios/justificativa_ausencia/', enviar_justificativa_ausencia, name='enviar_justificativa_ausencia'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
