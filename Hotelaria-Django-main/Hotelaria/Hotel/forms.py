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

class EditQuartoForm(forms.ModelForm):
    class Meta:
        model = quarto
        fields = ['num_Quarto', 'qtd_Hospedes', 'tipo', 'valor', 'descricao', 'status', 'img']
        
        widgets = {
            'num_Quarto': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Número do quarto',
                'min': '1'
            }),
            'qtd_Hospedes': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Quantidade de hóspedes',
                'min': '1'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Valor da diária',
                'step': '0.01',
                'min': '0'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Descrição do quarto',
                'rows': 4,
                'maxlength': '300'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'img': forms.FileInput(attrs={
                'class': 'form-file',
                'accept': 'image/*'
            })
        }
        
        labels = {
            'num_Quarto': 'Número do Quarto',
            'qtd_Hospedes': 'Quantidade de Hóspedes',
            'tipo': 'Tipo do Quarto',
            'valor': 'Valor (R$)',
            'descricao': 'Descrição',
            'status': 'Status',
            'img': 'Imagem do Quarto'
        }