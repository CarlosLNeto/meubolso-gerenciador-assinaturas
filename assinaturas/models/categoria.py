"""
Modelo de Categoria para organização de assinaturas
"""
from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    """
    Modelo para categorização de assinaturas.
    Cada usuário pode criar suas próprias categorias personalizadas.
    """
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='categorias',
        verbose_name='Usuário'
    )
    nome = models.CharField(
        max_length=50,
        verbose_name='Nome da Categoria'
    )
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descrição'
    )
    cor = models.CharField(
        max_length=7,
        default='#6366f1',
        verbose_name='Cor (Hexadecimal)',
        help_text='Formato: #RRGGBB'
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Criação'
    )

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        unique_together = ['usuario', 'nome']
        ordering = ['nome']
        indexes = [
            models.Index(fields=['usuario', 'nome']),
        ]

    def __str__(self):
        return f"{self.nome} ({self.usuario.username})"

    def total_assinaturas(self):
        """Retorna o número total de assinaturas nesta categoria"""
        return self.assinaturas.filter(status='ATIVA').count()
