from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_django, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import MonteCarloContent
from .forms import SimulacaoForm
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def cadastro(request):
    if request.method == "GET":
        return render(request, "cadastro.html")
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

def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login_django(request, user)
            return redirect("plataforma")
        else:
            return HttpResponse("Email ou senha inválidos")

@login_required(login_url="")
def plataforma(request):
    return render(request, "plataforma.html")

def simular_tempo_de_viagem(numero_simulacoes, media_tempo, desvio_padrao_tempo):
    # Simulação de Monte Carlo
    distribuicao_tempo = np.random.normal(media_tempo, desvio_padrao_tempo, numero_simulacoes)
    return distribuicao_tempo


def simulacao_view(request):
    if request.method == 'POST':
        form = SimulacaoForm(request.POST)
        if form.is_valid():
            media_tempo = form.cleaned_data['media_tempo']
            desvio_padrao_tempo = form.cleaned_data['desvio_padrao_tempo']
            numero_simulacoes = form.cleaned_data['numero_simulacoes']

            # Simulação de Monte Carlo para tempo de viagem
            distribuicao_tempo = simular_tempo_de_viagem(numero_simulacoes, media_tempo, desvio_padrao_tempo)
            
            # Criando o histograma
            plt.figure(figsize=(11, 5.5))
            plt.hist(distribuicao_tempo, bins=50, density=True, alpha=0.75)
            plt.axvline(np.mean(distribuicao_tempo), color='r', linestyle='dashed', linewidth=1)
            plt.xlabel('Tempo de Viagem (minutos)')
            plt.ylabel('Densidade')
            plt.title('Simulação de Tempo de Viagem')
            plt.grid(True)
            
            # Convertendo o gráfico para imagem base64 para ser exibido no template
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plot_url = 'data:image/png;base64,' + image_base64
            
            # Limpar a figura para evitar sobrecarga de memória
            plt.clf()
            
            # Renderizar o template com os dados do gráfico
            return render(request, 'simulacao.html', {'form': form, 'plot_url': plot_url})
    
    else:
        form = SimulacaoForm()
    
    return render(request, 'simulacao.html', {'form': form})

@login_required(login_url="")
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

def logout_view(request):
    logout(request)
    return redirect('login')
