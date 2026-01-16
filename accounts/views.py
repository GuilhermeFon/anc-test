from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from .forms import UsuarioLoginForm


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = UsuarioLoginForm
    
    def get_success_url(self):
        user = self.request.user
        
        if user.is_cartorio():
            return '/galinhas/'
        else:
            return '/minhas-galinhas/'
