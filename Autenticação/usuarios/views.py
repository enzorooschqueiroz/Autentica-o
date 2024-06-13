from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import logout
from .models import MonteCarloContent
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def cadastro (request):
    if request.method == "GET":
        return render (request, "cadastro.html")
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(username=username).first()

        if user:
            return HttpResponse("Já existe um usuário com esse username")
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        user = authenticate(username=username, password=password)
        if user:
            login_django(request, user)
            return redirect("plataforma")
        else:
            return HttpResponse("Erro ao autenticar o usuário após o cadastro")
    

def login (request):
    if request.method == "GET":
        return render (request, "login.html")
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login_django(request, user)
            return render (request, "plataforma.html")
        else:
            return HttpResponse("Email ou senha inválidos")

@login_required(login_url="")
def plataforma(request):
    if request.user.is_authenticated:
        return render (request, "plataforma.html")
    else:
        return HttpResponse("Você deve estar registrado...")
    
def logout_view(request):
    logout(request)
    return redirect('login') 

def simulacao_view(request):
    if request.user.is_authenticated:
        return render (request, "simulacao.html")
    else:
        return HttpResponse("Você deve estar registrado...")

def equipe_view(request):
    equipe_members = [
        'Enzo Queiroz',
        'Gabriel Barbosa',
        'Paulo Araújo',
        'Rafael Máximo',
        'Rodrigo Bragagnolo'
    ]
    context = {
        'equipe_members': equipe_members
    }
    return render(request, 'equipe.html', context)

def home(request):
    montecarlo_contents = MonteCarloContent.objects.all()
    return render(request, 'home.html', {'montecarlo_contents': montecarlo_contents})