from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.db.models import Q
from accounts.decorators import CartorioRequiredMixin, ProdutorRequiredMixin
from .models import Raca, Propriedade, Galinha
from .forms import RacaForm, PropriedadeForm, GalinhaForm


@login_required
def home(request):
    """View inicial do sistema."""
    print(f"[DEBUG HOME] User: {request.user.username}")
    print(f"[DEBUG HOME] Perfil: {request.user.perfil}")
    print(f"[DEBUG HOME] is_cartorio(): {request.user.is_cartorio()}")
    print(f"[DEBUG HOME] is_produtor(): {request.user.is_produtor()}")
    
    if request.user.is_cartorio():
        print("[DEBUG HOME] Redirecionando para galinha_list (cartório)")
        return redirect('core:galinha_list')
    else:
        print("[DEBUG HOME] Redirecionando para galinha_list_produtor (produtor)")
        return redirect('core:galinha_list_produtor')

class RacaListView(LoginRequiredMixin, CartorioRequiredMixin, ListView):
    model = Raca
    template_name = 'core/raca_list.html'
    context_object_name = 'racas'
    paginate_by = 20

class RacaCreateView(LoginRequiredMixin, CartorioRequiredMixin, CreateView):
    model = Raca
    form_class = RacaForm
    template_name = 'core/raca_form.html'
    success_url = reverse_lazy('core:raca_list')

class RacaUpdateView(LoginRequiredMixin, CartorioRequiredMixin, UpdateView):
    model = Raca
    form_class = RacaForm
    template_name = 'core/raca_form.html'
    success_url = reverse_lazy('core:raca_list')

class RacaDeleteView(LoginRequiredMixin, CartorioRequiredMixin, DeleteView):
    model = Raca
    template_name = 'core/raca_confirm_delete.html'
    success_url = reverse_lazy('core:raca_list')

class PropriedadeListView(LoginRequiredMixin, CartorioRequiredMixin, ListView):
    model = Propriedade
    template_name = 'core/propriedade_list.html'
    context_object_name = 'propriedades'
    paginate_by = 20

class PropriedadeCreateView(LoginRequiredMixin, CartorioRequiredMixin, CreateView):
    model = Propriedade
    form_class = PropriedadeForm
    template_name = 'core/propriedade_form.html'
    success_url = reverse_lazy('core:propriedade_list')

class PropriedadeUpdateView(LoginRequiredMixin, CartorioRequiredMixin, UpdateView):
    model = Propriedade
    form_class = PropriedadeForm
    template_name = 'core/propriedade_form.html'
    success_url = reverse_lazy('core:propriedade_list')

class PropriedadeDeleteView(LoginRequiredMixin, CartorioRequiredMixin, DeleteView):
    model = Propriedade
    template_name = 'core/propriedade_confirm_delete.html'
    success_url = reverse_lazy('core:propriedade_list')

class GalinhaListView(LoginRequiredMixin, CartorioRequiredMixin, ListView):
    model = Galinha
    template_name = 'core/galinha_list.html'
    context_object_name = 'galinhas'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(numero_registro__icontains=search) |
                Q(nome__icontains=search)
            )
        return queryset


class GalinhaDetailView(LoginRequiredMixin, DetailView):
    model = Galinha
    template_name = 'core/galinha_detail.html'
    context_object_name = 'galinha'
    
    def get_queryset(self):
        """Filtra galinhas conforme o perfil do usuário."""
        queryset = super().get_queryset()
        if self.request.user.is_produtor():
            queryset = queryset.filter(propriedade_atual__usuario=self.request.user)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transferencias'] = self.object.transferencias.filter(
            status='APROVADO'
        ).order_by('-data_processamento')
        return context

class GalinhaCreateView(LoginRequiredMixin, CartorioRequiredMixin, CreateView):
    model = Galinha
    form_class = GalinhaForm
    template_name = 'core/galinha_form.html'
    success_url = reverse_lazy('core:galinha_list')

class GalinhaUpdateView(LoginRequiredMixin, CartorioRequiredMixin, UpdateView):
    model = Galinha
    form_class = GalinhaForm
    template_name = 'core/galinha_form.html'
    success_url = reverse_lazy('core:galinha_list')

class GalinhaDeleteView(LoginRequiredMixin, CartorioRequiredMixin, DeleteView):
    model = Galinha
    template_name = 'core/galinha_confirm_delete.html'
    success_url = reverse_lazy('core:galinha_list')

class GalinhaListProdutorView(LoginRequiredMixin, ProdutorRequiredMixin, ListView):
    model = Galinha
    template_name = 'core/galinha_list_produtor.html'
    context_object_name = 'galinhas'
    paginate_by = 20
    
    def get_queryset(self):
        """Produtor vê apenas galinhas de suas propriedades."""
        queryset = super().get_queryset().filter(
            propriedade_atual__usuario=self.request.user
        )
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(numero_registro__icontains=search) |
                Q(nome__icontains=search)
            )
        return queryset


class PropriedadeListProdutorView(LoginRequiredMixin, ProdutorRequiredMixin, ListView):
    model = Propriedade
    template_name = 'core/propriedade_list_produtor.html'
    context_object_name = 'propriedades'
    paginate_by = 20
    
    def get_queryset(self):
        """Produtor vê apenas suas propriedades."""
        return super().get_queryset().filter(usuario=self.request.user)
