from django import forms
from django.utils.translation import gettext as _
from django.utils.translation import gettext
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from .models import *
from core.models import Empresa

class DateInput(forms.DateInput):
    input_type = 'date'

class ItemHortifrutiForm(forms.ModelForm):
    class Meta:
        model = ItemHortifruti
        fields = "__all__"
        exclude = ['data_cadastro','data_modificado']

class AgendaHortifrutiForm(forms.ModelForm):
     class Meta:
        model = AgendaHortifruti
        fields = "__all__"
        widgets = {
            'data_final': DateInput(),
        }
        exclude = ['data_cadastro']

class QuantidadeItemHortifrutiRequisitadoForm(forms.ModelForm):

    def clean_quantidadeRequisitada(self):
        quantidadeRequisitada = self.cleaned_data['quantidadeRequisitada']
        if quantidadeRequisitada == '':
            quantidadeRequisitada = 0
        return quantidadeRequisitada

    def __init__(self, *args, **kwargs):
        super(QuantidadeItemHortifrutiRequisitadoForm, self).__init__(*args, **kwargs)
        if self.instance.descricao.strip():
            self.fields['quantidadeRequisitada'].label = self.instance.descricao

    class Meta:
        model = QuantidadeItemHortifruti
        fields = "__all__"
        exclude = ['pedido', 'item', 'descricao', 'habilitado', 'quantidadeAdquirida']

class QuantidadeItemHortifrutiAdiquiridoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(QuantidadeItemHortifrutiAdiquiridoForm, self).__init__(*args, **kwargs)
        if self.instance.descricao.strip():
            self.fields['quantidadeAdquirida'].label = self.instance.pedido.empresa.descricao
        self.fields['quantidadeRequisitada'].widget.attrs['readonly'] = True

    def clean_quantidadeAdquirida(self):
        quantidadeAdquirida = self.cleaned_data['quantidadeAdquirida']
        if quantidadeAdquirida == '':
            print(quantidadeAdquirida)
            quantidadeAdquirida = 0
        return quantidadeAdquirida

    class Meta:
        model = QuantidadeItemHortifruti
        fields = "__all__"
        exclude = ['pedido', 'item', 'descricao', 'habilitado']

PedidoHortifrutiRequisitadoFormset = forms.inlineformset_factory(
PedidoHortifruti,
QuantidadeItemHortifruti,
form=QuantidadeItemHortifrutiRequisitadoForm,
extra=0,
can_delete=False,
)



