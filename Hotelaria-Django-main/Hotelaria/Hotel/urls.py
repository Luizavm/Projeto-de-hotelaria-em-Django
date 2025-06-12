from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Homepage, name='homepage'),
    path('login', views.Login, name='login'),
    path('logout', views.Sair, name='logout'),
    path('addQuarto', views.addQuarto, name="addQuarto"),
    path('quarto_lista', views.quarto_lista, name='quarto_lista'),
    path('addColaborador', views.addColaborador, name='addcolaborador'),
    path('reserva', views.reserva, name='reserva'),
]