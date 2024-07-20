from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from usuarios.views import index

app_name = 'usuarios'

urlpatterns = [
    path('', index, name='index'),
]

