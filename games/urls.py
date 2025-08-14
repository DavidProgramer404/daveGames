# rutas de juegos y categorias
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:category_id>/', views.category_games, name='category_games'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
]
