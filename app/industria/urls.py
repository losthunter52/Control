from django.urls import path
from . import views

# Generic


#ItemIndustria
urlpatterns = [
    path('admin/item/', views.listaItemIndustria.as_view(), name='ItemIndustria'),
    path('admin/item/add', views.cadastroItemIndustria, name='ItemIndustriaCadastro'),
    path('admin/item/edit/<int:pk>', views.editarItemIndustria, name='ItemIndustriaEditar'),
    path('admin/item/delete<int:pk>', views.excluirItemIndustria, name='ItemIndustriaExcluir'),
]

# CategoriaIndustria
urlpatterns += [
    path('admin/categoria/', views.listaCategoriaIndustria.as_view(), name='CategoriaIndustria'),
    path('admin/categoria/add', views.cadastroCategoriaIndustria, name='CategoriaIndustriaCadastro'),
    path('admin/categoria/edit/<int:pk>', views.editarCategoriaIndustria, name='CategoriaIndustriaEditar'),
    path('admin/categoria/delete<int:pk>', views.excluirCategoriaIndustria, name='CategoriaIndustriaExcluir'),
]

# AgendaIndustria
urlpatterns += [
    path('admin/agenda/', views.listaAgendaIndustria.as_view(), name='AgendaIndustria'),
    path('admin/agenda/<int:pk>', views.detalhesAgendaIndustria, name='AgendaIndustriaDetalhes'),
    path('admin/agenda/add', views.cadastroAgendaIndustria, name='AgendaIndustriaCadastro'),
    path('admin/agenda/edit/<int:pk>', views.editarAgendaIndustria, name='AgendaIndustriaEditar'),
    path('admin/agenda/delete<int:pk>', views.excluirAgendaIndustria, name='AgendaIndustriaExcluir'),
]

# PedidoIndustria
urlpatterns += [
    path('pedido/', views.listaPedidoIndustria.as_view(), name='PedidoIndustria'),
    path('pedido/<int:pk>', views.detalhesPedidoIndustria, name='PedidoIndustriaDetalhes'),
    path('pedido/edit/<int:pk>', views.editarPedidoIndustria, name='PedidoIndustriaEditar'),
    path('pedido/delete<int:pk>', views.excluirPedidoIndustria, name='PedidoIndustriaExcluir'),
]
