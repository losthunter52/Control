from django.forms import NullBooleanField, inlineformset_factory, modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from .models import *
from .forms import *
from django.db.models import Q
from django.db.models import Sum, Count, Value, CharField
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User


# Create your views here.
# Geral


# ---------------------------------------------------------------------------------------------------------

# ItemAbastecimento----------------------------------------------------------------------------------------

class listaItemAbastecimento(ListView):
    model = ItemAbastecimento
    template_name = 'abastecimento/listaItem.html'
    context_object_name = 'item_list'

    def get_queryset(self):
        queryset = super(listaItemAbastecimento,
                         self).get_queryset().order_by('descricao')
        data = self.request.GET
        search = data.get('search')
        if search:
            queryset = queryset.filter(
                Q(codigo__icontains=search) |
                Q(descricao__icontains=search) |
                Q(tipo__icontains=search)
            ).order_by('descricao')
        return queryset


def cadastroItemAbastecimento(request):
    form = ItemAbastecimentoForm()
    if request.method == 'POST':
        form = ItemAbastecimentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ItemAbastecimento')

    return render(request, 'abastecimento/cadastro.html', {'form': form})


def editarItemAbastecimento(request, pk, template_name='abastecimento/cadastro.html'):
    itens = get_object_or_404(ItemAbastecimento, pk=pk)
    form = ItemAbastecimentoForm(request.POST or None, instance=itens)
    if form.is_valid():
        form.save()
        return redirect('ItemAbastecimento')
    return render(request, template_name, {'form': form})


