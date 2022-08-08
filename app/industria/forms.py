from django import forms
from django.utils.translation import gettext as _
from django.utils.translation import gettext
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from .models import *
from core.models import Empresa

class DateInput(forms.DateInput):
    input_type = 'date'

class ItemIndustriaForm(forms.ModelForm):
    class Meta:
        model = ItemIndustria
        fields = "__all__"
        exclude = ['data_cadastro','data_modificado']

class AgendaIndustriaForm(forms.ModelForm):
     class Meta:
        model = AgendaIndustria
        fields = "__all__"
        widgets = {
            'data_final': DateInput(),
        }
        exclude = ['data_cadastro']

class QuantidadeItemIndustriaForm(forms.ModelForm):

    def clean_quantidade(self):
        quantidade = self.cleaned_data['quantidade']
        if quantidade == '':
            quantidade = 0
        return quantidade

    def __init__(self, *args, **kwargs):
        super(QuantidadeItemIndustriaForm, self).__init__(*args, **kwargs)
        if self.instance.descricao.strip():
            self.fields['quantidade'].label = self.instance.descricao
        if self.instance.habilitado == 'N':
            self.fields['quantidade'].widget.attrs['readonly'] = True
            self.initial['quantidade'] = 0.00

    class Meta:
        model = QuantidadeItemIndustria
        fields = "__all__"
        exclude = ['pedido', 'item', 'descricao', 'habilitado']

PedidoIndustriaFormset = forms.inlineformset_factory(
PedidoIndustria,
QuantidadeItemIndustria,
form=QuantidadeItemIndustriaForm,
extra=0,
can_delete=False,
)

class CategoriaIndustriaForm(forms.ModelForm):
    class Meta:
        model = CategoriaIndustria
        fields = "__all__"
