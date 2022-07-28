# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('lobby/', views.lobby, name='lobby'),
    path('ingame', views.ingame, name='ingame'),
    path('ingame/<int:game_id>/', views.ingame, name='ingame'),
]
