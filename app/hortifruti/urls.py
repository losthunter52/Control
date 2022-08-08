from django.urls import path
from . import views

# Generic


#ItemHortifruti
urlpatterns = [
    path('admin/item/', views.listaItemHortifruti.as_view(), name='ItemHortifruti'),
    path('admin/item/add', views.cadastroItemHortifruti, name='ItemHortifrutiCadastro'),
    path('admin/item/edit/<int:pk>', views.editarItemHortifruti, name='ItemHortifrutiEditar'),
    path('admin/item/delete<int:pk>', views.excluirItemHortifruti, name='ItemHortifrutiExcluir'),
]

# AgendaHortifruti
urlpatterns += [
    path('admin/agenda/', views.listaAgendaHortifruti.as_view(), name='AgendaHortifruti'),
    path('admin/agenda/<int:pk>', views.detalhesAgendaHortifruti, name='AgendaHortifrutiDetalhes'),
    path('admin/agenda/<int:pkAgenda>/<str:pkItem>', views.editarItemAgendaHortifruti, name='ItemAgendaHortifruti'),
    path('admin/agenda/add', views.cadastroAgendaHortifruti, name='AgendaHortifrutiCadastro'),
    path('admin/agenda/edit/<int:pk>', views.editarAgendaHortifruti, name='AgendaHortifrutiEditar'),
    path('admin/agenda/delete<int:pk>', views.excluirAgendaHortifruti, name='AgendaHortifrutiExcluir'),
]

# PedidoHortifruti
urlpatterns += [
    path('pedido/', views.listaPedidoHortifruti.as_view(), name='PedidoHortifruti'),
    path('pedido/<int:pk>', views.detalhesPedidoHortifruti, name='PedidoHortifrutiDetalhes'),
    path('pedido/edit/<int:pk>', views.editarPedidoHortifruti, name='PedidoHortifrutiEditar'),
    path('pedido/delete<int:pk>', views.excluirPedidoHortifruti, name='PedidoHortifrutiExcluir'),
]
