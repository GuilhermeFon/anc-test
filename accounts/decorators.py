from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin


def cartorio_required(function=None, redirect_field_name='next', login_url='accounts:login'):
    """
    Decorator para views que requerem usuário do cartório.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_cartorio(),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def produtor_required(function=None, redirect_field_name='next', login_url='accounts:login'):
    """
    Decorator para views que requerem usuário produtor.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_produtor(),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


class CartorioRequiredMixin(UserPassesTestMixin):
    """Mixin para CBVs que requerem usuário do cartório."""
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_cartorio()
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("Apenas usuários do cartório podem acessar esta página.")
        return super().handle_no_permission()


class ProdutorRequiredMixin(UserPassesTestMixin):
    """Mixin para CBVs que requerem usuário produtor."""
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_produtor()
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("Apenas produtores podem acessar esta página.")
        return super().handle_no_permission()
