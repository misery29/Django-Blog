from django.urls import path
from campos.views import list_fields, detail_fields, map_view

app_name = 'campos'

urlpatterns = [
    path('', list_fields, name='list_fields'),
    path('campo/<int:pk>/',detail_fields, name='detail_fields'),
    path('mapa/', map_view, name='map_view'),

]