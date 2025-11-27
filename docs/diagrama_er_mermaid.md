# Diagrama ER - Meu Bolso (Formato Mermaid)

Este diagrama pode ser visualizado diretamente no GitHub, VS Code (com extensão Mermaid), ou em https://mermaid.live

## Diagrama Entidade-Relacionamento

```mermaid
erDiagram
    USUARIO ||--o{ CATEGORIA : possui
    USUARIO ||--o{ ASSINATURA : possui
    CATEGORIA ||--o{ ASSINATURA : categoriza

    USUARIO {
        int id PK
        string username UK "Único, obrigatório"
        string email UK "Único, obrigatório"
        string password "Hash, obrigatório"
        string first_name "Opcional"
        string last_name "Opcional"
        datetime date_joined "Auto"
        boolean is_active "Default true"
    }

    CATEGORIA {
        int id PK
        int usuario_id FK "Obrigatório"
        string nome "Max 50 chars"
        text descricao "Opcional"
        string cor "Hex color, default #6366f1"
        datetime data_criacao "Auto"
    }

    ASSINATURA {
        int id PK
        int usuario_id FK "Obrigatório"
        int categoria_id FK "Opcional, SET_NULL"
        string nome "Max 100 chars"
        text descricao "Opcional"
        decimal valor "10 dígitos, 2 decimais"
        string moeda "Default BRL"
        string ciclo_pagamento "MENSAL|ANUAL|TRIMESTRAL|SEMESTRAL"
        date data_primeira_cobranca
        date data_proxima_cobranca
        int dia_vencimento "1-31, opcional"
        string status "ATIVA|CANCELADA|PAUSADA"
        datetime data_criacao "Auto"
        datetime data_atualizacao "Auto"
        text observacoes "Opcional"
    }
```

## Diagrama de Classes (UML)

```mermaid
classDiagram
    class Usuario {
        +int id
        +string username
        +string email
        +string password
        +string first_name
        +string last_name
        +datetime date_joined
        +boolean is_active
    }

    class Categoria {
        +int id
        +int usuario_id
        +string nome
        +string descricao
        +string cor
        +datetime data_criacao
        +total_assinaturas() int
        +total_valor_mensal() decimal
    }

    class Assinatura {
        +int id
        +int usuario_id
        +int categoria_id
        +string nome
        +string descricao
        +decimal valor
        +string moeda
        +string ciclo_pagamento
        +date data_primeira_cobranca
        +date data_proxima_cobranca
        +int dia_vencimento
        +string status
        +datetime data_criacao
        +datetime data_atualizacao
        +string observacoes
        +calcular_proxima_cobranca() date
        +valor_mensal() decimal
        +valor_anual() decimal
        +dias_ate_proxima_cobranca() int
        +esta_vencida() boolean
        +atualizar_proxima_cobranca() void
    }

    Usuario "1" --> "0..*" Categoria : possui
    Usuario "1" --> "0..*" Assinatura : possui
    Categoria "0..1" --> "0..*" Assinatura : categoriza
```

## Visualização Online

Para visualizar estes diagramas de forma interativa:

1. **Mermaid Live Editor**: https://mermaid.live
   - Cole o código Mermaid acima
   - Visualize, edite e exporte como PNG/SVG

2. **GitHub**: Este arquivo já renderiza automaticamente no GitHub

3. **VS Code**: Instale a extensão "Markdown Preview Mermaid Support"

## Regras de Negócio Ilustradas

```mermaid
graph TD
    A[Usuário cria Assinatura] --> B{Tem Categoria?}
    B -->|Sim| C[Associar Categoria]
    B -->|Não| D[Sem Categoria]
    C --> E[Calcular Próxima Cobrança]
    D --> E
    E --> F{Ciclo de Pagamento}
    F -->|Mensal| G[+1 mês]
    F -->|Trimestral| H[+3 meses]
    F -->|Semestral| I[+6 meses]
    F -->|Anual| J[+12 meses]
    G --> K[Salvar Assinatura]
    H --> K
    I --> K
    J --> K
```

## Fluxo de Atualização de Cobrança

```mermaid
sequenceDiagram
    participant U as Usuário
    participant S as Sistema
    participant A as Assinatura
    participant D as Database
    
    U->>S: Registra pagamento
    S->>A: atualizar_proxima_cobranca()
    A->>A: Calcular nova data baseada em ciclo
    A->>D: Salvar nova data_proxima_cobranca
    D-->>S: Confirmação
    S-->>U: Próxima cobrança atualizada
```
