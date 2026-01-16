# Cartório Rural de Registro de Galinhas

Sistema Django para gerenciamento cartorial de registro de galinhas, propriedades e transferências.

## Dependências

- Python 3.8+
- Django 5.0.1
- python-decouple 3.8
- Bootstrap 5.3.0 (via CDN)

## Instalação

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar SECRET_KEY
python generate_secret_key.py
# Copie a chave gerada e cole no arquivo .env

# Criar banco de dados
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser
```

## Como Executar

```bash
python manage.py runserver
```

Acesse: http://127.0.0.1:8000

## Decisões Técnicas

**Arquitetura modular**: 4 apps Django (`accounts`, `core`, `transferencias`, `certidoes`) para separação de responsabilidades.

**Autenticação customizada**: Model `Usuario` extende `AbstractUser` com perfis CARTORIO e PRODUTOR. Controle de acesso via mixins e decorators.

**Class-Based Views**: CBVs com mixins reutilizáveis para autorização e filtragem de dados por perfil.

**Validações em cascata**: Model → Form → View, garantindo integridade de dados e regras de negócio.

**Transferências com workflow**: Estados PENDENTE/APROVADO/REJEITADO com validações de propriedade antes da aprovação.
