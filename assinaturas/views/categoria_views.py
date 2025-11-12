"""
Views para CRUD de Categorias
(Create, Read, Update, Delete)
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def listar_categorias(request):
    """View para listagem de categorias"""
    # TODO: Implementar listagem completa
    return render(request, 'categorias.html')


@login_required(login_url='login')
def criar_categoria(request):
    """View para criar nova categoria"""
    # TODO: Implementar criação
    pass


@login_required(login_url='login')
def editar_categoria(request, id):
    """View para editar categoria existente"""
    # TODO: Implementar edição
    pass


@login_required(login_url='login')
def deletar_categoria(request, id):
    """View para deletar categoria"""
    # TODO: Implementar exclusão
    pass
