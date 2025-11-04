# Diagrama Entidade-Relacionamento (ER)
## Sistema: Meu Bolso - Gerenciador de Assinaturas

### Entidades e Atributos

#### 1. **Usuario** (extends Django User model)
- **id** (PK, Integer, Auto-increment)
- username (String, Unique, Required)
- email (String, Unique, Required)
- password (String, Hashed, Required)
- first_name (String, Optional)
- last_name (String, Optional)
- date_joined (DateTime, Auto)
- is_active (Boolean, Default: True)

#### 2. **Categoria**
- **id** (PK, Integer, Auto-increment)
- **usuario_id** (FK → Usuario)
- nome (String, Max 50, Required)
  - Exemplos: "Entretenimento", "Trabalho", "Educação", "Saúde", "Outros"
- descricao (Text, Optional)
- cor (String, Max 7, Default: "#6366f1")
  - Formato hexadecimal para visualização no dashboard
- data_criacao (DateTime, Auto)

#### 3. **Assinatura**
- **id** (PK, Integer, Auto-increment)
- **usuario_id** (FK → Usuario)
- **categoria_id** (FK → Categoria, Optional)
- nome (String, Max 100, Required)
  - Exemplos: "Netflix", "Spotify", "Academia", "Adobe Creative Cloud"
- descricao (Text, Optional)
- valor (Decimal, Max 10 dígitos, 2 casas decimais, Required)
  - Valor da assinatura em reais
- moeda (String, Max 3, Default: "BRL")
- ciclo_pagamento (String, Choices, Required)
  - Opções: "MENSAL", "ANUAL", "TRIMESTRAL", "SEMESTRAL"
- data_primeira_cobranca (Date, Required)
- data_proxima_cobranca (Date, Required)
- dia_vencimento (Integer, Range 1-31, Optional)
- status (String, Choices, Default: "ATIVA")
  - Opções: "ATIVA", "CANCELADA", "PAUSADA"
- data_criacao (DateTime, Auto)
- data_atualizacao (DateTime, Auto)
- observacoes (Text, Optional)

### Relacionamentos

```
Usuario (1) ──────< (N) Categoria
  │
  │  Um usuário pode ter várias categorias
  │  Uma categoria pertence a um único usuário
  │
  └──────< (N) Assinatura
       │
       │  Um usuário pode ter várias assinaturas
       │  Uma assinatura pertence a um único usuário
       │

Categoria (1) ──────< (N) Assinatura
       │
       │  Uma categoria pode ter várias assinaturas
       │  Uma assinatura pode ter uma categoria (opcional)
```

### Diagrama Visual (ASCII)

```
┌─────────────────┐
│    Usuario      │
├─────────────────┤
│ PK id           │
│    username     │
│    email        │
│    password     │
│    first_name   │
│    last_name    │
│    date_joined  │
└────────┬────────┘
         │
         │ 1:N
         │
    ┌────┴────────────────────┐
    │                         │
    │                         │
┌───▼──────────┐      ┌──────▼──────────┐
│  Categoria   │      │  Assinatura     │
├──────────────┤      ├─────────────────┤
│ PK id        │ 1:N  │ PK id           │
│ FK usuario_id│◄─────┤ FK usuario_id   │
│    nome      │      │ FK categoria_id │
│    descricao │      │    nome         │
│    cor       │      │    descricao    │
│ data_criacao │      │    valor        │
└──────────────┘      │    moeda        │
                      │    ciclo_pag... │
                      │    data_prim... │
                      │    data_prox... │
                      │    dia_vencim.. │
                      │    status       │
                      │    data_criacao │
                      │    data_atual...│
                      │    observacoes  │
                      └─────────────────┘
```

### Regras de Negócio

1. **Cascata de Exclusão**:
   - Se um usuário for deletado, todas as suas categorias e assinaturas são deletadas
   - Se uma categoria for deletada, as assinaturas associadas ficam sem categoria (SET_NULL)

2. **Validações**:
   - O valor da assinatura deve ser maior que 0
   - A data da próxima cobrança deve ser igual ou posterior à data atual
   - O nome da categoria deve ser único por usuário
   - O ciclo de pagamento determina automaticamente a próxima cobrança

3. **Cálculos Automáticos**:
   - Custo mensal total: Soma de todas assinaturas ativas convertidas para base mensal
   - Custo anual total: Soma de todas assinaturas ativas convertidas para base anual
   - Próximas cobranças: Lista ordenada por data_proxima_cobranca

### Índices Recomendados

- Usuario: email (único), username (único)
- Categoria: (usuario_id, nome) - índice composto único
- Assinatura: usuario_id, categoria_id, status, data_proxima_cobranca
