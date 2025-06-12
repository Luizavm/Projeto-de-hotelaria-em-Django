from django.contrib.auth.models import User, Group
from django import forms
from .models import quarto

class quartoForms(forms.ModelForm):
    class Meta:
        model = quarto
        fields = ['num_Quarto','qtd_Hospedes','tipo','valor','descricao','status', 'img']

class ColaboradorForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    cargo = forms.ChoiceField(choices=[('Atendente', 'Atendente')])

class ReservaForm(forms.Form):
    num_quarto = forms.IntegerField(
        label="Número do Quarto",
        min_value=1,
        max_value=300,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Ex: 101',
            'class': 'form-control'
        })
    )
    data_checkin = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    data_checkout = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

