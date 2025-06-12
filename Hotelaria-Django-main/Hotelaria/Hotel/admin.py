from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(homepage)
admin.site.register(quarto)
admin.site.register(Colaborador)
admin.site.register(Reserva)

def has_delete_permission(self, request, obj=None):
    return request.user.is_superuser