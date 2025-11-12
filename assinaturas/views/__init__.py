"""
Módulo de views do app assinaturas
Organizadas por responsabilidade
"""

# Importar views de autenticação
from .auth_views import (
    login_view,
    signup_view,
    logout_view,
)

# Importar views do dashboard
from .dashboard_views import (
    dashboard,
)

# Importar views de assinaturas
from .assinatura_views import (
    listar_assinaturas,
    criar_assinatura,
    editar_assinatura,
    deletar_assinatura,
)

# Importar views de categorias
from .categoria_views import (
    listar_categorias,
    criar_categoria,
    editar_categoria,
    deletar_categoria,
)

# Manter compatibilidade com imports antigos
assinaturas_view = listar_assinaturas
categorias_view = listar_categorias

__all__ = [
    # Auth
    'login_view',
    'signup_view',
    'logout_view',
    # Dashboard
    'dashboard',
    # Assinaturas
    'listar_assinaturas',
    'criar_assinatura',
    'editar_assinatura',
    'deletar_assinatura',
    'assinaturas_view',  # Alias para compatibilidade
    # Categorias
    'listar_categorias',
    'criar_categoria',
    'editar_categoria',
    'deletar_categoria',
    'categorias_view',  # Alias para compatibilidade
]
