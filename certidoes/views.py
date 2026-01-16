from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import cartorio_required
from core.models import Galinha


@login_required
@cartorio_required
def emitir_certidao(request, pk):
    galinha = get_object_or_404(Galinha, pk=pk)
    
    transferencias = galinha.transferencias.filter(
        status='APROVADO'
    ).order_by('-data_processamento')
    
    context = {
        'galinha': galinha,
        'transferencias': transferencias,
    }
    
    return render(request, 'certidoes/certidao.html', context)
