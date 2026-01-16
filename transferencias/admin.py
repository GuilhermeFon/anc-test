from django.contrib import admin
from .models import TransferenciaPropriedade


@admin.register(TransferenciaPropriedade)
class TransferenciaPropriedadeAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'galinha', 'origem', 'destino', 
        'status', 'data_solicitacao', 'data_processamento'
    ]
    list_filter = ['status', 'data_solicitacao']
    search_fields = ['galinha__numero_registro', 'galinha__nome']
    raw_id_fields = ['galinha', 'origem', 'destino']
    readonly_fields = ['data_solicitacao', 'data_processamento']
    date_hierarchy = 'data_solicitacao'
