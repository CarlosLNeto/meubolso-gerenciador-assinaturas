from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


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


class Assinatura(models.Model):
    """
    Modelo principal para gerenciar assinaturas/despesas recorrentes.
    """
    
    CICLO_CHOICES = [
        ('MENSAL', 'Mensal'),
        ('TRIMESTRAL', 'Trimestral'),
        ('SEMESTRAL', 'Semestral'),
        ('ANUAL', 'Anual'),
    ]
    
    STATUS_CHOICES = [
        ('ATIVA', 'Ativa'),
        ('PAUSADA', 'Pausada'),
        ('CANCELADA', 'Cancelada'),
    ]

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assinaturas',
        verbose_name='Usuário'
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assinaturas',
        verbose_name='Categoria'
    )
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome da Assinatura'
    )
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descrição'
    )
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Valor'
    )
    moeda = models.CharField(
        max_length=3,
        default='BRL',
        verbose_name='Moeda'
    )
    ciclo_pagamento = models.CharField(
        max_length=20,
        choices=CICLO_CHOICES,
        verbose_name='Ciclo de Pagamento'
    )
    data_primeira_cobranca = models.DateField(
        verbose_name='Data da Primeira Cobrança'
    )
    data_proxima_cobranca = models.DateField(
        verbose_name='Data da Próxima Cobrança'
    )
    dia_vencimento = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(31)],
        null=True,
        blank=True,
        verbose_name='Dia do Vencimento',
        help_text='Dia do mês em que ocorre a cobrança (1-31)'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ATIVA',
        verbose_name='Status'
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Criação'
    )
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name='Data de Atualização'
    )
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observações'
    )

    class Meta:
        verbose_name = 'Assinatura'
        verbose_name_plural = 'Assinaturas'
        ordering = ['-data_criacao']
        indexes = [
            models.Index(fields=['usuario', 'status']),
            models.Index(fields=['data_proxima_cobranca']),
            models.Index(fields=['categoria']),
        ]

    def __str__(self):
        return f"{self.nome} - R$ {self.valor} ({self.get_ciclo_pagamento_display()})"

    def save(self, *args, **kwargs):
        """
        Override do método save para calcular automaticamente 
        a próxima cobrança se não foi definida
        """
        if not self.data_proxima_cobranca:
            self.data_proxima_cobranca = self.calcular_proxima_cobranca(
                self.data_primeira_cobranca
            )
        
        if not self.dia_vencimento:
            self.dia_vencimento = self.data_primeira_cobranca.day
            
        super().save(*args, **kwargs)

    def calcular_proxima_cobranca(self, data_base=None):
        """
        Calcula a próxima data de cobrança baseada no ciclo de pagamento
        """
        if data_base is None:
            data_base = self.data_proxima_cobranca or self.data_primeira_cobranca
        
        hoje = date.today()
        
        if data_base >= hoje:
            return data_base
        
        if self.ciclo_pagamento == 'MENSAL':
            delta = relativedelta(months=1)
        elif self.ciclo_pagamento == 'TRIMESTRAL':
            delta = relativedelta(months=3)
        elif self.ciclo_pagamento == 'SEMESTRAL':
            delta = relativedelta(months=6)
        elif self.ciclo_pagamento == 'ANUAL':
            delta = relativedelta(years=1)
        else:
            delta = relativedelta(months=1)
        
        proxima_data = data_base
        while proxima_data < hoje:
            proxima_data += delta
        
        return proxima_data

    def valor_mensal(self):
        """
        Converte o valor da assinatura para base mensal para cálculos
        """
        if self.ciclo_pagamento == 'MENSAL':
            return self.valor
        elif self.ciclo_pagamento == 'TRIMESTRAL':
            return self.valor / 3
        elif self.ciclo_pagamento == 'SEMESTRAL':
            return self.valor / 6
        elif self.ciclo_pagamento == 'ANUAL':
            return self.valor / 12
        return self.valor

    def valor_anual(self):
        """
        Converte o valor da assinatura para base anual
        """
        if self.ciclo_pagamento == 'MENSAL':
            return self.valor * 12
        elif self.ciclo_pagamento == 'TRIMESTRAL':
            return self.valor * 4
        elif self.ciclo_pagamento == 'SEMESTRAL':
            return self.valor * 2
        elif self.ciclo_pagamento == 'ANUAL':
            return self.valor
        return self.valor * 12

    def dias_ate_proxima_cobranca(self):
        """
        Retorna quantos dias faltam até a próxima cobrança
        """
        hoje = date.today()
        if self.data_proxima_cobranca >= hoje:
            return (self.data_proxima_cobranca - hoje).days
        return 0

    def esta_vencida(self):
        """
        Verifica se a assinatura tem cobrança vencida
        """
        return self.data_proxima_cobranca < date.today()

    def atualizar_proxima_cobranca(self):
        """
        Atualiza a data da próxima cobrança para o próximo ciclo
        """
        self.data_proxima_cobranca = self.calcular_proxima_cobranca(
            self.data_proxima_cobranca
        )
        self.save()
