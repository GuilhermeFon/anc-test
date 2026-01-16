from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    
    path('racas/', views.RacaListView.as_view(), name='raca_list'),
    path('racas/criar/', views.RacaCreateView.as_view(), name='raca_create'),
    path('racas/<int:pk>/editar/', views.RacaUpdateView.as_view(), name='raca_update'),
    path('racas/<int:pk>/excluir/', views.RacaDeleteView.as_view(), name='raca_delete'),
    
    path('propriedades/', views.PropriedadeListView.as_view(), name='propriedade_list'),
    path('propriedades/criar/', views.PropriedadeCreateView.as_view(), name='propriedade_create'),
    path('propriedades/<int:pk>/editar/', views.PropriedadeUpdateView.as_view(), name='propriedade_update'),
    path('propriedades/<int:pk>/excluir/', views.PropriedadeDeleteView.as_view(), name='propriedade_delete'),
    
    path('minhas-propriedades/', views.PropriedadeListProdutorView.as_view(), name='propriedade_list_produtor'),
    
    path('galinhas/', views.GalinhaListView.as_view(), name='galinha_list'),
    path('galinhas/criar/', views.GalinhaCreateView.as_view(), name='galinha_create'),
    path('galinhas/<int:pk>/', views.GalinhaDetailView.as_view(), name='galinha_detail'),
    path('galinhas/<int:pk>/editar/', views.GalinhaUpdateView.as_view(), name='galinha_update'),
    path('galinhas/<int:pk>/excluir/', views.GalinhaDeleteView.as_view(), name='galinha_delete'),
    
    path('minhas-galinhas/', views.GalinhaListProdutorView.as_view(), name='galinha_list_produtor'),
]
