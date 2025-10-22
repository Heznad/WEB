from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseServerError
from django.shortcuts import redirect, render

# Create your views here.
menu = ["О сайте", "Каталог", "Отзывы","Войти"]

data_db = [
    {'id': 1, 'title':'Uncharted', 'price': 999.00, 'platform':'PS4', 'year_release':'2007', 'is_stock': False},
    {'id': 2, 'title': 'The Witcher 3: Wild Hunt', 'price': 1999.00, 'platform': 'XBOX', 'year_release': '2015', 'is_stock': True},
    {'id': 3, 'title': 'Grand Theft Auto V', 'price': 1499.00, 'platform': 'PC', 'year_release': '2013', 'is_stock': True},
    {'id': 4, 'title': 'Elden Ring', 'price': 2499.00, 'platform': 'PS5', 'year_release': '2022', 'is_stock': False},
    {'id': 5, 'title': 'The Last of Us', 'price': 1299.00, 'platform': 'PS4', 'year_release': '2013', 'is_stock': True},
]

def index(request):
    data = {
        'title':'Главная страница',
        'games': data_db,
        'menu':menu,
    }
    return render(request, 'games/index.html', context=data)

def categories(request, cat_id):
    return HttpResponse(f"<h1>Игры по категориям<h1><p>id:{cat_id}</p>")

def categories_by_slug(request, cat_slug):
    if request.GET:
        print(request.GET)
    if request.POST:
        print(request.POST)
    return HttpResponse(f"<h1>Игры по категориям<h1><p>slug:{cat_slug}</p>")

def archive(request, year):
    if year > 2025:
        return redirect("home")

    return HttpResponse(f"<h1>Игры по годам</h1><p>{year}</p>")

def about(request):
    data = {
        'title':'О сайте',
        'menu':menu,
    }
    return render(request, 'games/about.html', context=data)

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

