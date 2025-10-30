from django.urls import path
from games import views

urlpatterns = [
    path('', views.index, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/game/<slug:game_slug>/', views.catalog_game_slug, name='game_detail'),
    path('catalog/genre/<slug:genre_slug>/', views.catalog_by_genre, name='catalog_by_genre'),
    path('catalog/tag/<slug:tag_slug>/', views.catalog_by_tag, name='catalog_by_tag'),
    path('about/', views.about, name='about'),
    path('reviews/', views.reviews, name='reviews'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('add-game/', views.add_game, name='add_game'),
    path('upload-file/', views.upload_file, name='upload_file'),
]