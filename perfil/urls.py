from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from .views import perfil

app_name = "perfil"

urlpatterns = [
    path("perfil/perfil/", perfil, name="perfil"),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
