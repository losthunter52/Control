from django.forms import NullBooleanField, inlineformset_factory, modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from .models import *
from .forms import *
from django.db.models import Q
from django.db.models import Sum, Value, CharField
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User


# Create your views here.
#Geral


#---------------------------------------------------------------------------------------------------------

#ItemIndustria----------------------------------------------------------------------------------------

class listaItemIndustria(ListView):
    model = ItemIndustria
    template_name = 'industria/listaItem.html'
    context_object_name = 'item_list'

    def get_queryset(self):
        queryset = super(listaItemIndustria, self).get_queryset().order_by('descricao')
        data = self.request.GET
        search = data.get('search')
        if search:
            queryset = queryset.filter(
                Q(codigo__icontains=search) |
                Q(descricao__icontains=search) |
                Q(tipo__icontains=search) 
            ).order_by('descricao')
        return queryset

def cadastroItemIndustria(request):
    form = ItemIndustriaForm()
    if request.method == 'POST':
        form = ItemIndustriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ItemIndustria')

    return render(request, 'industria/cadastro.html', {'form': form})


def editarItemIndustria(request, pk, template_name='industria/cadastro.html'):
    itens = get_object_or_404(ItemIndustria, pk=pk)
    form = ItemIndustriaForm(request.POST or None, instance=itens)
    if form.is_valid():
        form.save()
        return redirect('ItemIndustria')
    return render(request, template_name, {'form': form})


