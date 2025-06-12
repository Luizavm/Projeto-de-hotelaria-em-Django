from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import quarto
from .models import *
from .forms import *

# Create your views here.
def Homepage(request):
    context = {}
    dados_home = homepage.objects.all()
    context['dados_home'] = dados_home
    return render(request, 'homepage.html', context)

def Login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            context = {
                "alerta" : "Usuário ou Senha Invalida"
            }
            return render(request, 'Login.html', context)

    else:
        return render(request, 'Login.html')
    
def addQuarto(request):
    if request.method == 'POST':
        form = quartoForms(request.POST, request.FILES)        
        if form.is_valid():
            form.save()
            return redirect('addQuarto')
    else:    
        form = quartoForms()
    
    context = {'form': form}
    return render(request, 'addQuartos.html', context)

@login_required
def addColaborador(request):
   if request.method == 'POST':
       form = ColaboradorForm(request.POST)
       if form.is_valid():
           cd = form.cleaned_data
           User.objects.create_user(username=cd['username'], password=cd['password'])
           return redirect('/')
   else:
       form = ColaboradorForm()
   return render(request, 'addColaborador.html', {'form': form})

@login_required
def quarto_lista(request):
   lista_quartos = quarto.objects.all()
   return render(request, 'quarto.html', {'lista_quartos': lista_quartos})

@login_required
def editar_quarto(request, quarto_id):
   quarto = get_object_or_404(quarto, id=quarto_id)
   
   if request.method == 'POST':
       form = quartoForms(request.POST, request.FILES, instance=quarto)
       if form.is_valid():
           form.save()
           return redirect('quarto_lista')
   else:
       form = quartoForms(instance=quarto)
   return render(request, 'editar_quarto.html', {'form': form, 'quarto': quarto})

@login_required
def reserva(request):
   if request.method == 'POST':
       form = ReservaForm(request.POST)
       if form.is_valid():
           cd = form.cleaned_data
           quarto_selecionado = get_object_or_404(quarto, num_Quarto=cd['num_quarto'])
           
           Reserva.objects.create(
               usuario=request.user,
               tipo_quarto=quarto_selecionado.tipo,
               data_checkin=cd['data_checkin'],
               data_checkout=cd['data_checkout'],
               quarto=quarto_selecionado
           )
           
           quarto_selecionado.status = False
           quarto_selecionado.save()
           return redirect('reservas')
   else:
       form = ReservaForm()
   return render(request, 'reserva.html', {'form': form})

def Sair(request):
    logout(request)
    return redirect ('homepage')