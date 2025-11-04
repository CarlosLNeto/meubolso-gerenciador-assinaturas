from django.contrib import admin
from .models import Categoria, Assinatura


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'usuario', 'cor', 'total_assinaturas', 'data_criacao']
    list_filter = ['usuario', 'data_criacao']
    search_fields = ['nome', 'descricao', 'usuario__username']
    readonly_fields = ['data_criacao']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('usuario', 'nome', 'descricao')
        }),
        ('Aparência', {
            'fields': ('cor',)
        }),
        ('Metadados', {
            'fields': ('data_criacao',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Assinatura)
class AssinaturaAdmin(admin.ModelAdmin):
    list_display = [
        'nome', 
        'usuario', 
        'valor_formatado', 
        'ciclo_pagamento', 
        'categoria',
        'status', 
        'data_proxima_cobranca',
        'dias_restantes'
    ]
    list_filter = [
        'status', 
        'ciclo_pagamento', 
        'categoria', 
        'data_proxima_cobranca'
    ]
    search_fields = [
        'nome', 
        'descricao', 
        'usuario__username',
        'categoria__nome'
    ]
    readonly_fields = [
        'data_criacao', 
        'data_atualizacao',
        'valor_mensal_calculado',
        'valor_anual_calculado',
        'dias_restantes'
    ]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('usuario', 'nome', 'descricao', 'categoria')
        }),
        ('Valores e Pagamento', {
            'fields': (
                'valor', 
                'moeda', 
                'ciclo_pagamento',
                'valor_mensal_calculado',
                'valor_anual_calculado'
            )
        }),
        ('Datas', {
            'fields': (
                'data_primeira_cobranca',
                'data_proxima_cobranca',
                'dia_vencimento',
                'dias_restantes'
            )
        }),
        ('Status e Observações', {
            'fields': ('status', 'observacoes')
        }),
        ('Metadados', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['marcar_como_ativa', 'marcar_como_pausada', 'marcar_como_cancelada']
    
    def valor_formatado(self, obj):
        return f"R$ {obj.valor:,.2f}"
    valor_formatado.short_description = 'Valor'
    
    def dias_restantes(self, obj):
        dias = obj.dias_ate_proxima_cobranca()
        if dias == 0:
            return 'Hoje'
        elif dias < 0:
            return f'Vencida há {abs(dias)} dias'
        return f'{dias} dias'
    dias_restantes.short_description = 'Dias até cobrança'
    
    def valor_mensal_calculado(self, obj):
        return f"R$ {obj.valor_mensal():,.2f}"
    valor_mensal_calculado.short_description = 'Valor Mensal'
    
    def valor_anual_calculado(self, obj):
        return f"R$ {obj.valor_anual():,.2f}"
    valor_anual_calculado.short_description = 'Valor Anual'
    
    def marcar_como_ativa(self, request, queryset):
        queryset.update(status='ATIVA')
        self.message_user(request, f'{queryset.count()} assinatura(s) marcada(s) como ativa(s).')
    marcar_como_ativa.short_description = 'Marcar como Ativa'
    
    def marcar_como_pausada(self, request, queryset):
        queryset.update(status='PAUSADA')
        self.message_user(request, f'{queryset.count()} assinatura(s) pausada(s).')
    marcar_como_pausada.short_description = 'Marcar como Pausada'
    
    def marcar_como_cancelada(self, request, queryset):
        queryset.update(status='CANCELADA')
        self.message_user(request, f'{queryset.count()} assinatura(s) cancelada(s).')
    marcar_como_cancelada.short_description = 'Marcar como Cancelada'
