from django.urls import path
from avaliacoes import views

app_name = 'avaliacoes'

urlpatterns = [
    path('adicionar/<int:campo_id>/', views.adicionar_avaliacao, name='adicionar_avaliacao'),
]
