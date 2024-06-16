from django import forms

class SimulacaoForm(forms.Form):
    media_tempo = forms.FloatField(label='Média de Tempo')
    desvio_padrao_tempo = forms.FloatField(label='Desvio Padrão de Tempo')
    numero_simulacoes = forms.IntegerField(label='Número de Simulações')