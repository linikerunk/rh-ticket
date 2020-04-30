from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from .views import login, logout, enviar, listar, atualizar_chamado, funcionario_ajax



app_name = "chamados"


urlpatterns = [
    path("", enviar, name="enviar"),
    path("chamados/enviar/", enviar, name="enviar"),
    path("chamados/listar/", listar, name="listar"),
    path("chamados/pegar_funcionario/<int:id>/", funcionario_ajax, name="funcionario_ajax"),
    path("chamados/atualizar_chamado/<int:id>/", atualizar_chamado, name="atualizar_chamado"),
    path("login/", auth_views.LoginView.as_view(template_name="chamados/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="chamados/logout.html"), name="meu_logout"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
