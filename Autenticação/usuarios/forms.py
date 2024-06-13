from django import forms

class SimulacaoForm(forms.Form):
    media = forms.FloatField(label='Média', initial=3.0, min_value=0.1, max_value=10.0)
    desvio_padrao = forms.FloatField(label='Desvio Padrão', initial=1.0, min_value=0.1, max_value=5.0)
    numero_simulacoes = forms.IntegerField(label='Número de Simulações', initial=1000000, min_value=1000, max_value=10000000)