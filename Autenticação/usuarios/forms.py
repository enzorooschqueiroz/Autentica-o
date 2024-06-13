from django import forms

class DuracaoForm(forms.Form):
    duracao = forms.FloatField(label='Duração desejada', min_value=0.1, max_value=20.0)