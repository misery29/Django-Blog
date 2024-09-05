from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('reservar/<int:campo_id>/', views.reservar, name='reservar'),
    path('confirmar/', views.confirmar_reserva, name='confirmar_reserva'),
    path('historico/', views.historico_reservas, name='historico_reservas'),
    path('cancelar/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),

]