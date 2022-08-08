from django.urls import path
from . import views

# Generic


#ItemAbastecimento
urlpatterns = [
    path('admin/itemAbastecimento/', views.listaItemAbastecimento.as_view(), name='ItemAbastecimento'),
    path('admin/itemAbastecimento/add', views.cadastroItemAbastecimento, name='ItemAbastecimentoCadastro'),
    path('admin/itemAbastecimento/edit/<int:pk>', views.editarItemAbastecimento, name='ItemAbastecimentoEditar'),
    path('admin/itemAbastecimento/delete<int:pk>', views.excluirItemAbastecimento, name='ItemAbastecimentoExcluir'),
]

# CategoriaAbastecimento
urlpatterns += [
    path('admin/categoriaAbastecimento/', views.listaCategoriaAbastecimento.as_view(), name='CategoriaAbastecimento'),
    path('admin/categoriaAbastecimento/add', views.cadastroCategoriaAbastecimento, name='CategoriaAbastecimentoCadastro'),
    path('admin/categoriaAbastecimento/edit/<int:pk>', views.editarCategoriaAbastecimento, name='CategoriaAbastecimentoEditar'),
    path('admin/categoriaAbastecimento/delete<int:pk>', views.excluirCategoriaAbastecimento, name='CategoriaAbastecimentoExcluir'),
]

# AgendaAbastecimento
urlpatterns += [
    path('admin/agendaAbastecimento/', views.listaAgendaAbastecimento.as_view(), name='AgendaAbastecimento'),
    path('admin/agendaAbastecimento/<int:pk>', views.detalhesAgendaAbastecimento, name='AgendaAbastecimentoDetalhes'),
    path('admin/agendaAbastecimento/<int:pkAgenda>/<str:pkItem>', views.editarItemAgendaAbastecimento, name='ItemAgendaAbastecimento'),
    path('admin/agendaAbastecimento/add', views.cadastroAgendaAbastecimento, name='AgendaAbastecimentoCadastro'),
    path('admin/agendaAbastecimento/edit/<int:pk>', views.editarAgendaAbastecimento, name='AgendaAbastecimentoEditar'),
    path('admin/agendaAbastecimento/delete<int:pk>', views.excluirAgendaAbastecimento, name='AgendaAbastecimentoExcluir'),
]

# PedidoAbastecimento
urlpatterns += [
    path('pedidoAbastecimento/', views.listaPedidoAbastecimento.as_view(), name='PedidoAbastecimento'),
    path('pedidoAbastecimento/<int:pk>', views.detalhesPedidoAbastecimento, name='PedidoAbastecimentoDetalhes'),
    path('pedidoAbastecimento/edit/<int:pk>', views.editarPedidoAbastecimento, name='PedidoAbastecimentoEditar'),
    path('pedidoAbastecimento/delete<int:pk>', views.excluirPedidoAbastecimento, name='PedidoAbastecimentoExcluir'),
]
