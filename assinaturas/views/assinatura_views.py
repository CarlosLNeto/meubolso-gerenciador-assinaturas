"""
Views para CRUD de Assinaturas
(Create, Read, Update, Delete)
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from ..models import Assinatura, Categoria


@login_required(login_url='login')
def listar_assinaturas(request):
    """View para listagem de assinaturas com filtros"""
    # Buscar todas as assinaturas do usuário
    assinaturas = Assinatura.objects.filter(usuario=request.user)

    # Filtro por status
    status_filter = request.GET.get('status', '')
    if status_filter:
        assinaturas = assinaturas.filter(status=status_filter)

    # Filtro por categoria
    categoria_filter = request.GET.get('categoria', '')
    if categoria_filter:
        assinaturas = assinaturas.filter(categoria_id=categoria_filter)

    # Busca por nome
    search = request.GET.get('search', '')
    if search:
        assinaturas = assinaturas.filter(nome__icontains=search)

    # Ordenação
    order_by = request.GET.get('order_by', '-data_criacao')
    assinaturas = assinaturas.order_by(order_by)

    # Buscar todas as categorias do usuário para o filtro
    categorias = Categoria.objects.filter(usuario=request.user)

    # Estatísticas
    total_assinaturas = assinaturas.count()
    assinaturas_ativas = assinaturas.filter(status='ATIVA').count()

    context = {
        'assinaturas': assinaturas,
        'categorias': categorias,
        'total_assinaturas': total_assinaturas,
        'assinaturas_ativas': assinaturas_ativas,
        'status_filter': status_filter,
        'categoria_filter': categoria_filter,
        'search': search,
        'order_by': order_by,
    }

    return render(request, 'assinaturas.html', context)


@login_required(login_url='login')
def criar_assinatura(request):
    """View para criar nova assinatura"""
    if request.method == 'POST':
        # Coletar dados do formulário
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao', '')
        valor = request.POST.get('valor')
        ciclo_pagamento = request.POST.get('ciclo_pagamento')
        data_primeira_cobranca = request.POST.get('data_primeira_cobranca')
        categoria_id = request.POST.get('categoria')
        status = request.POST.get('status', 'ATIVA')
        observacoes = request.POST.get('observacoes', '')

        # Validações básicas
        if not all([nome, valor, ciclo_pagamento, data_primeira_cobranca]):
            messages.error(
                request,
                'Por favor, preencha todos os campos obrigatórios.'
            )
            return redirect('criar_assinatura')

        try:
            # Converter valor para Decimal
            valor = Decimal(valor.replace(',', '.'))

            # Buscar categoria (se fornecida)
            categoria = None
            if categoria_id:
                categoria = Categoria.objects.get(
                    id=categoria_id,
                    usuario=request.user
                )

            # Criar assinatura
            Assinatura.objects.create(
                usuario=request.user,
                nome=nome,
                descricao=descricao,
                valor=valor,
                ciclo_pagamento=ciclo_pagamento,
                data_primeira_cobranca=data_primeira_cobranca,
                categoria=categoria,
                status=status,
                observacoes=observacoes
            )

            messages.success(
                request,
                f'Assinatura "{nome}" criada com sucesso!'
            )
            return redirect('assinaturas')

        except Categoria.DoesNotExist:
            messages.error(request, 'Categoria inválida.')
            return redirect('criar_assinatura')
        except Exception as e:
            messages.error(request, f'Erro ao criar assinatura: {str(e)}')
            return redirect('criar_assinatura')

    # GET request - exibir formulário
    categorias = Categoria.objects.filter(usuario=request.user)

    context = {
        'categorias': categorias,
        'ciclos': Assinatura.CICLO_CHOICES,
        'status_choices': Assinatura.STATUS_CHOICES,
    }

    return render(request, 'assinatura_form.html', context)


@login_required(login_url='login')
def editar_assinatura(request, id):
    """View para editar assinatura existente"""
    assinatura = get_object_or_404(
        Assinatura,
        id=id,
        usuario=request.user
    )

    if request.method == 'POST':
        # Coletar dados do formulário
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao', '')
        valor = request.POST.get('valor')
        ciclo_pagamento = request.POST.get('ciclo_pagamento')
        data_primeira_cobranca = request.POST.get('data_primeira_cobranca')
        categoria_id = request.POST.get('categoria')
        status = request.POST.get('status', 'ATIVA')
        observacoes = request.POST.get('observacoes', '')

        # Validações básicas
        if not all([nome, valor, ciclo_pagamento, data_primeira_cobranca]):
            messages.error(
                request,
                'Por favor, preencha todos os campos obrigatórios.'
            )
            return redirect('editar_assinatura', id=id)

        try:
            # Converter valor para Decimal
            valor = Decimal(valor.replace(',', '.'))

            # Buscar categoria (se fornecida)
            categoria = None
            if categoria_id:
                categoria = Categoria.objects.get(
                    id=categoria_id,
                    usuario=request.user
                )

            # Atualizar assinatura
            assinatura.nome = nome
            assinatura.descricao = descricao
            assinatura.valor = valor
            assinatura.ciclo_pagamento = ciclo_pagamento
            assinatura.data_primeira_cobranca = data_primeira_cobranca
            assinatura.categoria = categoria
            assinatura.status = status
            assinatura.observacoes = observacoes
            assinatura.save()

            messages.success(
                request,
                f'Assinatura "{nome}" atualizada com sucesso!'
            )
            return redirect('assinaturas')

        except Categoria.DoesNotExist:
            messages.error(request, 'Categoria inválida.')
            return redirect('editar_assinatura', id=id)
        except Exception as e:
            messages.error(request, f'Erro ao atualizar: {str(e)}')
            return redirect('editar_assinatura', id=id)

    # GET request - exibir formulário preenchido
    categorias = Categoria.objects.filter(usuario=request.user)

    context = {
        'assinatura': assinatura,
        'categorias': categorias,
        'ciclos': Assinatura.CICLO_CHOICES,
        'status_choices': Assinatura.STATUS_CHOICES,
        'is_edit': True,
    }

    return render(request, 'assinatura_form.html', context)


@login_required(login_url='login')
def deletar_assinatura(request, id):
    """View para deletar assinatura"""
    assinatura = get_object_or_404(
        Assinatura,
        id=id,
        usuario=request.user
    )

    if request.method == 'POST':
        nome = assinatura.nome
        assinatura.delete()
        messages.success(
            request,
            f'Assinatura "{nome}" foi excluída com sucesso!'
        )
        return redirect('assinaturas')

    context = {
        'assinatura': assinatura,
    }

    return render(request, 'assinatura_delete.html', context)
