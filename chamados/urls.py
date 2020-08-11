from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from .views import (
enviar,
listar,
finalizar_chamado,
funcionario_ajax,
carregar_subcategorias,
funcionario_login_ajax,
funcionario_login_reset_ajax,
verificar_senha_ajax
)

app_name = "chamados"


urlpatterns = [
    path("", enviar, name="enviar"),
    path("chamados/listar/", listar, name="listar"),
    path("pegar_funcionario/<int:id>/", funcionario_ajax, name="funcionario_ajax"),
    path("carregar_subcategorias/<int:id>/", carregar_subcategorias, name="carregar_subcategorias"),
    path("funcionario_login/<int:id>/", funcionario_login_ajax, name="funcionario_login_ajax"),
    path("funcionario_login_reset/<int:id>/", funcionario_login_reset_ajax, name="funcionario_login_reset_ajax"),
    path("verifica_senha/<int:id>/", verificar_senha_ajax, name="verificar_senha_ajax"),
    path("chamados/atualizar_chamado/<int:id>/", finalizar_chamado, name="finalizar_chamado"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
