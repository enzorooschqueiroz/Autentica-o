from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponse

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
        return HttpResponse("Usuário cadastrado com sucesso")

        return HttpResponse(username)
    
    


def login (request):
    if request.method == "GET":
        return render (request, "login.html")
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            return HttpResponse("Autenticado!!!")
        else:
            return HttpResponse("Email ou senha inválidos")
