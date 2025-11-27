#!/usr/bin/env python
"""
Script para visualizar estatísticas do banco de dados

Uso: python -m scripts.ver_estatisticas [--usuarios]
"""
import os
import sys
import django

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meubolso.settings')
django.setup()

from django.contrib.auth.models import User
from assinaturas.models import Categoria, Assinatura
from django.db.models import Count, Sum, Q


def exibir_estatisticas():
    """Exibe estatísticas gerais do banco de dados"""
    
    print("\n" + "="*60)
    print("📊 ESTATÍSTICAS DO BANCO DE DADOS - MEU BOLSO")
    print("="*60 + "\n")
    
    # ===== USUÁRIOS =====
    total_usuarios = User.objects.count()
    usuarios_ativos = User.objects.filter(is_active=True).count()
    
    print("👥 USUÁRIOS")
    print(f"   Total: {total_usuarios}")
    print(f"   Ativos: {usuarios_ativos}")
    print(f"   Inativos: {total_usuarios - usuarios_ativos}")
    print()
    
    # ===== CATEGORIAS =====
    total_categorias = Categoria.objects.count()
    categorias_mais_usadas = Categoria.objects.annotate(
        total_assinaturas=Count('assinaturas', filter=Q(assinaturas__status='ATIVA'))
    ).order_by('-total_assinaturas')[:5]
    
    print("📁 CATEGORIAS")
    print(f"   Total: {total_categorias}")
    print()
    print("   Top 5 categorias mais usadas:")
    for cat in categorias_mais_usadas:
        print(f"      • {cat.nome}: {cat.total_assinaturas} assinaturas")
    print()
    
    # ===== ASSINATURAS =====
    total_assinaturas = Assinatura.objects.count()
    assinaturas_ativas = Assinatura.objects.filter(status='ATIVA').count()
    assinaturas_pausadas = Assinatura.objects.filter(status='PAUSADA').count()
    assinaturas_canceladas = Assinatura.objects.filter(status='CANCELADA').count()
    
    print("💳 ASSINATURAS")
    print(f"   Total: {total_assinaturas}")
    print(f"   Ativas: {assinaturas_ativas}")
    print(f"   Pausadas: {assinaturas_pausadas}")
    print(f"   Canceladas: {assinaturas_canceladas}")
    print()
    
    # ===== ESTATÍSTICAS FINANCEIRAS =====
    if assinaturas_ativas > 0:
        assinaturas = Assinatura.objects.filter(status='ATIVA')
        
        # Calcular totais
        total_mensal = sum(a.valor_mensal() for a in assinaturas)
        total_anual = sum(a.valor_anual() for a in assinaturas)
        
        # Média por usuário
        usuarios_com_assinaturas = User.objects.filter(
            assinaturas__status='ATIVA'
        ).distinct().count()
        
        if usuarios_com_assinaturas > 0:
            media_por_usuario = total_mensal / usuarios_com_assinaturas
        else:
            media_por_usuario = 0
        
        print("💰 FINANCEIRO (apenas assinaturas ativas)")
        print(f"   Total mensal: R$ {total_mensal:,.2f}")
        print(f"   Total anual: R$ {total_anual:,.2f}")
        print(f"   Média por usuário: R$ {media_por_usuario:,.2f}/mês")
        print()
        
        # Assinaturas mais caras
        mais_caras = assinaturas.order_by('-valor')[:5]
        print("   Top 5 assinaturas mais caras:")
        for ass in mais_caras:
            print(f"      • {ass.nome}: R$ {ass.valor} ({ass.ciclo_pagamento})")
        print()
    
    # ===== CICLOS DE PAGAMENTO =====
    ciclos = Assinatura.objects.filter(status='ATIVA').values(
        'ciclo_pagamento'
    ).annotate(total=Count('id'))
    
    if ciclos:
        print("📅 DISTRIBUIÇÃO POR CICLO DE PAGAMENTO")
        for ciclo in ciclos:
            print(f"   {ciclo['ciclo_pagamento']}: {ciclo['total']} assinaturas")
        print()
    
    # ===== USUÁRIOS COM MAIS ASSINATURAS =====
    usuarios_top = User.objects.annotate(
        total_assinaturas=Count('assinaturas', filter=Q(assinaturas__status='ATIVA'))
    ).filter(total_assinaturas__gt=0).order_by('-total_assinaturas')[:5]
    
    if usuarios_top:
        print("🏆 TOP 5 USUÁRIOS COM MAIS ASSINATURAS")
        for user in usuarios_top:
            gasto = sum(
                a.valor_mensal() 
                for a in user.assinaturas.filter(status='ATIVA')
            )
            print(f"   • {user.username}: {user.total_assinaturas} assinaturas "
                  f"(R$ {gasto:,.2f}/mês)")
        print()
    
    print("="*60 + "\n")


def listar_usuarios_detalhado():
    """Lista todos os usuários com suas assinaturas"""
    
    usuarios = User.objects.all()
    
    if not usuarios:
        print("\n⚠️  Nenhum usuário encontrado no banco de dados.\n")
        return
    
    print("\n" + "="*60)
    print("👥 DETALHES DOS USUÁRIOS")
    print("="*60 + "\n")
    
    for user in usuarios:
        assinaturas = user.assinaturas.filter(status='ATIVA')
        categorias = user.categorias.count()
        
        print(f"📌 {user.username} ({user.email})")
        print(f"   Categorias: {categorias}")
        print(f"   Assinaturas ativas: {assinaturas.count()}")
        
        if assinaturas:
            total_mensal = sum(a.valor_mensal() for a in assinaturas)
            print(f"   Gasto mensal: R$ {total_mensal:,.2f}")
            print(f"   Assinaturas:")
            for ass in assinaturas:
                cat_nome = ass.categoria.nome if ass.categoria else "Sem categoria"
                print(f"      • {ass.nome} ({cat_nome}): R$ {ass.valor} "
                      f"({ass.ciclo_pagamento})")
        print()
    
    print("="*60 + "\n")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--usuarios':
        listar_usuarios_detalhado()
    else:
        exibir_estatisticas()
