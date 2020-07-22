from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from perfil.forms import CustomAuthenticationForm

from .views import (
Login,
# ResetaSenha,
ResetaSenha,
logout,
perfil,
atualizar_perfil,
set_password,
)

app_name = "perfil"

urlpatterns = [
    path("perfil/perfil/", perfil, name="perfil"),
    path("perfil/atualizar_perfil/<int:id>/", atualizar_perfil, name="atualizar_perfil"),
    path('perfil/set_password/', set_password, name="set_password"),
    path("login/", Login.as_view(), name="login", kwargs={"authentication_form":CustomAuthenticationForm}),
    path("logout/", auth_views.LogoutView.as_view(template_name="perfil/logout.html"), name="meu_logout"),
    path("resetar_senha/", ResetaSenha, name="resetar_senha"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
