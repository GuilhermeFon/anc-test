from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.db import transaction
from accounts.decorators import CartorioRequiredMixin, ProdutorRequiredMixin
from .models import TransferenciaPropriedade
from .forms import TransferenciaPropriedadeForm


class TransferenciaListCartorioView(LoginRequiredMixin, CartorioRequiredMixin, ListView):
    model = TransferenciaPropriedade
    template_name = 'transferencias/transferencia_list_cartorio.html'
    context_object_name = 'transferencias'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_filter'] = self.request.GET.get('status', '')
        context['pendentes_count'] = TransferenciaPropriedade.objects.filter(
            status='PENDENTE'
        ).count()
        return context


class TransferenciaDetailCartorioView(LoginRequiredMixin, CartorioRequiredMixin, DetailView):
    model = TransferenciaPropriedade
    template_name = 'transferencias/transferencia_detail_cartorio.html'
    context_object_name = 'transferencia'


def aprovar_transferencia(request, pk):
    if not request.user.is_authenticated or not request.user.is_cartorio():
        return HttpResponseForbidden("Acesso negado.")
    
    transferencia = get_object_or_404(TransferenciaPropriedade, pk=pk)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                transferencia.aprovar()
            messages.success(request, 'Transferência aprovada com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao aprovar transferência: {str(e)}')
        
        return redirect('transferencias:transferencia_detail_cartorio', pk=pk)
    
    return render(request, 'transferencias/confirmar_aprovacao.html', {
        'transferencia': transferencia
    })


def rejeitar_transferencia(request, pk):
    if not request.user.is_authenticated or not request.user.is_cartorio():
        return HttpResponseForbidden("Acesso negado.")
    
    transferencia = get_object_or_404(TransferenciaPropriedade, pk=pk)
    
    if request.method == 'POST':
        observacao = request.POST.get('observacao', '')
        try:
            with transaction.atomic():
                transferencia.rejeitar(observacao)
            messages.success(request, 'Transferência rejeitada.')
        except Exception as e:
            messages.error(request, f'Erro ao rejeitar transferência: {str(e)}')
        
        return redirect('transferencias:transferencia_detail_cartorio', pk=pk)
    
    return render(request, 'transferencias/confirmar_rejeicao.html', {
        'transferencia': transferencia
    })



class TransferenciaListProdutorView(LoginRequiredMixin, ProdutorRequiredMixin, ListView):
    model = TransferenciaPropriedade
    template_name = 'transferencias/transferencia_list_produtor.html'
    context_object_name = 'transferencias'
    paginate_by = 20
    
    def get_queryset(self):
        return super().get_queryset().filter(
            origem__usuario=self.request.user
        ) | super().get_queryset().filter(
            destino__usuario=self.request.user
        )


class TransferenciaDetailProdutorView(LoginRequiredMixin, ProdutorRequiredMixin, DetailView):
    model = TransferenciaPropriedade
    template_name = 'transferencias/transferencia_detail_produtor.html'
    context_object_name = 'transferencia'
    
    def get_queryset(self):
        return super().get_queryset().filter(
            origem__usuario=self.request.user
        ) | super().get_queryset().filter(
            destino__usuario=self.request.user
        )


class TransferenciaCreateView(LoginRequiredMixin, ProdutorRequiredMixin, CreateView):
    model = TransferenciaPropriedade
    form_class = TransferenciaPropriedadeForm
    template_name = 'transferencias/transferencia_form.html'
    success_url = reverse_lazy('transferencias:transferencia_list_produtor')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        if form.instance.origem.usuario != self.request.user:
            messages.error(self.request, 'Propriedade de origem inválida.')
            return self.form_invalid(form)
        
        if form.instance.destino.usuario != self.request.user:
            messages.error(self.request, 'Propriedade de destino inválida.')
            return self.form_invalid(form)
        
        messages.success(self.request, 'Solicitação de transferência criada com sucesso!')
        return super().form_valid(form)
