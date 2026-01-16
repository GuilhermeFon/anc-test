from django.db import models
from django.core.exceptions import ValidationError
from core.models import Galinha, Propriedade


class TransferenciaPropriedade(models.Model):
    
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('APROVADO', 'Aprovado'),
        ('REJEITADO', 'Rejeitado'),
    ]
    
    galinha = models.ForeignKey(
        Galinha,
        on_delete=models.CASCADE,
        related_name='transferencias',
        verbose_name='Galinha'
    )
    origem = models.ForeignKey(
        Propriedade,
        on_delete=models.PROTECT,
        related_name='transferencias_origem',
        verbose_name='Propriedade de Origem'
    )
    destino = models.ForeignKey(
        Propriedade,
        on_delete=models.PROTECT,
        related_name='transferencias_destino',
        verbose_name='Propriedade de Destino'
    )
    data_solicitacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data da Solicitação'
    )
    data_processamento = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data do Processamento'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDENTE',
        verbose_name='Status'
    )
    observacao = models.TextField(
        blank=True,
        verbose_name='Observação'
    )
    
    class Meta:
        verbose_name = 'Transferência de Propriedade'
        verbose_name_plural = 'Transferências de Propriedade'
        ordering = ['-data_solicitacao']
    
    def __str__(self):
        return f"Transferência {self.id} - {self.galinha.numero_registro} - {self.get_status_display()}"
    
    def clean(self):
        super().clean()
        
        if self.origem == self.destino:
            raise ValidationError('A propriedade de origem e destino não podem ser iguais.')
        
        if self.galinha.propriedade_atual != self.origem:
            raise ValidationError(
                f'A galinha {self.galinha.numero_registro} não pertence à propriedade de origem informada.'
            )
        
        if self.origem.usuario != self.destino.usuario:
            raise ValidationError(
                'A propriedade de origem e destino devem pertencer ao mesmo produtor.'
            )
    
    def aprovar(self):
        from django.utils import timezone
        
        if self.status != 'PENDENTE':
            raise ValidationError('Apenas transferências pendentes podem ser aprovadas.')
        
        self.status = 'APROVADO'
        self.data_processamento = timezone.now()
        self.save()
        
        self.galinha.propriedade_atual = self.destino
        self.galinha.save()
    
    def rejeitar(self, observacao=''):
        from django.utils import timezone
        
        if self.status != 'PENDENTE':
            raise ValidationError('Apenas transferências pendentes podem ser rejeitadas.')
        
        self.status = 'REJEITADO'
        self.data_processamento = timezone.now()
        if observacao:
            self.observacao = observacao
        self.save()
