from django.urls import path
from app import views

urlpatterns = [    
    path('', views.index, name='index'),      
    path('display_playlist/', views.display_playlist, name='display_playlist'),
]