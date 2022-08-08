from django.forms import NullBooleanField, inlineformset_factory, modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User

#Geral
def home(request):
    return render(request, 'home.html')

# Empresa

class listaEmpresa(ListView):
    model = Empresa
    template_name = 'listaEmpresa.html'
    context_object_name = 'empresa_list'

    def get_queryset(self):
        queryset = super(listaEmpresa, self).get_queryset().order_by('descricao')
        data = self.request.GET
        search = data.get('search')
        if search:
            queryset = queryset.filter(
                Q(descricao__icontains=search) |
                Q(cnpj__icontains=search) |
                Q(email__icontains=search) |
                Q(telefone__icontains=search) |
                Q(habilitada__icontains=search)
            ).order_by('descricao')
        return queryset


def cadastroEmpresa(request):
    form = EmpresaForm()
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Empresa')

    return render(request, 'cadastro.html', {'form': form})

class detalhesEmpresa(DetailView):
    model = Empresa
    template_name ='detalhesEmpresa.html'

def editarEmpresa(request, pk, template_name='cadastro.html'):
    empresas = get_object_or_404(Empresa, pk=pk)
    form = EmpresaForm(request.POST or None, instance=empresas)
    if form.is_valid():
        form.save()
        return redirect('Empresa')
    return render(request, template_name, {'form': form})


def excluirEmpresa(request, pk, template_name='confirm_delete.html'):
    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == 'POST':
        empresa.delete()
        return redirect('Empresa')
    return render(request, template_name, {'object': empresa})

