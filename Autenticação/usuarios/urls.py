from django.urls import path
from django.contrib import admin
from .views import cadastro, login, plataforma, logout_view

urlpatterns = [
    path("cadastro/", cadastro, name="cadastro"),
    path("login/", login, name="login"), 
    path("plataforma/", plataforma, name="plataforma"),
    path("logout/",  logout_view, name="logout")


]