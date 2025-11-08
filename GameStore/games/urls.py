from django.urls import path
from . import views

urlpatterns = [
    # Основные маршруты
    path('', views.GamesHome.as_view(), name='home'),
    path('catalog/', views.GamesCatalog.as_view(), name='catalog'),
    path('catalog/game/<slug:game_slug>/', views.GameDetail.as_view(), name='game_detail'),
    path('catalog/genre/<slug:genre_slug>/', views.GamesByGenre.as_view(), name='catalog_by_genre'),
    path('catalog/tag/<slug:tag_slug>/', views.GamesByTag.as_view(), name='catalog_by_tag'),
    path('reviews/', views.ReviewsView.as_view(), name='reviews'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('add-game/', views.AddGameView.as_view(), name='add_game'),
    
    path('game/update/<slug:game_slug>/', views.UpdateGameView.as_view(), name='update_game'),
    path('game/delete/<slug:game_slug>/', views.DeleteGameView.as_view(), name='delete_game'),
    path('review/update/<int:review_id>/', views.UpdateReviewView.as_view(), name='update_review'),
    path('review/delete/<int:review_id>/', views.DeleteReviewView.as_view(), name='delete_review'),
    
    path('cart/', views.CartView.as_view(), name='cart'),
    path('add-review/', views.AddReviewView.as_view(), name='add_review'),
    path('add-review-ajax/', views.add_review_ajax, name='add_review_ajax'),
    path('game/<slug:game_slug>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('game/<slug:game_slug>/add-comment/', views.add_comment, name='add_comment'),
    path('game/<slug:game_slug>/toggle-like/', views.toggle_like, name='toggle_like'),
    path('upload-file/', views.UploadFileView.as_view(), name='upload_file'),
]