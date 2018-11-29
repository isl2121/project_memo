from django.urls import path, include
from . import views

app_name = 'memo'
urlpatterns = [
    path('', views.MemoLV.as_view() ,name='index')
]