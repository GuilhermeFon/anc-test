from django import forms
from .models import Raca, Propriedade, Galinha
from accounts.models import Usuario


class RacaForm(forms.ModelForm):
    
    class Meta:
        model = Raca
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PropriedadeForm(forms.ModelForm):
    
    class Meta:
        model = Propriedade
        fields = ['nome', 'municipio', 'usuario']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'municipio': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].queryset = Usuario.objects.filter(is_staff=False)


class GalinhaForm(forms.ModelForm):
    
    class Meta:
        model = Galinha
        fields = [
            'numero_registro', 'nome', 'sexo', 'data_nascimento',
            'raca', 'propriedade_atual', 'pai', 'mae'
        ]
        widgets = {
            'numero_registro': forms.TextInput(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'raca': forms.Select(attrs={'class': 'form-control'}),
            'propriedade_atual': forms.Select(attrs={'class': 'form-control'}),
            'pai': forms.Select(attrs={'class': 'form-control'}),
            'mae': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['pai'].queryset = Galinha.objects.filter(sexo='M')
        self.fields['mae'].queryset = Galinha.objects.filter(sexo='F')
        
        if self.instance.pk:
            self.fields['pai'].queryset = self.fields['pai'].queryset.exclude(pk=self.instance.pk)
            self.fields['mae'].queryset = self.fields['mae'].queryset.exclude(pk=self.instance.pk)