def excluirItemIndustria(request, pk, template_name='industria/confirm_delete.html'):
    item = get_object_or_404(ItemIndustria, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('ItemIndustria')
    return render(request, template_name, {'object': item})

#---------------------------------------------------------------------------------------------------------

#CategoriaIndustria-----------------------------------------------------------------------------------

class listaCategoriaIndustria(ListView):
    model = CategoriaIndustria
    template_name = 'industria/listaCategoria.html'
    context_object_name = 'categoriaIndustria_list'

    def get_queryset(self):
        queryset = super(listaCategoriaIndustria, self).get_queryset().order_by('descricao')
        data = self.request.GET
        search = data.get('search')
        if search:
            queryset = queryset.filter(
                Q(descricao__icontains=search) 
            ).order_by('descricao')
        return queryset


def cadastroCategoriaIndustria(request):
    form = CategoriaIndustriaForm()
    if request.method == 'POST':
        form = CategoriaIndustriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('CategoriaIndustria')

    return render(request, 'industria/cadastro.html', {'form': form})


def editarCategoriaIndustria(request, pk, template_name='industria/cadastro.html'):
    categoriaIndustria = get_object_or_404(CategoriaIndustria, pk=pk)
    form = CategoriaIndustriaForm(request.POST or None, instance=categoriaIndustria)
    if form.is_valid():
        form.save()
        return redirect('CategoriaIndustria')
    return render(request, template_name, {'form': form})


def excluirCategoriaIndustria(request, pk, template_name='industria/confirm_delete.html'):
    categoriaIndustria = get_object_or_404(CategoriaIndustria, pk=pk)
    if request.method == 'POST':
        categoriaIndustria.delete()
        return redirect('CategoriaIndustria')
    return render(request, template_name, {'object': categoriaIndustria})

#---------------------------------------------------------------------------------------------------------

#AgendaIndustria--------------------------------------------------------------------------------------

class listaAgendaIndustria(ListView):
    model = AgendaIndustria
    template_name = 'industria/listaAgenda.html'
    context_object_name = 'agendaIndustria_list'

    def get_queryset(self):
        queryset = super(listaAgendaIndustria, self).get_queryset().order_by('-data_final')
        data = self.request.GET
        search = data.get('search')
        if search:
            queryset = queryset.filter(
                Q(descricao__icontains=search) |
                Q(tipo__icontains=search) |
                Q(data_cadastro__icontains=search) |
                Q(data_final__icontains=search) 
            ).order_by('-data_final')
        return queryset

def cadastroAgendaIndustria(request):
    form = AgendaIndustriaForm()
    empresas = Empresa.objects.filter(habilitada="S")
    if request.method == 'POST':
        form = AgendaIndustriaForm(request.POST)
        if form.is_valid():
            agenda = form.save()
            for empresa in empresas:
                itens = ItemIndustria.objects.filter(tipo=agenda.tipo)
                if itens.exists():
                    pedido = PedidoIndustria.objects.create(master=agenda, empresa=empresa)
                    for item in itens:
                        if empresa in item.empresas.all():
                            QuantidadeItemIndustria.objects.create(item=item, descricao=item.descricao, pedido=pedido, quantidade=0, habilitado='S')
                        else:
                            QuantidadeItemIndustria.objects.create(item=item, descricao=item.descricao, pedido=pedido, quantidade=0, habilitado='N')
            return redirect('AgendaIndustria')

    return render(request, 'industria/cadastro.html', {'form': form})

def detalhesAgendaIndustria(request, pk):
    template_name = 'industria/detalhesAgenda.html'
    agendaIndustria = AgendaIndustria.objects.get(pk=pk)
    pedidos = PedidoIndustria.objects.get_queryset().filter(master=agendaIndustria)
    itens = QuantidadeItemIndustria.objects.filter(pedido__in=pedidos)
    totalItens = itens.values('item', 'item__codigo', 'descricao', 'item__categoria').annotate(total_quantidade=Sum('quantidade')).order_by('item__categoria', 'descricao')
    categorias = itens.values('item__categoria')
    print(categorias)
    context = {
        'categorias': categorias,
        'agenda': agendaIndustria,
        'pedidos': pedidos,
        'itens': itens,
        'totalItens': totalItens,
    }
    return render(request, template_name, context)   

def editarAgendaIndustria(request, pk, template_name='industria/cadastro.html'):
    agendaIndustria = get_object_or_404(AgendaIndustria, pk=pk)
    form = AgendaIndustriaForm(request.POST or None, instance=agendaIndustria)
    if form.is_valid():
        form.save()
        return redirect('AgendaIndustria')
    return render(request, template_name, {'form': form})


def excluirAgendaIndustria(request, pk, template_name='industria/confirm_delete.html'):
    agendaIndustria = get_object_or_404(AgendaIndustria, pk=pk)
    if request.method == 'POST':
        agendaIndustria.delete()
        return redirect('AgendaIndustria')
    return render(request, template_name, {'object': agendaIndustria})    

#---------------------------------------------------------------------------------------------------------

#PedidosIndustria-------------------------------------------------------------------------------------

class listaPedidoIndustria(ListView):
    model = PedidoIndustria
    template_name = 'industria/listaPedido.html'
    context_object_name = 'pedidoIndustria_list'

    def get_queryset(self):
        queryset = ""
        if self.request.user.is_authenticated:
            queryset = super(listaPedidoIndustria, self).get_queryset()
            queryset = queryset.filter(empresa__in=Empresa.objects.filter(usuarios=self.request.user)).order_by('-master__data_final')
        return queryset

def detalhesPedidoIndustria(request, pk):
    template_name = 'industria/detalhesPedido.html'
    if request.user.is_authenticated:
        empresas = Empresa.objects.filter(usuarios=request.user)
        pedido = PedidoIndustria.objects.get(pk=pk)
        itens = QuantidadeItemIndustria.objects.filter(pedido=pedido).order_by('item__categoria','item__descricao')
        context = {
            'pedido': pedido,
            'itens': itens,
        }
        if pedido.empresa in empresas:
            return render(request, template_name, context)
    return HttpResponseNotFound("404 Not Found")      

def editarPedidoIndustria(request, pk, template_name='industria/cadastroPedido.html'):
    if request.user.is_authenticated:
        empresas = Empresa.objects.filter(usuarios=request.user)
        pedido = PedidoIndustria.objects.get(pk=pk)
        itens = QuantidadeItemIndustria.objects.filter(pedido=pedido).order_by('item__categoria','item__descricao')
        formset = PedidoIndustriaFormset(request.POST or None, instance=pedido, queryset=itens, prefix='item')
        context = {
            'pedido': pedido,
            'formset': formset
            }
        if request.method == 'POST':
            if formset.is_valid():
                formset.save()
                return redirect('PedidoIndustria')
            else:
                print(formset.errors)
        if pedido.empresa in empresas:        
            return render(request, template_name, context)
    return HttpResponseNotFound("404 Not Found") 

def excluirPedidoIndustria(request, pk, template_name='industria/confirm_delete.html'):
    agendaIndustria = get_object_or_404(AgendaIndustria, pk=pk)
    if request.method == 'POST':
        agendaIndustria.delete()
        return redirect('AgendaIndustria')
    return render(request, template_name, {'object': agendaIndustria})

#---------------------------------------------------------------------------------------------------------