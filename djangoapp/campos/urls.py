from django.urls import path
from campos.views import list_fields

app_name = 'campos'

urlpatterns = [
    path('', list_fields, name='list_fields'),
]