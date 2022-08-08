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
    ('Mensal Fornecedores', 'Mensal Fornecedores'),
    ('Mensal Armazenado', 'Mensal Armazenado'),
    ('Quinzenal Alimentos', 'Quinzenal Alimentos'),
    ('Pedidos Itens Açougue', 'Pedidos Itens Açougue'),
    ('Pedidos Linea Verde', 'Pedidos Linea Verde')
)

SN_CHOICES = (
    ('S', 'Sim'),
    ('N', 'Nao')
)

class CategoriaAbastecimento(models.Model):
    descricao = models.CharField(max_length=32)

    def __str__(self):
        return self.descricao

class ItemAbastecimento(models.Model):
    codigo = models.CharField(max_length=8, unique = True)
    descricao = models.CharField(max_length=64, unique = True)
    empresas = models.ManyToManyField(Empresa)
    situacao = models.CharField(max_length=32, default='  --//--  ')
    acougue = models.CharField(choices=SN_CHOICES, max_length=2, default='N')
    loja = models.CharField(choices=SN_CHOICES, max_length=2, default='N')
    padaria = models.CharField(choices=SN_CHOICES, max_length=2, default='N')
    verdura = models.CharField(choices=SN_CHOICES, max_length=2, default='N')
    categoria = models.ForeignKey(CategoriaAbastecimento, on_delete=models.CASCADE)
    tipo = models.CharField(choices=PEDIDOS_CHOICES, max_length=32)
    data_cadastro = models.DateField(auto_now=True, editable=False)
    data_modificado = models.DateField(auto_now=True,)

    def __str__(self):
        return self.descricao

class AgendaAbastecimento(models.Model):
    descricao = models.CharField(max_length=96)
    tipo = models.CharField(choices=PEDIDOS_CHOICES, max_length=32)
    data_cadastro = models.DateField(auto_now=True,)
    data_final = models.DateField()

    @property
    def aberto(self):  
        return self.data_final >= date.today()

class PedidoAbastecimento(models.Model):
    master = models.ForeignKey(AgendaAbastecimento, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=96, default='')

    def __str__(self):
        return self.master.descricao
    
    @property
    def aberto(self):  
        return self.master.data_final >= date.today()

class QuantidadeItemAbastecimento(models.Model):
    item = models.ForeignKey(ItemAbastecimento, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=96, default='')
    pedido = models.ForeignKey(PedidoAbastecimento, on_delete=models.CASCADE)
    habilitado = models.CharField(max_length=2, default='')
    acougue = models.CharField(choices=SN_CHOICES, max_length=2, default='N')
    loja = models.CharField(choices=SN_CHOICES, max_length=2, default='N')
    padaria = models.CharField(choices=SN_CHOICES, max_length=2, default='N')
    verdura = models.CharField(choices=SN_CHOICES, max_length=2, default='N')
    quantidadeAcougue = models.PositiveIntegerField(default=0)
    quantidadeLoja = models.PositiveIntegerField(default=0)
    quantidadePadaria = models.PositiveIntegerField(default=0)
    quantidadeVerdura = models.PositiveIntegerField(default=0)
    quantidadeRequisitada = models.PositiveIntegerField(default=0)
    quantidadeAdquirida = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.item.descricao   

    def totalizar(self):  
        aux =  quantidadeLoja + quantidadePadaria + quantidadePadaria + quantidadeVerdura
        return aux
