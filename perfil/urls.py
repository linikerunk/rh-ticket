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
create_unidade_admin,
delete_unidade_admin,
delete_user_group,
update_unidade_admin,
update_email_admin,
update_menu_admin,
update_grupo_admin,
update_categoria_admin,
add_responsavel_categoria,
remove_responsavel_categoria,
)

app_name = "perfil"

urlpatterns = [
    path("perfil/perfil/", perfil, name="perfil"),
    path("perfil/espelhos/", espelho, name="espelho"),
    path("perfil/atualizar_perfil/<int:id>/", atualizar_perfil,
    name="atualizar_perfil"),
    path('perfil/set_password/', set_password, name="set_password"),
    path("login/", Login.as_view(), name="login",
    kwargs={"authentication_form":CustomAuthenticationForm}),
    path("logout/",
    auth_views.LogoutView.as_view(template_name="perfil/logout.html"),
    name="meu_logout"),
    path("resetar_senha/", reset_password, name="reset_password"),
    path("verifica_admissao/", verifica_admissao, name="verifica_admissao"),
    path("perfil/unidade_admin/", unidade_admin, name="unidade_admin"),
    path("perfil/create_unidade_admin/", create_unidade_admin,
    name="create_unidade_admin"),
    path("perfil/update_unidade_admin/<int:id>/", update_unidade_admin,
    name="update_unidade_admin"),
    path("perfil/delete_unidade_admin/<int:id>/", delete_unidade_admin,
    name="delete_unidade_admin"),
    path("perfil/delete_user_group/<int:id>/", delete_user_group,
    name="delete_user_group"),
    path("perfil/update_email_admin/<int:id>/", update_email_admin,
    name="update_email_admin"),
    path("perfil/update_menu_admin/<int:id>/", update_menu_admin,
    name="update_menu_admin"),
    path("perfil/update_grupo_admin/<int:id>/", update_grupo_admin,
    name="update_grupo_admin"),
    path("perfil/update_categoria_admin/<int:id>/", update_categoria_admin,
    name="update_categoria_admin"),
    path("perfil/add_responsavel_categoria/<int:id>/", add_responsavel_categoria,
    name="add_responsavel_categoria"),
    path("perfil/remove_responsavel_categoria/<int:id>/",
    remove_responsavel_categoria, name="remove_responsavel_categoria"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
