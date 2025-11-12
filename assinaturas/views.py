from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from decimal import Decimal
from datetime import date, timedelta
from .models import Assinatura, Categoria


def dashboard(request):
    """
    View principal do dashboard com estatísticas e resumo das assinaturas
    """
    if request.user.is_authenticated:
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
            total_assinaturas=Count('assinaturas', filter=Q(assinaturas__status='ATIVA'))
        ).filter(total_assinaturas__gt=0)
        
        context = {
            'total_assinaturas': total_assinaturas,
            'gasto_mensal': gasto_mensal,
            'gasto_anual': gasto_anual,
            'proximas_cobranças': proximas_cobranças,
            'categorias_stats': categorias_stats,
            'assinaturas_ativas': assinaturas_ativas[:5],  # Últimas 5 assinaturas
        }
    else:
        context = {
            'total_assinaturas': 0,
            'gasto_mensal': 0,
            'gasto_anual': 0,
            'proximas_cobranças': [],
            'categorias_stats': [],
            'assinaturas_ativas': [],
        }
    
    return render(request, 'dashboard.html', context)


def assinaturas_view(request):
    """View temporária para lista de assinaturas"""
    return render(request, 'assinaturas.html')


def categorias_view(request):
    """View temporária para categorias"""
    return render(request, 'categorias.html')
