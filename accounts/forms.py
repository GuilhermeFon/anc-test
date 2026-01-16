from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario


class UsuarioCreationForm(forms.ModelForm):
    """Formulário de criação de usuário."""
    
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Usuario
        fields = ['username', 'is_staff']
        labels = {
            'username': 'Usuário',
            'is_staff': 'É Cartório?',
        }
        help_texts = {
            'is_staff': 'Marque se o usuário for do Cartório. Desmarcado = Produtor.',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UsuarioLoginForm(AuthenticationForm):
    """Formulário de login customizado."""
    
    username = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuário'})
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'})
    )
