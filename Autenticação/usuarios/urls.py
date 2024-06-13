from django.urls import path
from django.contrib import admin
from .views import cadastro, login, plataforma, logout_view, simulacao_view, equipe_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("cadastro/", cadastro, name="cadastro"),
    path("", login, name="login"), 
    path("plataforma/", plataforma, name="plataforma"),
    path("logout/",  logout_view, name="logout"),
    path('simulacao/',simulacao_view, name='simulacao'),
    path('equipe/', equipe_view, name='equipe'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)