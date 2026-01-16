from django.urls import path
from . import views

app_name = 'certidoes'

urlpatterns = [
    path('<int:pk>/', views.emitir_certidao, name='emitir_certidao'),
]
