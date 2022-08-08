from django import forms
from django.utils.translation import gettext as _
from django.utils.translation import gettext
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from .models import *
from core.models import Empresa

class DateInput(forms.DateInput):
    input_type = 'date'

class ItemAbastecimentoForm(forms.ModelForm):
    class Meta:
        model = ItemAbastecimento
        fields = "__all__"
        exclude = ['data_cadastro','data_modificado']

class AgendaAbastecimentoForm(forms.ModelForm):
     class Meta:
        model = AgendaAbastecimento
        fields = "__all__"
        widgets = {
            'data_final': DateInput(),
        }
        exclude = ['data_cadastro']

class QuantidadeItemAbastecimentoRequisitadoForm(forms.ModelForm):

    def clean_quantidadeAcougue(self):
        quantidadeAcougue = self.cleaned_data['quantidadeAcougue']
        if quantidadeAcougue == '':
            quantidadeAcougue = 0
        return quantidadeAcougue

    def clean_quantidadeLoja(self):
        quantidadeLoja = self.cleaned_data['quantidadeLoja']
        if quantidadeLoja == '':
            quantidadeLoja = 0
        return quantidadeLoja

    def clean_quantidadePadaria(self):
        quantidadePadaria = self.cleaned_data['quantidadePadaria']
        if quantidadePadaria == '':
            quantidadePadaria = 0
        return quantidadePadaria

    def clean_quantidadeVerdura(self):
        quantidadeVerdura = self.cleaned_data['quantidadeVerdura']
        if quantidadeVerdura == '':
            quantidadeVerdura = 0
        return quantidadeVerdura

    def clean_quantidadeRequisitada(self):
        quantidadeRequisitada = self.cleaned_data['quantidadeRequisitada']
        quantidadeAcougue = self.cleaned_data['quantidadeAcougue']
        quantidadeLoja = self.cleaned_data['quantidadeLoja']
        quantidadePadaria = self.cleaned_data['quantidadePadaria']
        quantidadeVerdura = self.cleaned_data['quantidadeVerdura']
        quantidadeRequisitada = quantidadeAcougue + quantidadeLoja + quantidadePadaria + quantidadeVerdura
        return quantidadeRequisitada


    def __init__(self, *args, **kwargs):
        super(QuantidadeItemAbastecimentoRequisitadoForm, self).__init__(*args, **kwargs)
        if self.instance.descricao.strip():
            self.fields['quantidadeRequisitada'].label = self.instance.descricao
        if self.instance.habilitado == 'N':
            self.fields['quantidadeRequisitada'].widget.attrs['readonly'] = True
            self.initial['quantidadeRequisitada'] = 0
        if self.instance.acougue == 'N':
            self.fields['quantidadeAcougue'].widget.attrs['readonly'] = True
            self.initial['quantidadeAcougue'] = 0
        if self.instance.loja == 'N':
            self.fields['quantidadeLoja'].widget.attrs['readonly'] = True
            self.initial['quantidadeLoja'] = 0
        if self.instance.padaria == 'N':
            self.fields['quantidadePadaria'].widget.attrs['readonly'] = True
            self.initial['quantidadePadaria'] = 0
        if self.instance.verdura == 'N':
            self.fields['quantidadeVerdura'].widget.attrs['readonly'] = True
            self.initial['quantidadeVerdura'] = 0

    class Meta:
        model = QuantidadeItemAbastecimento
        fields = "__all__"
        exclude = ['pedido', 'descricao', 'habilitado', 'quantidadeAdquirida', 'acougue', 'loja', 'padaria', 'verdura']

class QuantidadeItemAbastecimentoAdiquiridoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(QuantidadeItemAbastecimentoAdiquiridoForm, self).__init__(*args, **kwargs)
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
        model = QuantidadeItemAbastecimento
        fields = "__all__"
        exclude = ['pedido', 'item', 'descricao', 'habilitado', 'acougue', 'loja', 'padaria', 'verdura', 'quantidadePadaria', 'quantidadeAcougue', 'quantidadeLoja', 'quantidadeVerdura']

PedidoAbastecimentoFormset = forms.inlineformset_factory(
PedidoAbastecimento,
QuantidadeItemAbastecimento,
form=QuantidadeItemAbastecimentoRequisitadoForm,
extra=0,
can_delete=False,
)

class CategoriaAbastecimentoForm(forms.ModelForm):
    class Meta:
        model = CategoriaAbastecimento
        fields = "__all__"
