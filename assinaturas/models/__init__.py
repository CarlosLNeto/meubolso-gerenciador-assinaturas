"""
Módulo de models do app assinaturas
Organizados por entidade
"""

# Importar models
from .categoria import Categoria
from .assinatura import Assinatura

# Definir o que será exportado
__all__ = [
    'Categoria',
    'Assinatura',
]
