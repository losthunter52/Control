from decimal import Decimal
from email.policy import default
from django.forms import BooleanField
from django.utils import timezone 
from django.db import models
from datetime import date
from django.core.validators import MinValueValidator
from django.utils.translation import gettext as _
from django.conf import settings
from core.models import Empresa
# Create your models here.

PEDIDOS_CHOICES = (
    ('Segunda', 'Segunda'),
    ('Quarta', 'Quarta'),
    ('Sexta', 'Sexta')
)

class ItemHortifruti(models.Model):
    codigo = models.CharField(max_length=8, unique = True)
    descricao = models.CharField(max_length=32, unique = True)

    def __str__(self):
        return self.descricao

class AgendaHortifruti(models.Model):
    descricao = models.CharField(max_length=96)
    tipo = models.CharField(choices=PEDIDOS_CHOICES, max_length=32)
    data_final = models.DateField()

    @property
    def aberto(self):  
        return self.data_final >= date.today()

class PedidoHortifruti(models.Model):
    master = models.ForeignKey(AgendaHortifruti, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=96, default='')

    def __str__(self):
        return self.master.descricao
    
    @property
    def aberto(self):  
        return self.master.data_final >= date.today()

class QuantidadeItemHortifruti(models.Model):
    item = models.ForeignKey(ItemHortifruti, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=96, default='')
    pedido = models.ForeignKey(PedidoHortifruti, on_delete=models.CASCADE)
    quantidadeRequisitada = models.PositiveIntegerField(default=0)
    quantidadeAdquirida = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.item.descricao   
