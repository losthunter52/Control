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
    ('0', 'Segunda'),
    ('1', 'Terça'),
    ('2', 'Quarta'),
    ('3', 'Quinta'),
    ('4', 'Sexta')
)

class CategoriaIndustria(models.Model):
    descricao = models.CharField(max_length=32)

    def __str__(self):
        return self.descricao

class ItemIndustria(models.Model):
    codigo = models.CharField(max_length=8, unique = True)
    descricao = models.CharField(max_length=32, unique = True)
    empresas = models.ManyToManyField(Empresa)
    categoria = models.ForeignKey(CategoriaIndustria, on_delete=models.CASCADE)
    tipo = models.CharField(choices=PEDIDOS_CHOICES, max_length=32)
    data_cadastro = models.DateField(auto_now=True, editable=False)
    data_modificado = models.DateField(auto_now=True,)

    def __str__(self):
        return self.descricao

class AgendaIndustria(models.Model):
    descricao = models.CharField(max_length=96)
    tipo = models.CharField(choices=PEDIDOS_CHOICES, max_length=32)
    data_cadastro = models.DateField(auto_now=True,)
    data_final = models.DateField()

class PedidoIndustria(models.Model):
    master = models.ForeignKey(AgendaIndustria, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=96, default='')

    def __str__(self):
        return self.master.descricao
    
    @property
    def aberto(self):  
        return self.master.data_final >= date.today()

class QuantidadeItemIndustria(models.Model):
    item = models.ForeignKey(ItemIndustria, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=96, default='')
    pedido = models.ForeignKey(PedidoIndustria, on_delete=models.CASCADE)
    quantidade = models.DecimalField(decimal_places=2, max_digits=5, validators=[MinValueValidator(Decimal('0.00'))])
    habilitado = models.CharField(max_length=2, default='')

    def __str__(self):
        return self.item.descricao   

