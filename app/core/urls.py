from django.urls import include, path
from . import views

# Generic
urlpatterns = [
    path('home/', views.home, name='Home'),
]

# Empresa
urlpatterns += [
    path('empresa/', views.listaEmpresa.as_view(), name='Empresa'),
    path('empresa/add', views.cadastroEmpresa, name='EmpresaCadastro'),
    path('empresa/edit/<int:pk>', views.editarEmpresa, name='EmpresaEditar'),
    path('empresa/<int:pk>', views.detalhesEmpresa.as_view(), name='EmpresaDetalhes'),
    path('empresa/delete<int:pk>', views.excluirEmpresa, name='EmpresaExcluir'),
]

# Modulo: Gestor de Pedidos

urlpatterns += [
    path('abastecimento/', include('abastecimento.urls')),
    path('industria/', include('industria.urls')),
    path('hortifruti/', include('hortifruti.urls'))
]