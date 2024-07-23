from django.urls import path
from .views import index

app_name = 'campos'

urlpatterns = [
    path('', index, name='index'),
]