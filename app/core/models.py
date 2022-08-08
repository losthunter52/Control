from django.db import models
from django.contrib.auth.models import User

# Geral

BOOL_CHOICES = (
    ('S', 'Sim'),
    ('N', 'Não')
)

class Empresa(models.Model):
    descricao = models.CharField(max_length=32, unique = True)
    cnpj = models.CharField(max_length=32, unique = True)
    telefone = models.CharField(max_length=32)
    email = models.EmailField('email')
    usuarios = models.ManyToManyField(User)
    habilitada = models.CharField(choices=BOOL_CHOICES, max_length=4)

    def __str__(self):
        return self.descricao

    
    