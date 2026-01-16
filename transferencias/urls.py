from django.urls import path
from . import views

app_name = 'transferencias'

urlpatterns = [
    path('cartorio/', views.TransferenciaListCartorioView.as_view(), name='transferencia_list_cartorio'),
    path('cartorio/<int:pk>/', views.TransferenciaDetailCartorioView.as_view(), name='transferencia_detail_cartorio'),
    path('cartorio/<int:pk>/aprovar/', views.aprovar_transferencia, name='aprovar_transferencia'),
    path('cartorio/<int:pk>/rejeitar/', views.rejeitar_transferencia, name='rejeitar_transferencia'),
    
    path('', views.TransferenciaListProdutorView.as_view(), name='transferencia_list_produtor'),
    path('<int:pk>/', views.TransferenciaDetailProdutorView.as_view(), name='transferencia_detail_produtor'),
    path('criar/', views.TransferenciaCreateView.as_view(), name='transferencia_create'),
]
