"""
Views para CRUD de Categorias
(Create, Read, Update, Delete)
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from ..models import Categoria, Assinatura


@login_required(login_url='login')
def listar_categorias(request):
    """View para listagem de categorias com estatísticas"""
    # Buscar todas as categorias do usuário
    categorias = Categoria.objects.filter(usuario=request.user).annotate(
        total_assinaturas=Count(
            'assinaturas',
            filter=Q(assinaturas__status='ATIVA')
        ),
        total_todas=Count('assinaturas')
    ).order_by('nome')

    # Estatísticas
    total_categorias = categorias.count()
    
    context = {
        'categorias': categorias,
        'total_categorias': total_categorias,
    }

    return render(request, 'categorias.html', context)


@login_required(login_url='login')
def criar_categoria(request):
    """View para criar nova categoria"""
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao', '')
        cor = request.POST.get('cor', '#6366f1')

        # Validações
        if not nome:
            messages.error(request, 'O nome da categoria é obrigatório.')
            return redirect('criar_categoria')

        # Verificar se já existe categoria com esse nome
        if Categoria.objects.filter(
            usuario=request.user,
            nome=nome
        ).exists():
            messages.error(
                request,
                f'Você já possui uma categoria com o nome "{nome}".'
            )
            return redirect('criar_categoria')

        try:
            # Criar categoria
            Categoria.objects.create(
                usuario=request.user,
                nome=nome,
                descricao=descricao,
                cor=cor
            )

            messages.success(
                request,
                f'Categoria "{nome}" criada com sucesso!'
            )
            return redirect('categorias')

        except Exception as e:
            messages.error(request, f'Erro ao criar categoria: {str(e)}')
            return redirect('criar_categoria')

    return render(request, 'categoria_form.html')


@login_required(login_url='login')
def editar_categoria(request, id):
    """View para editar categoria existente"""
    categoria = get_object_or_404(
        Categoria,
        id=id,
        usuario=request.user
    )

    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao', '')
        cor = request.POST.get('cor', '#6366f1')

        # Validações
        if not nome:
            messages.error(request, 'O nome da categoria é obrigatório.')
            return redirect('editar_categoria', id=id)

        # Verificar se já existe outra categoria com esse nome
        if Categoria.objects.filter(
            usuario=request.user,
            nome=nome
        ).exclude(id=id).exists():
            messages.error(
                request,
                f'Você já possui uma categoria com o nome "{nome}".'
            )
            return redirect('editar_categoria', id=id)

        try:
            # Atualizar categoria
            categoria.nome = nome
            categoria.descricao = descricao
            categoria.cor = cor
            categoria.save()

            messages.success(
                request,
                f'Categoria "{nome}" atualizada com sucesso!'
            )
            return redirect('categorias')

        except Exception as e:
            messages.error(request, f'Erro ao atualizar: {str(e)}')
            return redirect('editar_categoria', id=id)

    context = {
        'categoria': categoria,
        'is_edit': True,
    }

    return render(request, 'categoria_form.html', context)


@login_required(login_url='login')
def deletar_categoria(request, id):
    """View para deletar categoria"""
    categoria = get_object_or_404(
        Categoria,
        id=id,
        usuario=request.user
    )

    # Verificar quantas assinaturas usam esta categoria
    total_assinaturas = categoria.assinaturas.count()

    if request.method == 'POST':
        nome = categoria.nome
        categoria.delete()
        messages.success(
            request,
            f'Categoria "{nome}" foi excluída com sucesso!'
        )
        return redirect('categorias')

    context = {
        'categoria': categoria,
        'total_assinaturas': total_assinaturas,
    }

    return render(request, 'categoria_delete.html', context)
