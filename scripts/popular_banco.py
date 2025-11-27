#!/usr/bin/env python
"""
Script para popular o banco de dados com dados de exemplo
Útil para desenvolvimento e testes

Uso: python -m scripts.popular_banco [--limpar]
"""
import os
import sys
import django
from decimal import Decimal
from datetime import date, timedelta

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meubolso.settings')
django.setup()

from django.contrib.auth.models import User
from assinaturas.models import Categoria, Assinatura


def criar_dados_exemplo():
    """Cria dados de exemplo no banco de dados"""
    
    print("🚀 Iniciando população do banco de dados...\n")
    
    # Criar usuário de exemplo
    username = 'usuario_exemplo'
    
    if User.objects.filter(username=username).exists():
        print(f"ℹ️  Usuário '{username}' já existe. Removendo...")
        User.objects.filter(username=username).delete()
    
    print(f"👤 Criando usuário: {username}")
    user = User.objects.create_user(
        username=username,
        email='exemplo@meubolso.com',
        password='senha123',
        first_name='Usuário',
        last_name='Exemplo'
    )
    print(f"✅ Usuário criado: {user.username}\n")
    
    # As categorias já foram criadas automaticamente pelo signal
    categorias = Categoria.objects.filter(usuario=user)
    print(f"📁 Categorias disponíveis: {categorias.count()}")
    for cat in categorias:
        print(f"   • {cat.nome}")
    print()
    
    # Dados de assinaturas de exemplo
    assinaturas_exemplo = [
        {
            'nome': 'Netflix',
            'categoria': 'Streaming',
            'valor': Decimal('44.90'),
            'ciclo_pagamento': 'MENSAL',
            'dia_vencimento': 15,
            'descricao': 'Plano Premium 4 telas'
        },
        {
            'nome': 'Spotify',
            'categoria': 'Streaming',
            'valor': Decimal('21.90'),
            'ciclo_pagamento': 'MENSAL',
            'dia_vencimento': 10,
            'descricao': 'Plano Individual'
        },
        {
            'nome': 'Amazon Prime',
            'categoria': 'Streaming',
            'valor': Decimal('14.90'),
            'ciclo_pagamento': 'MENSAL',
            'dia_vencimento': 5,
            'descricao': 'Prime Video + Frete grátis'
        },
        {
            'nome': 'iFood Benefícios',
            'categoria': 'Delivery',
            'valor': Decimal('19.90'),
            'ciclo_pagamento': 'MENSAL',
            'dia_vencimento': 20,
            'descricao': 'Cashback e frete grátis'
        },
        {
            'nome': 'Clube O Globo',
            'categoria': 'Restaurante',
            'valor': Decimal('29.90'),
            'ciclo_pagamento': 'MENSAL',
            'dia_vencimento': 1,
            'descricao': 'Descontos em restaurantes parceiros'
        },
        {
            'nome': 'Duolingo Plus',
            'categoria': 'Educação',
            'valor': Decimal('34.90'),
            'ciclo_pagamento': 'MENSAL',
            'dia_vencimento': 25,
            'descricao': 'Sem anúncios e modo offline'
        },
        {
            'nome': 'GitHub Pro',
            'categoria': 'Produtividade',
            'valor': Decimal('4.00'),
            'ciclo_pagamento': 'MENSAL',
            'dia_vencimento': 12,
            'descricao': 'Repositórios privados ilimitados'
        },
        {
            'nome': 'ChatGPT Plus',
            'categoria': 'Produtividade',
            'valor': Decimal('20.00'),
            'ciclo_pagamento': 'MENSAL',
            'dia_vencimento': 8,
            'descricao': 'Acesso prioritário e GPT-4'
        },
        {
            'nome': 'Strava Premium',
            'categoria': 'Saúde',
            'valor': Decimal('24.99'),
            'ciclo_pagamento': 'MENSAL',
            'dia_vencimento': 18,
            'descricao': 'Análises avançadas de treinos'
        },
        {
            'nome': 'Xbox Game Pass',
            'categoria': 'Entretenimento',
            'valor': Decimal('45.00'),
            'ciclo_pagamento': 'MENSAL',
            'dia_vencimento': 22,
            'descricao': 'Catálogo de jogos ilimitado'
        },
        {
            'nome': 'Adobe Creative Cloud',
            'categoria': 'Produtividade',
            'valor': Decimal('254.00'),
            'ciclo_pagamento': 'MENSAL',
            'dia_vencimento': 3,
            'descricao': 'Todos os apps Adobe'
        },
        {
            'nome': 'YouTube Premium',
            'categoria': 'Streaming',
            'valor': Decimal('20.90'),
            'ciclo_pagamento': 'MENSAL',
            'dia_vencimento': 7,
            'descricao': 'Sem anúncios + YouTube Music'
        },
    ]
    
    print(f"📦 Criando {len(assinaturas_exemplo)} assinaturas de exemplo...\n")
    
    for ass_data in assinaturas_exemplo:
        # Buscar categoria
        categoria = categorias.filter(nome=ass_data['categoria']).first()
        
        # Calcular data de primeira cobrança (mês passado)
        hoje = date.today()
        dia = ass_data['dia_vencimento']
        if dia > hoje.day:
            # Se o dia ainda não passou neste mês, usar mês passado
            if hoje.month == 1:
                data_primeira = date(hoje.year - 1, 12, dia)
            else:
                data_primeira = date(hoje.year, hoje.month - 1, dia)
        else:
            data_primeira = date(hoje.year, hoje.month, dia)
        
        # Criar assinatura
        assinatura = Assinatura.objects.create(
            usuario=user,
            categoria=categoria,
            nome=ass_data['nome'],
            descricao=ass_data['descricao'],
            valor=ass_data['valor'],
            ciclo_pagamento=ass_data['ciclo_pagamento'],
            dia_vencimento=ass_data['dia_vencimento'],
            data_primeira_cobranca=data_primeira,
            status='ATIVA'
        )
        
        print(f"✅ {assinatura.nome} - R$ {assinatura.valor} ({assinatura.ciclo_pagamento})")
    
    # Estatísticas finais
    print(f"\n📊 RESUMO:")
    print(f"   • Usuário: {user.username}")
    print(f"   • Email: {user.email}")
    print(f"   • Senha: senha123")
    print(f"   • Categorias: {categorias.count()}")
    
    assinaturas = Assinatura.objects.filter(usuario=user)
    print(f"   • Assinaturas: {assinaturas.count()}")
    
    total_mensal = sum(a.valor_mensal() for a in assinaturas)
    total_anual = sum(a.valor_anual() for a in assinaturas)
    
    print(f"   • Gasto mensal: R$ {total_mensal:.2f}")
    print(f"   • Gasto anual: R$ {total_anual:.2f}")
    
    print(f"\n✨ Banco de dados populado com sucesso!")
    print(f"\n💡 Dica: Faça login com o usuário 'usuario_exemplo' e senha 'senha123'")
    print(f"   URL: http://127.0.0.1:8000/login/\n")


def limpar_dados_exemplo():
    """Remove dados de exemplo do banco de dados"""
    
    username = 'usuario_exemplo'
    
    if User.objects.filter(username=username).exists():
        print(f"🗑️  Removendo usuário e dados de exemplo...")
        User.objects.filter(username=username).delete()
        print(f"✅ Dados removidos com sucesso!\n")
    else:
        print(f"ℹ️  Nenhum dado de exemplo encontrado.\n")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--limpar':
        limpar_dados_exemplo()
    else:
        criar_dados_exemplo()
