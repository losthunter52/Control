from django.forms import NullBooleanField, inlineformset_factory, modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from .models import *
from .forms import *
from django.db.models import Q
from django.db.models import Sum, Avg, Max, Min, Value, CharField
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User


# Create your views here.
# Geral

# ---------------------------------------------------------------------------------------------------------

# ItemHortifruti----------------------------------------------------------------------------------------

class listaItemHortifruti(ListView):
    model = ItemHortifruti
    template_name = 'hortifruti/listaItem.html'
    context_object_name = 'item_list'

    def get_queryset(self):
        queryset = super(listaItemHortifruti,
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


def cadastroItemHortifruti(request):
    form = ItemHortifrutiForm()
    if request.method == 'POST':
        form = ItemHortifrutiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ItemHortifruti')

    return render(request, 'hortifruti/cadastro.html', {'form': form})


def editarItemHortifruti(request, pk, template_name='hortifruti/cadastro.html'):
    itens = get_object_or_404(ItemHortifruti, pk=pk)
    form = ItemHortifrutiForm(request.POST or None, instance=itens)
    if form.is_valid():
        form.save()
        return redirect('ItemHortifruti')
    return render(request, template_name, {'form': form})


def excluirItemHortifruti(request, pk, template_name='hortifruti/confirm_delete.html'):
    item = get_object_or_404(ItemHortifruti, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('ItemHortifruti')
    return render(request, template_name, {'object': item})

# ---------------------------------------------------------------------------------------------------------

# AgendaHortifruti--------------------------------------------------------------------------------------


class listaAgendaHortifruti(ListView):
    model = AgendaHortifruti
    template_name = 'hortifruti/listaAgenda.html'
    context_object_name = 'agendaHortifruti_list'

    def get_queryset(self):
        queryset = super(listaAgendaHortifruti,
                         self).get_queryset().order_by('-data_final')
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


def cadastroAgendaHortifruti(request):
    form = AgendaHortifrutiForm()
    empresas = Empresa.objects.filter(habilitada="S")
    if request.method == 'POST':
        form = AgendaHortifrutiForm(request.POST)
        if form.is_valid():
            agenda = form.save()
            for empresa in empresas:
                itens = ItemHortifruti.objects.all()
                if itens.exists():
                    pedido = PedidoHortifruti.objects.create(
                        master=agenda, empresa=empresa)
                    for item in itens:
                            QuantidadeItemHortifruti.objects.create(
                                item=item, descricao=item.descricao, pedido=pedido)
            return redirect('AgendaHortifruti')

    return render(request, 'hortifruti/cadastro.html', {'form': form})


def detalhesAgendaHortifruti(request, pk):
    template_name = 'hortifruti/detalhesAgenda.html'
    agendaHortifruti = AgendaHortifruti.objects.get(pk=pk)
    pedidos = PedidoHortifruti.objects.get_queryset().filter(master=agendaHortifruti)
    itens = QuantidadeItemHortifruti.objects.filter(pedido__in=pedidos)
    totalItens = itens.values('item', 'item__codigo', 'descricao').annotate(
        total_quantidadeRequisitada=Sum('quantidadeRequisitada'), total_quantidadeAdiquirida=Sum('quantidadeAdquirida')).order_by('descricao')
    context = {
        'agenda': agendaHortifruti,
        'pedidos': pedidos,
        'itens': itens,
        'totalItens': totalItens,
    }
    return render(request, template_name, context)


def editarAgendaHortifruti(request, pk, template_name='hortifruti/cadastro.html'):
    agendaHortifruti = get_object_or_404(AgendaHortifruti, pk=pk)
    form = AgendaHortifrutiForm(
        request.POST or None, instance=agendaHortifruti)
    if form.is_valid():
        form.save()
        return redirect('AgendaHortifruti')
    return render(request, template_name, {'form': form})


def editarItemAgendaHortifruti(request, pkAgenda, pkItem, template_name='hortifruti/itemAgenda.html'):
    if request.user.is_authenticated:
        agenda = AgendaHortifruti.objects.get(pk=pkAgenda)
        item = ItemHortifruti.objects.get(codigo=pkItem)
        itens = QuantidadeItemHortifruti.objects.filter(item__codigo=pkItem).filter(
            pedido__master=agenda)
        total_item = itens.values('item').aggregate(total=Sum('quantidadeRequisitada'))
        PedidoHortifrutiAdiquiridoFormset = modelformset_factory(QuantidadeItemHortifruti, form=QuantidadeItemHortifrutiAdiquiridoForm, fields=('__all__'), extra=0)
        formset = PedidoHortifrutiAdiquiridoFormset(
            request.POST or None, queryset=itens, prefix='item')
        context = {
            'total_item': total_item,
            'item' : item,
            'agenda': agenda,
            'formset': formset
        }
        if request.method == 'POST':
            if formset.is_valid():
                formset.save()
                return redirect('AgendaHortifrutiDetalhes', pk=pkAgenda)
            else:
                print(formset.errors)
        return render(request, template_name, context)
    return HttpResponseNotFound("404 Not Found")


def excluirAgendaHortifruti(request, pk, template_name='hortifruti/confirm_delete.html'):
    agendaHortifruti = get_object_or_404(AgendaHortifruti, pk=pk)
    if request.method == 'POST':
        agendaHortifruti.delete()
        return redirect('AgendaHortifruti')
    return render(request, template_name, {'object': agendaHortifruti})

# ---------------------------------------------------------------------------------------------------------

# PedidosHortifruti-------------------------------------------------------------------------------------


class listaPedidoHortifruti(ListView):
    model = PedidoHortifruti
    template_name = 'hortifruti/listaPedido.html'
    context_object_name = 'pedidoHortifruti_list'

    def get_queryset(self):
        queryset = ""
        if self.request.user.is_authenticated:
            queryset = super(listaPedidoHortifruti, self).get_queryset()
            queryset = queryset.filter(empresa__in=Empresa.objects.filter(
                usuarios=self.request.user)).order_by('-master__data_final')
        return queryset


def detalhesPedidoHortifruti(request, pk):
    template_name = 'hortifruti/detalhesPedido.html'
    if request.user.is_authenticated:
        empresas = Empresa.objects.filter(usuarios=request.user)
        pedido = PedidoHortifruti.objects.get(pk=pk)
        itens = QuantidadeItemHortifruti.objects.filter(
            pedido=pedido).order_by('item__descricao')
        context = {
            'pedido': pedido,
            'itens': itens,
        }
        if pedido.empresa in empresas:
            return render(request, template_name, context)
    return HttpResponseNotFound("404 Not Found")


def editarPedidoHortifruti(request, pk, template_name='hortifruti/cadastroPedido.html'):
    if request.user.is_authenticated:
        empresas = Empresa.objects.filter(usuarios=request.user)
        pedido = PedidoHortifruti.objects.get(pk=pk)
        itens = QuantidadeItemHortifruti.objects.filter(
            pedido=pedido).order_by('item__descricao')
        formset = PedidoHortifrutiRequisitadoFormset(
            request.POST or None, instance=pedido, queryset=itens, prefix='item')
        context = {
            'pedido': pedido,
            'formset': formset
        }
        if request.method == 'POST':
            if formset.is_valid():
                formset.save()
                return redirect('PedidoHortifruti')
            else:
                print(formset.errors)
        if pedido.empresa in empresas:
            return render(request, template_name, context)
    return HttpResponseNotFound("404 Not Found")


def excluirPedidoHortifruti(request, pk, template_name='hortifruti/confirm_delete.html'):
    agendaHortifruti = get_object_or_404(AgendaHortifruti, pk=pk)
    if request.method == 'POST':
        agendaHortifruti.delete()
        return redirect('AgendaHortifruti')
    return render(request, template_name, {'object': agendaHortifruti})

# ---------------------------------------------------------------------------------------------------------
