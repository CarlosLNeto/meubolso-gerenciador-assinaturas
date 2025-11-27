"""
Script de demonstração dos models do projeto Meu Bolso
Execute com: python manage.py shell < exemplo_uso_models.py
"""

from django.contrib.auth.models import User
from assinaturas.models import Categoria, Assinatura
from datetime import date, timedelta

print("=" * 60)
print("DEMONSTRAÇÃO DOS MODELS - MEU BOLSO")
print("=" * 60)

# 1. Criar um usuário de teste (se não existir)
user, created = User.objects.get_or_create(
    username='usuario_teste',
    defaults={
        'email': 'teste@example.com',
        'first_name': 'João',
        'last_name': 'Silva'
    }
)

if created:
    user.set_password('senha123')
    user.save()
    print(f"\n✓ Usuário criado: {user.username}")
else:
    print(f"\n✓ Usuário já existe: {user.username}")

# 2. Criar categorias
categorias_data = [
    {'nome': 'Entretenimento', 'descricao': 'Streaming e lazer', 'cor': '#FF6B6B'},
    {'nome': 'Trabalho', 'descricao': 'Ferramentas profissionais', 'cor': '#4ECDC4'},
    {'nome': 'Educação', 'descricao': 'Cursos e aprendizado', 'cor': '#FFE66D'},
]

print("\n" + "=" * 60)
print("CRIANDO CATEGORIAS")
print("=" * 60)

for cat_data in categorias_data:
    categoria, created = Categoria.objects.get_or_create(
        usuario=user,
        nome=cat_data['nome'],
        defaults={
            'descricao': cat_data['descricao'],
            'cor': cat_data['cor']
        }
    )
    status = "criada" if created else "já existe"
    print(f"- {categoria.nome}: {status}")

# 3. Criar assinaturas
assinaturas_data = [
    {
        'nome': 'Netflix',
        'categoria': 'Entretenimento',
        'valor': 55.90,
        'ciclo_pagamento': 'MENSAL',
        'data_primeira_cobranca': date.today(),
        'descricao': 'Plano Premium'
    },
    {
        'nome': 'Spotify',
        'categoria': 'Entretenimento',
        'valor': 21.90,
        'ciclo_pagamento': 'MENSAL',
        'data_primeira_cobranca': date.today() + timedelta(days=5),
        'descricao': 'Plano Individual'
    },
    {
        'nome': 'Adobe Creative Cloud',
        'categoria': 'Trabalho',
        'valor': 299.00,
        'ciclo_pagamento': 'MENSAL',
        'data_primeira_cobranca': date.today() + timedelta(days=10),
        'descricao': 'Plano Completo'
    },
    {
        'nome': 'Udemy Pro',
        'categoria': 'Educação',
        'valor': 599.00,
        'ciclo_pagamento': 'ANUAL',
        'data_primeira_cobranca': date.today() + timedelta(days=30),
        'descricao': 'Assinatura anual'
    },
]

print("\n" + "=" * 60)
print("CRIANDO ASSINATURAS")
print("=" * 60)

for ass_data in assinaturas_data:
    categoria = Categoria.objects.get(usuario=user, nome=ass_data['categoria'])
    
    assinatura, created = Assinatura.objects.get_or_create(
        usuario=user,
        nome=ass_data['nome'],
        defaults={
            'categoria': categoria,
            'valor': ass_data['valor'],
            'ciclo_pagamento': ass_data['ciclo_pagamento'],
            'data_primeira_cobranca': ass_data['data_primeira_cobranca'],
            'data_proxima_cobranca': ass_data['data_primeira_cobranca'],
            'descricao': ass_data['descricao'],
        }
    )
    status = "criada" if created else "já existe"
    print(f"- {assinatura.nome}: {status}")

# 4. Demonstrar funcionalidades
print("\n" + "=" * 60)
print("INFORMAÇÕES DAS ASSINATURAS")
print("=" * 60)

assinaturas = Assinatura.objects.filter(usuario=user, status='ATIVA')

for ass in assinaturas:
    print(f"\n📱 {ass.nome}")
    print(f"   Categoria: {ass.categoria.nome if ass.categoria else 'Sem categoria'}")
    print(f"   Valor: R$ {ass.valor:,.2f} ({ass.get_ciclo_pagamento_display()})")
    print(f"   Valor Mensal: R$ {ass.valor_mensal():,.2f}")
    print(f"   Valor Anual: R$ {ass.valor_anual():,.2f}")
    print(f"   Próxima cobrança: {ass.data_proxima_cobranca.strftime('%d/%m/%Y')}")
    print(f"   Dias até cobrança: {ass.dias_ate_proxima_cobranca()}")

# 5. Calcular totais
print("\n" + "=" * 60)
print("RESUMO FINANCEIRO")
print("=" * 60)

total_mensal = sum(ass.valor_mensal() for ass in assinaturas)
total_anual = sum(ass.valor_anual() for ass in assinaturas)

print(f"\n💰 Total Mensal: R$ {total_mensal:,.2f}")
print(f"💰 Total Anual: R$ {total_anual:,.2f}")
print(f"📊 Total de Assinaturas Ativas: {assinaturas.count()}")

# 6. Gastos por categoria
print("\n" + "=" * 60)
print("GASTOS POR CATEGORIA")
print("=" * 60)

categorias = Categoria.objects.filter(usuario=user)
for cat in categorias:
    ass_categoria = assinaturas.filter(categoria=cat)
    if ass_categoria.exists():
        total_cat = sum(ass.valor_mensal() for ass in ass_categoria)
        print(f"\n🏷️  {cat.nome}")
        print(f"   Assinaturas: {ass_categoria.count()}")
        print(f"   Total Mensal: R$ {total_cat:,.2f}")

print("\n" + "=" * 60)
print("DEMONSTRAÇÃO CONCLUÍDA!")
print("=" * 60)
print("\nPara visualizar no Django Admin:")
print("1. Crie um superusuário: python manage.py createsuperuser")
print("2. Inicie o servidor: python manage.py runserver")
print("3. Acesse: http://127.0.0.1:8000/admin/")
print("=" * 60)
