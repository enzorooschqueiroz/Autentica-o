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
from .forms import DuracaoForm

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
    if request.method == 'POST':
        form = DuracaoForm(request.POST)
        if form.is_valid():
            duracao_desejada = form.cleaned_data['duracao']
            
            # Simulação de Monte Carlo
            sims = 10000000
            A = np.random.uniform(1, 5, sims)
            B = np.random.uniform(2, 6, sims)
            duracao = A + B
            
            # Criando o histograma
            plt.figure(figsize=(11, 5.5))
            plt.hist(duracao, density=True, bins=50)
            plt.axvline(duracao_desejada, color='r', linestyle='dashed', linewidth=1)
            plt.xlabel('Duração')
            plt.ylabel('Densidade')
            plt.title('Simulação de Monte Carlo para Duração')
            plt.grid(True)
            
            # Convertendo o gráfico para imagem base64 para ser exibido no template
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plot_url = 'data:image/png;base64,' + image_base64
            
            # Limpar a figura para evitar sobrecarga de memória
            plt.clf()

            return render(request, 'simulacao.html', {'form': form, 'plot_url': plot_url})
    else:
        form = DuracaoForm()
    return render(request, 'simulacao.html', {'form': form})

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