from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

# Create your models here.
class homepage(models.Model):
    titulo = models.CharField(max_length=50)
    descricao = models.TextField(max_length=200)
    logo = models.ImageField(upload_to='homepage/')

    def __str__(self):
        return self.titulo
    
class quarto(models.Model):

    tipo_quarto = [
        ("Solteiro", "Solteiro"),
        ("Premium", "Premium"),
        ("Plus", "Plus"),
    ]
    status_status = [
        (1, "Disponivel"),
        (0, "Reservado")
    ]

    num_Quarto = models.IntegerField()
    qtd_Hospedes = models.IntegerField()
    tipo = models.CharField(choices=tipo_quarto)
    valor = models.FloatField(max_length=3)
    descricao = models.TextField(max_length=300)
    status = models.BooleanField(choices=status_status, default=1)
    img = models.ImageField(upload_to='quarto/')


class Colaborador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=20, choices=[
        ('Gerente', 'Gerente'),
        ('Atendente', 'Atendente'),
    ])

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Reserva(models.Model):
    quarto = models.ForeignKey('quarto', on_delete=models.CASCADE, related_name="reservas")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_checkin = models.DateField()
    data_checkout = models.DateField()
    
    def clean(self):
        if self.data_checkin >= self.data_checkout:
            raise ValidationError("Data de check-out deve ser posterior ao check-in.")
        # Verifica conflitos de reserva
        conflitos = Reserva.objects.filter(  
            quarto=self.quarto,
            data_checkin__lt=self.data_checkout,
            data_checkout__gt=self.data_checkin
        ).exclude(id=self.id)
        if conflitos.exists():
            raise ValidationError("Quarto já reservado neste período.")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        self.atualizar_status_quarto()
    
    def delete(self, *args, **kwargs):
        quarto = self.quarto
        super().delete(*args, **kwargs)
        self.atualizar_status_quarto_por_id(quarto.id)
    
    def atualizar_status_quarto(self):
        """Atualiza o status do quarto baseado nas reservas ativas"""
        hoje = timezone.now().date()
        
        # Verifica se há reservas ativas (check-in <= hoje < check-out)
        reservas_ativas = Reserva.objects.filter(
            quarto=self.quarto,
            data_checkin__lte=hoje,
            data_checkout__gt=hoje
        ).exists()
        
        # Atualiza o status: False se há reserva ativa, True se disponível
        self.quarto.status = not reservas_ativas
        self.quarto.save()
    
    @staticmethod
    def atualizar_status_quarto_por_id(quarto_id):
        """Método estático para atualizar status quando reserva é deletada"""
        from .models import quarto  # Ajuste o import conforme sua estrutura
        try:
            quarto_obj = quarto.objects.get(id=quarto_id)
            hoje = timezone.now().date()
            
            reservas_ativas = Reserva.objects.filter(
                quarto=quarto_obj,
                data_checkin__lte=hoje,
                data_checkout__gt=hoje
            ).exists()
            
            quarto_obj.status = not reservas_ativas
            quarto_obj.save()
        except quarto.DoesNotExist:
            pass
    
    def __str__(self):
        return f"Reserva {self.quarto.num_Quarto} - {self.usuario.username}"