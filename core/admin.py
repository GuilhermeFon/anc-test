from django.contrib import admin
from .models import Raca, Propriedade, Galinha


@admin.register(Raca)
class RacaAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']


@admin.register(Propriedade)
class PropriedadeAdmin(admin.ModelAdmin):
    list_display = ['nome', 'municipio', 'usuario']
    list_filter = ['municipio']
    search_fields = ['nome', 'municipio', 'usuario__username']
    raw_id_fields = ['usuario']


@admin.register(Galinha)
class GalinhaAdmin(admin.ModelAdmin):
    list_display = ['numero_registro', 'nome', 'sexo', 'raca', 'propriedade_atual', 'data_nascimento']
    list_filter = ['sexo', 'raca', 'propriedade_atual']
    search_fields = ['numero_registro', 'nome']
    raw_id_fields = ['propriedade_atual', 'pai', 'mae']
    date_hierarchy = 'data_nascimento'
