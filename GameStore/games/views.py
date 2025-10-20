from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseServerError
from django.shortcuts import redirect

# Create your views here.
def index(request):
    return HttpResponse("Страница приложения games.")

def categories(request, cat_id):
    if cat_id == 500:
        raise HttpResponse(status=500)
    return HttpResponse(f"<h1>Игры по категориям<h1><p>id:{cat_id}</p>")

def categories_by_slug(request, cat_slug):
    if request.GET:
        print(request.GET)
    if request.POST:
        print(request.POST)
    return HttpResponse(f"<h1>Игры по категориям<h1><p>slug:{cat_slug}</p>")

def archive(request, year):
    if year > 2025:
        return redirect('home', permanent=True)

    return HttpResponse(f"<h1>Игры по годам</h1><p>{year}</p>")

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def server_error(request):
    return HttpResponseServerError('<h1>Ошибка сервера</h1>')

