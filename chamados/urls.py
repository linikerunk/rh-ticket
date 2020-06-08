from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from .views import (
enviar,
listar,
atualizar_chamado,
funcionario_ajax,
carregar_subcategorias,
carregar_unidade,
)

app_name = "chamados"


urlpatterns = [
    path("", enviar, name="enviar"),
    path("chamados/listar/", listar, name="listar"),
    path("pegar_funcionario/<int:id>/", funcionario_ajax, name="funcionario_ajax"),
    path("carregar_subcategorias/<int:id>/", carregar_subcategorias, name="carregar_subcategorias"),
    path("carregar_unidade/<int:id>/", carregar_unidade, name="carregar_unidade"),
    path("chamados/atualizar_chamado/<int:id>/", atualizar_chamado, name="atualizar_chamado"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
