from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404

# Create your views here.
menu = ['Главная', 'Каталог', 'Отзывы', 'О сайте', 'Войти']
games_db = [
    {
        'id': 1, 
        'title': 'Uncharted', 
        'price': 999.00, 
        'platform': 'PS3', 
        'year_release': '2007', 
        'is_stock': False, 
        'image': 'uncharted_cover.jpg',
        'age_rating': '16+',
        'description': 'Приключенческий экшен от третьего лица, где вы играете за охотника за сокровищами Нейтана Дрейка.',
        'genres': ['Экшен', 'Приключения', 'Шутер']
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
        'description': 'Эпическая RPG в мире фэнтези, где вы Геральт из Ривии - ведьмак, охотящийся на монстров.',
        'genres': ['RPG', 'Фэнтези', 'Приключения']
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
        'description': 'Открытый мир криминального экшена с тремя протагонистами в городе Лос-Сантос.',
        'genres': ['Экшен', 'Приключения', 'Открытый мир']
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
        'description': 'Фэнтезийная action-RPG с открытым миром от создателей Dark Souls.',
        'genres': ['RPG', 'Фэнтези', 'Экшен']
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
        'description': 'Постапокалиптическая история о выживании и отношениях между Джоэлом и Элли.',
        'genres': ['Экшен', 'Приключения', 'Хоррор']
    },
    {
        'id': 6, 
        'title': 'Cyberpunk 2077', 
        'price': 1899.00, 
        'platform': 'PC', 
        'year_release': '2020', 
        'is_stock': True, 
        'image': 'cyberpunk_cover.jpg',
        'age_rating': '18+',
        'description': 'RPG в киберпанк-мире будущего с открытым миром и нелинейным сюжетом.',
        'genres': ['RPG', 'Фантастика', 'Экшен']
    },
    {
        'id': 7, 
        'title': 'Red Dead Redemption 2', 
        'price': 2199.00, 
        'platform': 'PS4', 
        'year_release': '2018', 
        'is_stock': True, 
        'image': 'red_dead_cover.jpg',
        'age_rating': '18+',
        'description': 'Приключения в диком западе с глубоким сюжетом и открытым миром.',
        'genres': ['Приключения', 'Экшен', 'Открытый мир']
    },
    {
        'id': 8, 
        'title': 'Minecraft', 
        'price': 799.00, 
        'platform': 'PC', 
        'year_release': '2011', 
        'is_stock': True, 
        'image': 'minecraft_cover.jpg',
        'age_rating': '7+',
        'description': 'Песочница с бесконечными возможностями для творчества и выживания.',
        'genres': ['Песочница', 'Приключения', 'Выживание']
    },
    {
        'id': 9, 
        'title': 'FIFA 23', 
        'price': 2999.00, 
        'platform': 'PS5', 
        'year_release': '2022', 
        'is_stock': True, 
        'image': 'fifa_cover.jpg',
        'age_rating': '3+',
        'description': 'Футбольный симулятор с реалистичной графикой и геймплеем.',
        'genres': ['Спорт', 'Симулятор']
    },
    {
        'id': 10, 
        'title': 'Resident Evil 4', 
        'price': 2499.00, 
        'platform': 'PS5', 
        'year_release': '2023', 
        'is_stock': True, 
        'image': 'resident_evil_cover.jpg',
        'age_rating': '18+',
        'description': 'Хоррор-экшен с элементами выживания и захватывающим сюжетом.',
        'genres': ['Хоррор', 'Экшен', 'Выживание']
    },
]
reviews_db = [
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
about_db = {
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
        'menu':menu,
    }
    return render(request, 'games/index.html', context=data)

def about(request):
    data = {
        'title': about_db['title'],
        'about': about_db,
        'menu': menu,
    }
    return render(request, 'games/about.html', context=data)

def reviews(request):
    data = {
        'title': 'Отзывы',
        'reviews': reviews_db,
        'menu': menu,
    }
    return render(request, 'games/reviews.html', context=data)

def catalog(request):
    data = {
        'title': 'Каталог',
        'menu': menu,
    }
    return render(request, 'games/catalog.html', context=data)

def catalog_by_genre(request, genre):
    # Фильтруем игры по жанру
    filtered_games = [game for game in games_db if genre in game['genres']]
    
    data = {
        'title': f'Каталог - {genre}',
        'games': filtered_games,
        'menu': menu,
        'current_genre': genre,
    }
    return render(request, 'games/catalog_genre.html', context=data)

def catalog_game_id(request, game_id):
    # Ищем игру по ID
    game = None
    for g in games_db:
        if g['id'] == game_id:
            game = g
            break
    
    # Если игра не найдена - 404
    if not game:
        raise Http404("Игра не найдена")
    
    data = {
        'title': game['title'],
        'game': game,  # Передаем одну игру
        'menu': menu,
    }
    return render(request, 'games/game_detail.html', context=data)

def login(request):
    data = {
        'title': 'Вход',
        'menu': menu,
    }
    return render(request, 'games/login.html', context=data)

def register(request):
    data = {
        'title': 'Регистрация',
        'menu': menu,
    }
    return render(request, 'games/register.html', context=data)

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

