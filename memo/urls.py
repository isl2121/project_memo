from django.urls import path, include
from . import views

app_name = 'memo'
urlpatterns = [
    path('', views.MemoLV.as_view() ,name='index'),
    path('join/', views.signup, name='join'),
    path('login/', views.login, name='login'),
    path('make/', views.make, name='make'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('modify/<int:pk>/', views.modify, name='modify'),
    path('like/<int:pk>/', views.like, name='like')
]
