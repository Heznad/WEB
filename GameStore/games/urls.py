from django.urls import path
from games import views

urlpatterns = [
    path('', views.GamesHome.as_view(), name='home'),
    path('catalog/', views.GamesCatalog.as_view(), name='catalog'),
    path('catalog/game/<slug:game_slug>/', views.GameDetail.as_view(), name='game_detail'),
    path('catalog/genre/<slug:genre_slug>/', views.GamesByGenre.as_view(), name='catalog_by_genre'),
    path('catalog/tag/<slug:tag_slug>/', views.GamesByTag.as_view(), name='catalog_by_tag'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('reviews/', views.ReviewsView.as_view(), name='reviews'),
    path('add-game/', views.AddGameView.as_view(), name='add_game'),
    path('edit-game/<slug:game_slug>/', views.UpdateGameView.as_view(), name='edit_game'),
    path('delete-game/<slug:game_slug>/', views.DeleteGameView.as_view(), name='delete_game'),
    path('upload-file/', views.UploadFileView.as_view(), name='upload_file'),
]