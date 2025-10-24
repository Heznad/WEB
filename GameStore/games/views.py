from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseServerError
from django.shortcuts import redirect, render

# Create your views here.
menu = ["О сайте", "Каталог", "Отзывы","Войти"]
data_db = [
    {
        'id': 1, 
        'title': 'Uncharted', 
        'price': 999.00, 
        'platform': 'PS3', 
        'year_release': '2007', 
        'is_stock': False, 
        'image': 'uncharted_cover.jpg',
        'age_rating': '16+',
        'description': 'Приключенческий экшен от третьего лица, где вы играете за охотника за сокровищами Нейтана Дрейка.'
    },
    {
        'id': 2, 
        'title': 'The Witcher 3: Wild Hunt', 
        'price': 1999.00, 
        'platform': 'XBOX', 
        'year_release': '2015', 
        'is_stock': True, 
        'image': 'the_witcher_3_cover.jpg',
        'age_rating': '18+',
        'description': 'Эпическая RPG в мире фэнтези, где вы Геральт из Ривии - ведьмак, охотящийся на монстров.'
    },
    {
        'id': 3, 
        'title': 'Grand Theft Auto V', 
        'price': 1499.00, 
        'platform': 'PC', 
        'year_release': '2013', 
        'is_stock': True, 
        'image': 'gta_5_cover.jpg',
        'age_rating': '18+',
        'description': 'Открытый мир криминального экшена с тремя протагонистами в городе Лос-Сантос.'
    },
    {
        'id': 4, 
        'title': 'Elden Ring', 
        'price': 2609.00, 
        'platform': 'PS5', 
        'year_release': '2022', 
        'is_stock': True, 
        'image': 'elden_ring_cover.jpg',
        'age_rating': '16+',
        'description': 'Фэнтезийная action-RPG с открытым миром от создателей Dark Souls.'
    },
    {
        'id': 5, 
        'title': 'The Last of Us', 
        'price': 1299.00, 
        'platform': 'PS4', 
        'year_release': '2013', 
        'is_stock': True, 
        'image': 'the_last_of_us_cover.jpg',
        'age_rating': '18+',
        'description': 'Постапокалиптическая история о выживании и отношениях между Джоэлом и Элли.'
    },
]
data_db_reviews = [
    {
        'id': 1,
        'author': 'Алексей Петров',
        'rating': 5,
        'date': '15.12.2023',
        'text': 'Отличный магазин! Быстрая доставка, игры всегда лицензионные. The Witcher 3 работала без нареканий.',
        'game': 'The Witcher 3: Wild Hunt'
    },
    {
        'id': 2,
        'author': 'Мария Иванова',
        'rating': 4,
        'date': '02.01.2024',
        'text': 'Хороший сервис, но хотелось бы больше акций. GTA V пришла мгновенно после оплаты.',
        'game': 'Grand Theft Auto V'
    },
    {
        'id': 3,
        'author': 'Дмитрий Сидоров',
        'rating': 5,
        'date': '20.11.2023',
        'text': 'Elden Ring - просто шедевр! Спасибо за оперативную доставку ключа. Буду покупать ещё.',
        'game': 'Elden Ring'
    },
    {
        'id': 4,
        'author': 'Ольга Козлова',
        'rating': 5,
        'date': '08.01.2024',
        'text': 'The Last of Us тронула до слёз. Качество обслуживания на высоте, всем рекомендую этот магазин!',
        'game': 'The Last of Us'
    },
    {
        'id': 5,
        'author': 'Сергей Волков',
        'rating': 3,
        'date': '29.12.2023',
        'text': 'Uncharted понравилась, но были небольшие проблемы с активацией. Техподдержка помогла быстро.',
        'game': 'Uncharted'
    }
]
data_db_about = {
    'title': 'О нашем магазине',
    'description': 'GameStore — это ведущий онлайн-магазин компьютерных игр, где каждый геймер найдет именно то, что ищет. Мы создали этот проект с одной простой целью: сделать покупку игр максимально удобной, быстрой и приятной для всех любителей видеоигр.',
    'features': [
        {
            'icon': '🎮',
            'title': 'Огромный ассортимент',
            'text': 'Более 10 000 игр для всех платформ: PC, PlayStation, Xbox и Nintendo'
        },
        {
            'icon': '💎',
            'title': 'Качество и надежность',
            'text': 'Только лицензионные продукты от официальных поставщиков и издателей'
        },
        {
            'icon': '💰',
            'title': 'Выгодные цены',
            'text': 'Регулярные акции, распродажи и система скидок для постоянных клиентов'
        },
        {
            'icon': '🚚',
            'title': 'Мгновенная доставка',
            'text': 'Ключи активации приходят сразу после оплаты, без ожидания'
        }
    ],
    'stats': [
        {'number': '10K+', 'label': 'игр в каталоге'},
        {'number': '50K+', 'label': 'довольных клиентов'},
        {'number': '5+', 'label': 'лет на рынке'},
        {'number': '24/7', 'label': 'поддержка'}
    ],
    'contact_info': {
        'phone': '8-800-XXX-XX-XX',
        'email': 'support@gamestore.ru',
        'work_time': 'круглосуточно',
        'support': '24/7'
    }
}

def index(request):
    data = {
        'title':'Главная страница',
        'games': data_db,
        'menu':menu,
    }
    return render(request, 'games/index.html', context=data)

def about(request):
    data = {
        'title': data_db_about['title'],
        'about': data_db_about,
        'menu': menu,
    }
    return render(request, 'games/about.html', context=data)

def reviews(request):
    data = {
        'title': 'Отзывы',
        'reviews': data_db_reviews,
        'menu': menu,
    }
    return render(request, 'games/reviews.html', context=data)

def catalog(request):
    data = {
        'title':'Главная страница',
        'games': data_db,
        'menu':menu,
    }
    return render(request, 'games/catalog.html', context=data)

def login(request):
    data = {
        'title': 'Вход',
        'menu': menu,
    }
    return render(request, 'games/login.html', context=data)

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

"""def categories_by_slug(request, cat_slug):
    if request.GET:
        print(request.GET)
    if request.POST:
        print(request.POST)
    return HttpResponse(f"<h1>Игры по категориям<h1><p>slug:{cat_slug}</p>")"""

#def archive(request, year):
    #if year > 2025:
    #    return redirect("home")
    #return HttpResponse(f"<h1>Игры по годам</h1><p>{year}</p>")

#def categories(request, cat_id):
#    return HttpResponse(f"<h1>Игры по категориям<h1><p>id:{cat_id}</p>")