def excluirItemAbastecimento(request, pk, template_name='abastecimento/confirm_delete.html'):
    item = get_object_or_404(ItemAbastecimento, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('ItemAbastecimento')
    return render(request, template_name, {'object': item})

# ---------------------------------------------------------------------------------------------------------

# CategoriaAbastecimento-----------------------------------------------------------------------------------


class listaCategoriaAbastecimento(ListView):
    model = CategoriaAbastecimento
    template_name = 'abastecimento/listaCategoria.html'
    context_object_name = 'categoriaAbastecimento_list'

    def get_queryset(self):
        queryset = super(listaCategoriaAbastecimento,
                         self).get_queryset().order_by('descricao')
        data = self.request.GET
        search = data.get('search')
        if search:
            queryset = queryset.filter(
                Q(descricao__icontains=search)
            ).order_by('descricao')
        return queryset


def cadastroCategoriaAbastecimento(request):
    form = CategoriaAbastecimentoForm()
    if request.method == 'POST':
        form = CategoriaAbastecimentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('CategoriaAbastecimento')

    return render(request, 'abastecimento/cadastro.html', {'form': form})


def editarCategoriaAbastecimento(request, pk, template_name='abastecimento/cadastro.html'):
    categoriaAbastecimento = get_object_or_404(CategoriaAbastecimento, pk=pk)
    form = CategoriaAbastecimentoForm(
        request.POST or None, instance=categoriaAbastecimento)
    if form.is_valid():
        form.save()
        return redirect('CategoriaAbastecimento')
    return render(request, template_name, {'form': form})


def excluirCategoriaAbastecimento(request, pk, template_name='abastecimento/confirm_delete.html'):
    categoriaAbastecimento = get_object_or_404(CategoriaAbastecimento, pk=pk)
    if request.method == 'POST':
        categoriaAbastecimento.delete()
        return redirect('CategoriaAbastecimento')
    return render(request, template_name, {'object': categoriaAbastecimento})

# ---------------------------------------------------------------------------------------------------------

# AgendaAbastecimento--------------------------------------------------------------------------------------


class listaAgendaAbastecimento(ListView):
    model = AgendaAbastecimento
    template_name = 'abastecimento/listaAgenda.html'
    context_object_name = 'agendaAbastecimento_list'

    def get_queryset(self):
        queryset = super(listaAgendaAbastecimento,
                         self).get_queryset().order_by('-data_final', '-pk')
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


def cadastroAgendaAbastecimento(request):
    form = AgendaAbastecimentoForm()
    empresas = Empresa.objects.filter(habilitada="S")
    if request.method == 'POST':
        form = AgendaAbastecimentoForm(request.POST)
        if form.is_valid():
            agenda = form.save()
            for empresa in empresas:
                itens = ItemAbastecimento.objects.filter(tipo=agenda.tipo)
                if itens.exists():
                    pedido = PedidoAbastecimento.objects.create(
                        master=agenda, empresa=empresa)
                    for item in itens:
                        if empresa in item.empresas.all():
                            QuantidadeItemAbastecimento.objects.create(
                                item=item, descricao=item.descricao, pedido=pedido, habilitado='S', acougue=item.acougue, loja=item.loja, padaria=item.padaria, verdura=item.verdura)
                        else:
                            QuantidadeItemAbastecimento.objects.create(
                                item=item, descricao=item.descricao, pedido=pedido, habilitado='N', acougue=item.acougue, loja=item.loja, padaria=item.padaria, verdura=item.verdura)
            return redirect('AgendaAbastecimento')

    return render(request, 'abastecimento/cadastro.html', {'form': form})


def detalhesAgendaAbastecimento(request, pk):
    template_name = 'abastecimento/detalhesAgenda.html'
    agendaAbastecimento = AgendaAbastecimento.objects.get(pk=pk)
    pedidos = PedidoAbastecimento.objects.get_queryset().filter(
        master=agendaAbastecimento)
    itens = QuantidadeItemAbastecimento.objects.filter(pedido__in=pedidos)
    totalItens = itens.values('item', 'item__codigo', 'descricao', 'item__categoria', 'item__categoria__descricao').annotate(
        total_quantidadeRequisitada=Sum('quantidadeRequisitada')).order_by('item__categoria', 'descricao').annotate(
        total_quantidadeAdiquirida=Sum('quantidadeAdquirida')).order_by('item__categoria', 'descricao')
    categorias = itens.values('item__categoria', 'item__categoria__descricao').annotate(
        quantidade=Sum('quantidadeRequisitada'))
    context = {
        'categorias': categorias,
        'agenda': agendaAbastecimento,
        'pedidos': pedidos,
        'itens': itens,
        'totalItens': totalItens,
    }
    return render(request, template_name, context)


def editarAgendaAbastecimento(request, pk, template_name='abastecimento/cadastro.html'):
    agendaAbastecimento = get_object_or_404(AgendaAbastecimento, pk=pk)
    form = AgendaAbastecimentoForm(
        request.POST or None, instance=agendaAbastecimento)
    if form.is_valid():
        form.save()
        return redirect('AgendaAbastecimento')
    return render(request, template_name, {'form': form})


def editarItemAgendaAbastecimento(request, pkAgenda, pkItem, template_name='abastecimento/itemAgenda.html'):
    if request.user.is_authenticated:
        agenda = AgendaAbastecimento.objects.get(pk=pkAgenda)
        item = ItemAbastecimento.objects.get(codigo=pkItem)
        itens = QuantidadeItemAbastecimento.objects.filter(item__codigo=pkItem).filter(
            pedido__master=agenda)
        total_item = itens.values('item').aggregate(
            total=Sum('quantidadeRequisitada'))
        PedidoAbastecimentoAdiquiridoFormset = modelformset_factory(
            QuantidadeItemAbastecimento, form=QuantidadeItemAbastecimentoAdiquiridoForm, fields=('__all__'), extra=0)
        formset = PedidoAbastecimentoAdiquiridoFormset(
            request.POST or None, queryset=itens, prefix='item')
        context = {
            'total_item': total_item,
            'item': item,
            'agenda': agenda,
            'formset': formset
        }
        if request.method == 'POST':
            if formset.is_valid():
                formset.save()
                return redirect('AgendaAbastecimentoDetalhes', pk=pkAgenda)
            else:
                print(formset.errors)
        return render(request, template_name, context)
    return HttpResponseNotFound("404 Not Found")


def excluirAgendaAbastecimento(request, pk, template_name='abastecimento/confirm_delete.html'):
    agendaAbastecimento = get_object_or_404(AgendaAbastecimento, pk=pk)
    if request.method == 'POST':
        agendaAbastecimento.delete()
        return redirect('AgendaAbastecimento')
    return render(request, template_name, {'object': agendaAbastecimento})

# ---------------------------------------------------------------------------------------------------------

# PedidosAbastecimento-------------------------------------------------------------------------------------


class listaPedidoAbastecimento(ListView):
    model = PedidoAbastecimento
    template_name = 'abastecimento/listaPedido.html'
    context_object_name = 'pedidoAbastecimento_list'

    def get_queryset(self):
        queryset = ""
        if self.request.user.is_authenticated:
            queryset = super(listaPedidoAbastecimento, self).get_queryset()
            queryset = queryset.filter(empresa__in=Empresa.objects.filter(
                usuarios=self.request.user)).order_by('-master__data_final', '-master__pk')
        return queryset


def detalhesPedidoAbastecimento(request, pk):
    template_name = 'abastecimento/detalhesPedido.html'
    if request.user.is_authenticated:
        empresas = Empresa.objects.filter(usuarios=request.user)
        pedido = PedidoAbastecimento.objects.get(pk=pk)
        itens = QuantidadeItemAbastecimento.objects.filter(
            pedido=pedido).order_by('item__categoria', 'item__descricao')
        context = {
            'pedido': pedido,
            'itens': itens,
        }
        if pedido.empresa in empresas:
            return render(request, template_name, context)
    return HttpResponseNotFound("404 Not Found")


def editarPedidoAbastecimento(request, pk, template_name='abastecimento/cadastroPedido.html'):
    if request.user.is_authenticated:
        empresas = Empresa.objects.filter(usuarios=request.user)
        pedido = PedidoAbastecimento.objects.get(pk=pk)
        itens = QuantidadeItemAbastecimento.objects.filter(
            pedido=pedido)
        categorias = itens.values('item__categoria', 'item__categoria__descricao').annotate(quantidade=Count('item__categoria'))
        formset = PedidoAbastecimentoFormset(
            request.POST or None, instance=pedido, queryset=itens, prefix='item')
        context = {
            'categorias': categorias,
            'pedido': pedido,
            'formset': formset
        }
        if request.method == 'POST':
            if formset.is_valid():
                formset.save()
                return redirect('PedidoAbastecimento')
            else:
                print(formset.errors)
        if pedido.empresa in empresas:
            return render(request, template_name, context)
    return HttpResponseNotFound("404 Not Found")


def excluirPedidoAbastecimento(request, pk, template_name='abastecimento/confirm_delete.html'):
    agendaAbastecimento = get_object_or_404(AgendaAbastecimento, pk=pk)
    if request.method == 'POST':
        agendaAbastecimento.delete()
        return redirect('AgendaAbastecimento')
    return render(request, template_name, {'object': agendaAbastecimento})

# ---------------------------------------------------------------------------------------------------------
