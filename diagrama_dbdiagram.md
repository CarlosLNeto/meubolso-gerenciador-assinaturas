# Diagrama ER - Meu Bolso (dbdiagram.io)

## 🎯 Como usar:

1. Acesse: **https://dbdiagram.io/**
2. Copie TODO o código SQL abaixo
3. Cole no editor do site
4. O diagrama será gerado automaticamente!
5. Exporte como PNG, PDF ou SVG

---

## 📋 Código para dbdiagram.io:

```sql
// Diagrama ER - Meu Bolso
// Sistema de Gerenciamento de Assinaturas e Despesas Recorrentes
// Desenvolvido por: Carlos Alves Lavor Neto e Eric Dias Perin
// UEA - Engenharia da Computação - Tecnologia Web

Table Usuario {
  id integer [pk, increment, note: 'Primary Key']
  username varchar(150) [unique, not null, note: 'Nome de usuário único']
  email varchar(254) [unique, not null, note: 'Email único']
  password varchar(128) [not null, note: 'Senha criptografada (hash)']
  first_name varchar(150) [note: 'Nome']
  last_name varchar(150) [note: 'Sobrenome']
  date_joined datetime [not null, default: `now()`, note: 'Data de cadastro']
  is_active boolean [not null, default: true, note: 'Usuário ativo?']
  
  Note: '''
    Django User Model
    Sistema de autenticação de usuários
    Permite login e controle de acesso
  '''
}

Table Categoria {
  id integer [pk, increment, note: 'Primary Key']
  usuario_id integer [ref: > Usuario.id, not null, note: 'Dono da categoria']
  nome varchar(50) [not null, note: 'Ex: Entretenimento, Trabalho']
  descricao text [note: 'Descrição opcional da categoria']
  cor varchar(7) [not null, default: '#6366f1', note: 'Cor em hexadecimal para UI']
  data_criacao datetime [not null, default: `now()`, note: 'Data de criação']
  
  indexes {
    (usuario_id, nome) [unique, name: 'unique_categoria_por_usuario']
  }
  
  Note: '''
    Categorias para organizar assinaturas
    Exemplos: Streaming, Software, Saúde, Educação
    Cada usuário tem suas próprias categorias
  '''
}

Table Assinatura {
  id integer [pk, increment, note: 'Primary Key']
  usuario_id integer [ref: > Usuario.id, not null, note: 'Dono da assinatura']
  categoria_id integer [ref: > Categoria.id, null, note: 'Categoria opcional']
  nome varchar(100) [not null, note: 'Ex: Netflix, Spotify, Gym']
  descricao text [note: 'Detalhes sobre a assinatura']
  valor decimal(10,2) [not null, note: 'Valor da assinatura']
  moeda varchar(3) [not null, default: 'BRL', note: 'Código da moeda']
  ciclo_pagamento varchar(20) [not null, note: 'MENSAL | TRIMESTRAL | SEMESTRAL | ANUAL']
  data_primeira_cobranca date [not null, note: 'Data da primeira cobrança']
  data_proxima_cobranca date [not null, note: 'Próxima data de pagamento']
  dia_vencimento integer [note: 'Dia do vencimento (1-31)']
  status varchar(20) [not null, default: 'ATIVA', note: 'ATIVA | PAUSADA | CANCELADA']
  data_criacao datetime [not null, default: `now()`, note: 'Data de criação']
  data_atualizacao datetime [not null, default: `now()`, note: 'Última atualização']
  observacoes text [note: 'Notas adicionais']
  
  indexes {
    usuario_id [name: 'idx_assinatura_usuario']
    categoria_id [name: 'idx_assinatura_categoria']
    status [name: 'idx_assinatura_status']
    data_proxima_cobranca [name: 'idx_proxima_cobranca']
  }
  
  Note: '''
    Assinaturas e serviços recorrentes
    Calcula automaticamente próximas cobranças
    Métodos: valor_mensal(), valor_anual(), dias_ate_proxima_cobranca()
  '''
}

// ========================================
// RELACIONAMENTOS
// ========================================

// Usuario → Categoria (1:N)
// Um usuário pode ter várias categorias
// Ao deletar usuário, deletar todas categorias
Ref: Usuario.id < Categoria.usuario_id [delete: cascade]

// Usuario → Assinatura (1:N)
// Um usuário pode ter várias assinaturas
// Ao deletar usuário, deletar todas assinaturas
Ref: Usuario.id < Assinatura.usuario_id [delete: cascade]

// Categoria → Assinatura (1:N)
// Uma categoria pode ter várias assinaturas
// Ao deletar categoria, manter assinatura sem categoria
Ref: Categoria.id < Assinatura.categoria_id [delete: set null]
```

---

## 📊 O que o diagrama mostra:

### Entidades (Tabelas):
- **USUARIO**: Usuários do sistema (autenticação Django)
- **CATEGORIA**: Categorias para organizar assinaturas
- **ASSINATURA**: Assinaturas e serviços recorrentes

### Relacionamentos:
- 1 Usuário → N Categorias (um usuário pode ter várias categorias)
- 1 Usuário → N Assinaturas (um usuário pode ter várias assinaturas)
- 1 Categoria → N Assinaturas (uma categoria pode ter várias assinaturas)

### Regras de Negócio:
- ✅ Se deletar usuário → deleta suas categorias e assinaturas (CASCADE)
- ✅ Se deletar categoria → assinaturas ficam sem categoria (SET NULL)
- ✅ Nome de categoria é único por usuário
- ✅ Valor da assinatura deve ser > 0
- ✅ Cálculos automáticos de próxima cobrança

---

## 🎨 Dica de cores no dbdiagram.io:

Após gerar o diagrama, você pode personalizar as cores:

1. Clique em uma tabela
2. No painel direito, escolha "Table Color"
3. Sugestões:
   - **Usuario**: Azul (#4A90E2)
   - **Categoria**: Verde (#50C878)
   - **Assinatura**: Vermelho (#FF6B6B)

---

## 💾 Como exportar:

1. Clique em "Export" no menu superior
2. Escolha o formato:
   - **PNG**: Para apresentações e documentos
   - **PDF**: Para impressão
   - **SQL**: Para gerar o schema do banco

---

**Desenvolvido com ❤️ por Carlos Alves Lavor Neto e Eric Dias Perin**
