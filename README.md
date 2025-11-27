# Meu Bolso - Sistema de Gerenciamento de Assinaturas

Sistema web desenvolvido em Django para controle e gerenciamento de assinaturas e despesas recorrentes.

## Autores

- Carlos Alves Lavor Neto
- Eric Dias Perin

**Instituição:** Universidade do Estado do Amazonas (UEA)  
**Curso:** Engenharia da Computação  
**Disciplina:** Tecnologia Web  
**Ano:** 2024/2025

## Sobre o Projeto

Aplicação web para gerenciamento centralizado de assinaturas recorrentes, oferecendo controle financeiro através de dashboard interativo, categorização automática e análises de gastos mensais e anuais.

### Funcionalidades

- Sistema completo de autenticação (login, cadastro, logout)
- Dashboard com estatísticas em tempo real
- Gestão de assinaturas (CRUD completo)
- Categorização automática (9 categorias pré-definidas)
- Cálculo automático de próximas cobranças
- Análise de gastos mensais e anuais
- Alertas de vencimentos próximos
- Interface responsiva

## Tecnologias

- **Backend:** Django 5.2.7
- **Banco de Dados:** SQLite3
- **Frontend:** HTML5, CSS3, JavaScript
- **Python:** 3.8+

## Instalação

### Requisitos

- Python 3.8 ou superior
- pip

### Passos

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd ProjetoTecWeb

# Crie e ative o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Execute as migrações
python manage.py migrate

# Inicie o servidor
python manage.py runserver
```

Acesse: `http://127.0.0.1:8000`

## Estrutura do Projeto

```
ProjetoTecWeb/
├── assinaturas/          # Aplicação principal
│   ├── migrations/       # Migrações do banco
│   ├── models/          # Modelos (Categoria, Assinatura)
│   ├── views/           # Views (auth, dashboard, CRUD)
│   ├── templates/       # Templates HTML
│   ├── admin.py         # Configuração admin
│   ├── apps.py          # Configuração da app
│   └── signals.py       # Signals (categorias padrão)
├── meubolso/            # Configurações do projeto
├── docs/                # Documentação
├── scripts/             # Scripts utilitários
├── static/              # Arquivos estáticos
├── manage.py            # Gerenciador Django
├── requirements.txt     # Dependências
└── README.md           # Este arquivo
```

## Modelos de Dados

### Categoria
- Relacionamento com usuário (N:1)
- Campos: nome, descrição, cor
- 9 categorias criadas automaticamente para novos usuários

### Assinatura
- Relacionamentos: usuário (N:1), categoria (N:1, opcional)
- Campos principais: nome, valor, ciclo_pagamento, status
- Métodos: `valor_mensal()`, `valor_anual()`, `calcular_proxima_cobranca()`

### Categorias Padrão

Criadas automaticamente no cadastro:
- Streaming
- Entretenimento
- Lazer
- Produtividade
- Educação
- Saúde
- Delivery
- Restaurante
- Assinatura

## Administração

### Django Admin

```bash
# Criar superusuário
python manage.py createsuperuser

# Acessar admin
# URL: http://127.0.0.1:8000/admin/
```

Interface administrativa completa para gerenciar usuários, categorias e assinaturas.

## Scripts Utilitários

### Popular banco com dados de exemplo

```bash
python -m scripts.popular_banco            # Criar dados
python -m scripts.popular_banco --limpar   # Remover dados
```

Cria: 1 usuário (usuario_exemplo/senha123), 9 categorias, 12 assinaturas de exemplo

### Ver estatísticas do banco

```bash
python -m scripts.ver_estatisticas           # Estatísticas gerais
python -m scripts.ver_estatisticas --usuarios # Detalhes por usuário
```

## Comandos Úteis

```bash
# Migrações
python manage.py makemigrations
python manage.py migrate

# Servidor
python manage.py runserver

# Verificação
python manage.py check

# Testes
python manage.py test
```

## SEO e Boas Práticas

O projeto implementa técnicas modernas de SEO:

- Títulos únicos e descritivos por página
- Meta descriptions personalizadas
- URLs semânticas e RESTful
- Breadcrumbs para navegação
- HTML semântico com ARIA
- robots.txt para controle de indexação

Detalhes em: `docs/SEO_IMPLEMENTADO.md`

## Diagrama ER

Consulte o arquivo `docs/diagrama_er_mermaid.md` para visualização completa do diagrama entidade-relacionamento.

**Relacionamentos principais:**
- USUARIO 1:N CATEGORIA
- USUARIO 1:N ASSINATURA
- CATEGORIA 1:N ASSINATURA

## Licença

Projeto desenvolvido para fins acadêmicos.

---

Desenvolvido na Amazônia por Carlos Alves Lavor Neto e Eric Dias Perin
