from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    def __str__(self):
        tipo = "Cartório" if self.is_staff else "Produtor"
        return f"{self.username} ({tipo})"
    
    def is_cartorio(self):
        return self.is_staff
    
    def is_produtor(self):
        return not self.is_staff
    
    def get_perfil_display(self):
        return "Cartório" if self.is_staff else "Produtor"
