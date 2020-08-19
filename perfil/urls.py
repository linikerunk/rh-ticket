from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from perfil.forms import CustomAuthenticationForm

from .views import (
Login,
reset_password,
logout,
perfil,
espelho,
atualizar_perfil,
verifica_admissao,
set_password,
unidade_admin,
)

app_name = "perfil"

urlpatterns = [
    path("perfil/perfil/", perfil, name="perfil"),
    path("perfil/espelhos/", espelho, name="espelho"),
    path("perfil/atualizar_perfil/<int:id>/", atualizar_perfil, name="atualizar_perfil"),
    path('perfil/set_password/', set_password, name="set_password"),
    path("login/", Login.as_view(), name="login", kwargs={"authentication_form":CustomAuthenticationForm}),
    path("logout/", auth_views.LogoutView.as_view(template_name="perfil/logout.html"), name="meu_logout"),
    path("resetar_senha/<int:id>/", reset_password, name="reset_password"),
    path("verifica_admissao/", verifica_admissao, name="verifica_admissao"),
    path("perfil/unidade_admin/", unidade_admin, name="unidade_admin"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
