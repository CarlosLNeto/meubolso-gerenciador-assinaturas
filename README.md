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

# Crie um superusuário (opcional)
python manage.py createsuperuser

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
├── docs/                # Documentação (diagrama ER)
├── scripts/             # Scripts utilitários
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

## Gerenciamento do Banco de Dados

### Django Admin

```bash
# Criar superusuário
python manage.py createsuperuser

# Acessar admin
# URL: http://127.0.0.1:8000/admin/
```

### Django Shell

```bash
python manage.py shell

# Exemplos de consultas
>>> from django.contrib.auth.models import User
>>> from assinaturas.models import Categoria, Assinatura

# Listar usuários
>>> User.objects.all()

# Assinaturas ativas de um usuário
>>> user = User.objects.get(username='seu_usuario')
>>> Assinatura.objects.filter(usuario=user, status='ATIVA')

# Total de gastos mensais
>>> total = sum(a.valor_mensal() for a in user.assinaturas.filter(status='ATIVA'))
```

### SQLite CLI

```bash
sqlite3 db.sqlite3

.tables                                    # Listar tabelas
SELECT * FROM auth_user;                   # Listar usuários
SELECT * FROM assinaturas_categoria;       # Listar categorias
SELECT * FROM assinaturas_assinatura;      # Listar assinaturas
.quit
```

### DB Browser for SQLite

Interface gráfica para visualização: https://sqlitebrowser.org/

### Backup e Restore

```bash
# Backup
python manage.py dumpdata > backup.json
cp db.sqlite3 db.sqlite3.backup

# Restore
python manage.py loaddata backup.json
```

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
python manage.py runserver 8080  # Porta alternativa

# Verificação
python manage.py check

# Testes
python manage.py test

# Coletar arquivos estáticos
python manage.py collectstatic
```

## Diagrama ER

Consulte o arquivo `docs/diagrama_er_mermaid.md` para visualização completa do diagrama entidade-relacionamento.

**Relacionamentos principais:**
- USUARIO 1:N CATEGORIA
- USUARIO 1:N ASSINATURA
- CATEGORIA 1:N ASSINATURA

## Desenvolvimento

### Ambiente de Desenvolvimento

```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Instalar/Atualizar dependências
pip install -r requirements.txt --upgrade

# Verificar instalação
python manage.py check
```

### Estrutura de Branches (recomendado)

- `main`: Versão estável
- `develop`: Desenvolvimento
- `feature/*`: Novas funcionalidades

## Licença

Projeto desenvolvido para fins acadêmicos.

---

Desenvolvido na Amazônia por Carlos Alves Lavor Neto e Eric Dias Perin
