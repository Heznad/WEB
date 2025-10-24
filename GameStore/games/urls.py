from django.urls import path
from games import views

urlpatterns = [
    path('', views.index, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<int:game_id>', views.catalog_game_id, name='catalog_game_id'),
    path('catalog/genre/<str:genre>/', views.catalog_by_genre, name='catalog_by_genre'),
    path('about/', views.about, name='about'),
    path('reviews/', views.reviews, name='reviews'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]





