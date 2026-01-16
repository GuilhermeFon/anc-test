import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import Raca

User = get_user_model()


def create_initial_data():
    
    racas_iniciais = [
        "Índio Gigante", "Rhode Island Red", "Plymouth Rock", "Leghorn",
        "Sussex", "Orpington", "Brahma", "Wyandotte", "Australorp", "New Hampshire"
    ]
    
    criadas = 0
    for nome in racas_iniciais:
        _, created = Raca.objects.get_or_create(nome=nome)
        if created:
            criadas += 1
    
    print(f"Raças: {criadas} criadas, {len(racas_iniciais) - criadas} já existiam")
    print(f"Usuários: {User.objects.filter(is_staff=True).count()} cartório, {User.objects.filter(is_staff=False).count()} produtores")


if __name__ == '__main__':
    create_initial_data()
