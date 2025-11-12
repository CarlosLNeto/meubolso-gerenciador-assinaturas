from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Q
from datetime import date, timedelta
from decimal import Decimal
from .models import Assinatura, Categoria


@login_required(login_url='login')
def dashboard(request):
    """
    View principal do dashboard com estatísticas e resumo das assinaturas
    """
    # Assinaturas ativas do usuário
    assinaturas_ativas = Assinatura.objects.filter(
        usuario=request.user,
        status='ATIVA'
    )

    # Total de assinaturas ativas
    total_assinaturas = assinaturas_ativas.count()

    # Gasto mensal (convertendo todas as assinaturas para base mensal)
    gasto_mensal = sum(
        assinatura.valor_mensal()
        for assinatura in assinaturas_ativas
    )

    # Gasto anual
    gasto_anual = sum(
        assinatura.valor_anual()
        for assinatura in assinaturas_ativas
    )

    # Próximas cobranças (próximos 30 dias)
    hoje = date.today()
    proximos_30_dias = hoje + timedelta(days=30)

    proximas_cobranças = assinaturas_ativas.filter(
        data_proxima_cobranca__gte=hoje,
        data_proxima_cobranca__lte=proximos_30_dias
    ).order_by('data_proxima_cobranca')[:5]

    # Distribuição por categoria
    categorias_stats = Categoria.objects.filter(
        usuario=request.user
    ).annotate(
        total_assinaturas=Count(
            'assinaturas',
            filter=Q(assinaturas__status='ATIVA')
        )
    ).filter(total_assinaturas__gt=0)

    context = {
        'total_assinaturas': total_assinaturas,
        'gasto_mensal': gasto_mensal,
        'gasto_anual': gasto_anual,
        'proximas_cobranças': proximas_cobranças,
        'categorias_stats': categorias_stats,
        'assinaturas_ativas': assinaturas_ativas[:5],
    }

    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def assinaturas_view(request):
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
        if not nome or not valor or not ciclo_pagamento or not data_primeira_cobranca:
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
            return redirect('criar_assinatura')
        
        try:
            # Converter valor para Decimal
            valor = Decimal(valor.replace(',', '.'))
            
            # Buscar categoria (se fornecida)
            categoria = None
            if categoria_id:
                categoria = Categoria.objects.get(id=categoria_id, usuario=request.user)
            
            # Criar assinatura
            assinatura = Assinatura.objects.create(
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
            
            messages.success(request, f'Assinatura "{nome}" criada com sucesso!')
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


def categorias_view(request):
    """View temporária para categorias"""
    return render(request, 'categorias.html')


def login_view(request):
    """View para login de usuários"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
   
        user = authenticate(request, username=username, password=password)
  
        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo de volta, {user.username}!')
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuário ou senha incorretos.')

    return render(request, 'login.html')


def signup_view(request):
    """View para cadastro de novos usuários"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # Validações
        if password != password_confirm:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'signup.html')
     
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Este nome de usuário já está em uso.')
            return render(request, 'signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este e-mail já está cadastrado.')
            return render(request, 'signup.html')
        
        # Criar usuário
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Fazer login automático
        login(request, user)
        messages.success(request, 'Conta criada com sucesso! Bem-vindo!')
        return redirect('dashboard')
    
    return render(request, 'signup.html')


def logout_view(request):
    """View para logout de usuários"""
    logout(request)
    messages.success(request, 'Você saiu com sucesso.')
    return redirect('login')
