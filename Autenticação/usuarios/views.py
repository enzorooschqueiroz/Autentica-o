from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse

def cadastro (request):
    if request.method == "GET":
        return render (request, "cadastro.html")
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.get(username=username)

        if user:
            return HttpResponse("Já existe um usuário com esse username")

        return HttpResponse(username)
    
    


def login (request):
    return render (request, "login.html")