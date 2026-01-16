from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import Usuario


class Raca(models.Model):
    
    nome = models.CharField(max_length=100, unique=True, verbose_name='Nome')
    
    class Meta:
        verbose_name = 'Raça'
        verbose_name_plural = 'Raças'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Propriedade(models.Model):
    
    nome = models.CharField(max_length=200, verbose_name='Nome')
    municipio = models.CharField(max_length=100, verbose_name='Município')
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='propriedades',
        verbose_name='Produtor'
    )
    
    class Meta:
        verbose_name = 'Propriedade'
        verbose_name_plural = 'Propriedades'
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} - {self.municipio}"


class Galinha(models.Model):
    
    SEXO_CHOICES = [
        ('M', 'Macho'),
        ('F', 'Fêmea'),
    ]
    
    numero_registro = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de Registro'
    )
    nome = models.CharField(max_length=100, verbose_name='Nome')
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, verbose_name='Sexo')
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')
    raca = models.ForeignKey(
        Raca,
        on_delete=models.PROTECT,
        related_name='galinhas',
        verbose_name='Raça'
    )
    propriedade_atual = models.ForeignKey(
        Propriedade,
        on_delete=models.PROTECT,
        related_name='galinhas',
        verbose_name='Propriedade Atual'
    )
    pai = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='filhos_como_pai',
        verbose_name='Pai',
        limit_choices_to={'sexo': 'M'}
    )
    mae = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='filhos_como_mae',
        verbose_name='Mãe',
        limit_choices_to={'sexo': 'F'}
    )
    
    class Meta:
        verbose_name = 'Galinha'
        verbose_name_plural = 'Galinhas'
        ordering = ['numero_registro']
    
    def __str__(self):
        return f"{self.numero_registro} - {self.nome}"
    
    def get_idade_anos(self):
        from datetime import date
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )
