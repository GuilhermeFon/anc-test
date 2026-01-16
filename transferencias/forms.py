from django import forms
from .models import TransferenciaPropriedade
from core.models import Galinha, Propriedade


class TransferenciaPropriedadeForm(forms.ModelForm):
    
    class Meta:
        model = TransferenciaPropriedade
        fields = ['galinha', 'origem', 'destino', 'observacao']
        widgets = {
            'galinha': forms.Select(attrs={'class': 'form-control'}),
            'origem': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'destino': forms.Select(attrs={'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and user.is_produtor():
            self.fields['galinha'].queryset = Galinha.objects.filter(
                propriedade_atual__usuario=user
            )
            self.fields['origem'].queryset = Propriedade.objects.filter(usuario=user)
            self.fields['destino'].queryset = Propriedade.objects.filter(usuario=user)
    
    def clean(self):
        cleaned_data = super().clean()
        galinha = cleaned_data.get('galinha')
        origem = cleaned_data.get('origem')
        
        if galinha and origem and galinha.propriedade_atual != origem:
            raise forms.ValidationError(
                'A galinha selecionada não pertence à propriedade de origem.'
            )
        
        return cleaned_data
