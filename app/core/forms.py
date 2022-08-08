from django import forms
from .models import *

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        labels = {
          "fantasia": "Nome Fantasia",
          "cnpj": "CNPJ",
          "telefone": "Telefone",
          "email": "Email",
          "habilitada": "Habilitada",
        }
        fields = "__all__"