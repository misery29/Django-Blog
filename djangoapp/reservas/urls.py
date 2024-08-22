from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('reservar/<int:campo_id>/', views.reservar, name='reservar'),
    path('confirmar/', views.confirmar_reserva, name='confirmar_reserva'),
]