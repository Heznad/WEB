from django.urls import path, register_converter
from games import views, converters

#register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('catalog/', views.catalog, name='cats'),
    path('reviews/', views.reviews, name='reviews'),
    path('login/', views.login, name='login')
    #path('cats/<slug:cat_slug>/', views.categories_by_slug, name='cats_slug'),
]





