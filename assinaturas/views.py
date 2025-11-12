from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Count, Q
from decimal import Decimal
from datetime import date, timedelta
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


def assinaturas_view(request):
    """View temporária para lista de assinaturas"""
    return render(request, 'assinaturas.html')


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
