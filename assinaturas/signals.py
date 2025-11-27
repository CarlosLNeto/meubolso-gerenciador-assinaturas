"""
Signals para criação automática de categorias padrão
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Categoria


# Categorias padrão que serão criadas para novos usuários
CATEGORIAS_PADRAO = [
    {
        "nome": "Streaming",
        "descricao": "Serviços de streaming de vídeo, música e podcasts",
        "cor": "#e74c3c",
    },
    {
        "nome": "Entretenimento",
        "descricao": "Jogos, revistas e outros serviços de entretenimento",
        "cor": "#9b59b6",
    },
    {"nome": "Lazer", "descricao": "Atividades de lazer e recreação", "cor": "#f368e0"},
    {
        "nome": "Produtividade",
        "descricao": "Ferramentas de trabalho e produtividade",
        "cor": "#3498db",
    },
    {
        "nome": "Educação",
        "descricao": "Cursos online e plataformas educacionais",
        "cor": "#2ecc71",
    },
    {
        "nome": "Saúde",
        "descricao": "Aplicativos de saúde, fitness e bem-estar",
        "cor": "#e67e22",
    },
    {
        "nome": "Delivery",
        "descricao": "Serviços de entrega e delivery de alimentos",
        "cor": "#f39c12",
    },
    {"nome": "Restaurante", "descricao": "Gastos em restaurantes", "cor": "#d35400"},
    {
        "nome": "Assinatura",
        "descricao": "Outras assinaturas diversas",
        "cor": "#95a5a6",
    },
]


@receiver(post_save, sender=User)
def criar_categorias_padrao(sender, instance, created, **kwargs):
    """
    Cria categorias padrão quando um novo usuário é criado
    """
    if created:
        # Criar categorias padrão para o novo usuário
        for categoria_data in CATEGORIAS_PADRAO:
            Categoria.objects.create(
                usuario=instance,
                nome=categoria_data["nome"],
                descricao=categoria_data["descricao"],
                cor=categoria_data["cor"],
            )
