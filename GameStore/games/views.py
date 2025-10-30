from django.http import HttpResponseNotFound, Http404
from django.shortcuts import redirect, render, get_object_or_404
from .models import Game, Review, Status, Genre, Tag, UploadFiles, Cart, CartItem 
from django.contrib.auth.models import User
from .forms import AddGameModelForm, UploadFileForm
from django.db import connection
from django.conf import settings
menu = ['Главная', 'Каталог', 'Отзывы', 'О сайте', 'Войти']

def fill_database():
    # Если есть какие-то данные - удаляем их
    if Game.objects.exists() or Genre.objects.exists() or Tag.objects.exists():
        """print("🗑️ Очищаем старые данные...")
        CartItem.objects.all().delete()
        Cart.objects.all().delete()
        Review.objects.all().delete()
        Game.objects.all().delete()
        UploadFiles.objects.all().delete()  # Добавляем очистку загруженных файлов
        Tag.objects.all().delete()
        Genre.objects.all().delete()
        User.objects.filter(username='test_user').delete()
        
        # Сброс автоинкремента
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('games_game', 'games_genre', 'games_tag', 'games_review', 'games_cart', 'games_cartitem', 'games_uploadfiles', 'games_game_tags', 'games_game_genres')")
        
        print("✅ Старые данные удалены и автоинкремент сброшен")"""
        return

    print("🔄 Заполняем базу данных...")

    # Создаем жанры
    genres_data = [
        {'name': 'Экшен'},
        {'name': 'Приключения'},
        {'name': 'RPG'},
        {'name': 'Шутер'},
        {'name': 'Фэнтези'},
        {'name': 'Открытый мир'},
        {'name': 'Хоррор'},
        {'name': 'Спорт'},
        {'name': 'Симулятор'},
        {'name': 'Выживание'},
        {'name': 'Песочница'},
    ]
    
    genres_dict = {}
    for genre_data in genres_data:
        genre = Genre.objects.create(name=genre_data['name'])
        genres_dict[genre.name] = genre
        print(f"✅ Создан жанр: {genre.name} (slug: {genre.slug})")

    # Создаем теги
    tags_data = [
        {'name': 'Хит продаж'},
        {'name': 'Новинка'},
        {'name': 'Со скидкой'},
        {'name': 'Распродажа'},
        {'name': 'Мультиплеер'},
        {'name': 'Кооператив'},
        {'name': 'Одиночная'},
        {'name': 'С прокачкой'},
        {'name': 'С крафтом'},
        {'name': 'Атмосферная'},
    ]
    
    tags_dict = {}
    for tag_data in tags_data:
        tag = Tag.objects.create(name=tag_data['name'])
        tags_dict[tag.name] = tag
        print(f"✅ Создан тег: {tag.name} (slug: {tag.slug})")

    # Создаем тестового пользователя для отзывов и корзины
    test_user, created = User.objects.get_or_create(
        username='test_user',
        defaults={
            'email': 'test@example.com', 
            'first_name': 'Тестовый', 
            'last_name': 'Пользователь'
        }
    )
    if created:
        test_user.set_password('test123')
        test_user.save()
        print(f"✅ Создан тестовый пользователь: {test_user.username}")

    # Создаем корзину для пользователя
    cart, created = Cart.objects.get_or_create(user=test_user)
    if created:
        print(f"✅ Создана корзина для пользователя {test_user.username}")

    # Данные игр (теперь без поля image - оно будет заполняться через админку)
    games_data = [
        {
            'title': 'Uncharted', 
            'price': 999.00, 
            'platform': 'PS3', 
            'year_release': 2007, 
            'is_stock': False, 
            'age_rating': '16+',
            'description': 'Приключенческий экшен от третьего лица, где вы играете за охотника за сокровищами Нейтана Дрейка.',
            'is_published': Status.PUBLISHED,
            'genre_names': ['Экшен', 'Приключения', 'Шутер'],
            'tag_names': ['Одиночная', 'Приключения']
        },
        {
            'title': 'The Witcher 3: Wild Hunt', 
            'price': 1999.00, 
            'platform': 'XBOX', 
            'year_release': 2015, 
            'is_stock': True, 
            'age_rating': '18+',
            'description': 'Эпическая RPG в мире фэнтези, где вы Геральт из Ривии - ведьмак, охотящийся на монстров.',
            'is_published': Status.PUBLISHED,
            'genre_names': ['RPG', 'Фэнтези', 'Приключения'],
            'tag_names': ['Хит продаж', 'Открытый мир', 'С прокачкой', 'Одиночная']
        },
        {
            'title': 'Grand Theft Auto V', 
            'price': 1499.00, 
            'platform': 'PC', 
            'year_release': 2013, 
            'is_stock': True, 
            'age_rating': '18+',
            'description': 'Открытый мир криминального экшена с тремя протагонистами в городе Лос-Сантос.',
            'is_published': Status.PUBLISHED,
            'genre_names': ['Экшен', 'Приключения', 'Открытый мир'],
            'tag_names': ['Хит продаж', 'Открытый мир', 'Мультиплеер']
        },
        {
            'title': 'Elden Ring', 
            'price': 2609.00, 
            'platform': 'PS5', 
            'year_release': 2022, 
            'is_stock': True, 
            'age_rating': '16+',
            'description': 'Фэнтезийная action-RPG с открытым миром от создателей Dark Souls.',
            'is_published': Status.PUBLISHED,
            'genre_names': ['RPG', 'Фэнтези', 'Экшен'],
            'tag_names': ['Новинка', 'С прокачкой', 'Атмосферная', 'Одиночная']
        },
        {
            'title': 'The Last of Us', 
            'price': 1299.00, 
            'platform': 'PS4', 
            'year_release': 2013, 
            'is_stock': True, 
            'age_rating': '18+',
            'description': 'Постапокалиптическая история о выживании и отношениях между Джоэлом и Элли.',
            'is_published': Status.PUBLISHED,
            'genre_names': ['Экшен', 'Приключения', 'Хоррор'],
            'tag_names': ['Атмосферная', 'Одиночная']
        },
        {
            'title': 'Cyberpunk 2077', 
            'price': 1899.00, 
            'platform': 'PC', 
            'year_release': 2020, 
            'is_stock': True, 
            'age_rating': '18+',
            'description': 'RPG в киберпанк-мире будущего с открытым миром и нелинейным сюжетом.',
            'is_published': Status.PUBLISHED,
            'genre_names': ['RPG', 'Фантастика', 'Экшен'],
            'tag_names': ['Атмосферная', 'С прокачкой', 'Одиночная']
        },
        {
            'title': 'Red Dead Redemption 2', 
            'price': 2199.00, 
            'platform': 'PS4', 
            'year_release': 2018, 
            'is_stock': True, 
            'age_rating': '18+',
            'description': 'Приключения в диком западе с глубоким сюжетом и открытым миром.',
            'is_published': Status.PUBLISHED,
            'genre_names': ['Приключения', 'Экшен', 'Открытый мир'],
            'tag_names': ['Хит продаж', 'Открытый мир', 'Атмосферная', 'Одиночная']
        },
        {
            'title': 'Minecraft', 
            'price': 799.00, 
            'platform': 'PC', 
            'year_release': 2011, 
            'is_stock': True, 
            'age_rating': '7+',
            'description': 'Песочница с бесконечными возможностями для творчества и выживания.',
            'is_published': Status.PUBLISHED,
            'genre_names': ['Песочница', 'Приключения', 'Выживание'],
            'tag_names': ['С крафтом', 'Мультиплеер', 'Кооператив']
        },
        {
            'title': 'FIFA 23', 
            'price': 2999.00, 
            'platform': 'PS5', 
            'year_release': 2022, 
            'is_stock': True, 
            'age_rating': '3+',
            'description': 'Футбольный симулятор с реалистичной графикой и геймплеем.',
            'is_published': Status.PUBLISHED,
            'genre_names': ['Спорт', 'Симулятор'],
            'tag_names': ['Мультиплеер', 'Спорт']
        },
        {
            'title': 'Resident Evil 4', 
            'price': 2499.00, 
            'platform': 'PS5', 
            'year_release': 2023, 
            'is_stock': True, 
            'age_rating': '18+',
            'description': 'Хоррор-экшен с элементами выживания и захватывающим сюжетом.',
            'is_published': Status.PUBLISHED,
            'genre_names': ['Хоррор', 'Экшен', 'Выживание'],
            'tag_names': ['Атмосферная', 'Одиночная']
        },
    ]

    # Создаем игры
    games_dict = {}
    for game_data in games_data:
        # Извлекаем названия жанров и тегов
        genre_names = game_data.pop('genre_names', [])
        tag_names = game_data.pop('tag_names', [])
        
        # Создаем игру (image будет None - заполним через админку)
        game = Game.objects.create(**game_data)
        
        # Устанавливаем связи с жанрами
        for genre_name in genre_names:
            genre = genres_dict.get(genre_name)
            if genre:
                game.genres.add(genre)
        
        # Устанавливаем связи с тегами
        for tag_name in tag_names:
            tag = tags_dict.get(tag_name)
            if tag:
                game.tags.add(tag)
        
        games_dict[game.title] = game
        print(f"✅ Создана игра: {game.title} (slug: {game.slug}) с жанрами: {', '.join(genre_names)} и тегами: {', '.join(tag_names)}")

    # Создаем отзывы
    reviews_data = [
        {
            'rating': 5,
            'text': 'Отличный магазин! Быстрая доставка, игры всегда лицензионные. The Witcher 3 работала без нареканий.',
            'game_title': 'The Witcher 3: Wild Hunt'
        },
        {
            'rating': 4,
            'text': 'Хороший сервис, но хотелось бы больше акций. GTA V пришла мгновенно после оплаты.',
            'game_title': 'Grand Theft Auto V'
        },
        {
            'rating': 5,
            'text': 'Elden Ring - просто шедевр! Спасибо за оперативную доставку ключа. Буду покупать ещё.',
            'game_title': 'Elden Ring'
        },
        {
            'rating': 5,
            'text': 'The Last of Us тронула до слёз. Качество обслуживания на высоте, всем рекомендую этот магазин!',
            'game_title': 'The Last of Us'
        },
        {
            'rating': 3,
            'text': 'Uncharted понравилась, но были небольшие проблемы с активацией. Техподдержка помогла быстро.',
            'game_title': 'Uncharted'
        }
    ]

    for review_data in reviews_data:
        game_title = review_data.pop('game_title')
        
        game = games_dict.get(game_title)
        if game:
            review = Review.objects.create(user=test_user, game=game, **review_data)
            print(f"✅ Создан отзыв от {review.user.username} на {game.title}")
        else:
            print(f"❌ Игра '{game_title}' не найдена для отзыва")

    # Создаем несколько тестовых загруженных файлов
    try:
        # Создаем запись о загруженном файле (без самого файла)
        uploaded_file = UploadFiles.objects.create(
            file='test_document.pdf',
            description='Тестовый документ для демонстрации',
            file_size=1024
        )
        print(f"✅ Создан тестовый загруженный файл: {uploaded_file.file.name}")
    except Exception as e:
        print(f"⚠️ Не удалось создать тестовый файл: {e}")

    print("🎮 База данных успешно заполнена!")

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
            'text': 'Регулярные акции, распродажи и системы скидок для постоянных клиентов'
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
    # Заполняем БД при первом обращении
    fill_database()
    
    games_from_db = Game.published.in_stock()
    
    data = {
        'title':'Главная страница',
        'menu':menu,
        'games': games_from_db,
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
    reviews_from_db = Review.objects.filter(is_published=True)
    
    data = {
        'title': 'Отзывы',
        'reviews': reviews_from_db,
        'menu': menu,
    }
    return render(request, 'games/reviews.html', context=data)

def catalog(request):
    games_from_db = Game.published.all()
    
    data = {
        'title': 'Каталог',
        'menu': menu,
        'games': games_from_db,
    }
    return render(request, 'games/catalog.html', context=data)

def catalog_by_genre(request, genre_slug):
    genre = get_object_or_404(Genre, slug=genre_slug)
    filtered_games = Game.published.filter(genres=genre)
    
    data = {
        'title': f'Каталог - {genre.name}',
        'games': filtered_games,
        'menu': menu,
        'current_genre': genre_slug,
    }
    return render(request, 'games/catalog.html', context=data)

def catalog_game_slug(request, game_slug):
    game = get_object_or_404(Game.published, slug=game_slug)
    
    data = {
        'title': game.title,
        'game': game,
        'menu': menu,
    }
    return render(request, 'games/game_detail.html', context=data)

def catalog_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    filtered_games = Game.published.filter(tags=tag)
    
    data = {
        'title': f'Каталог - Тег: {tag.name}',
        'games': filtered_games,
        'menu': menu,
        'current_tag': tag_slug,
    }
    return render(request, 'games/catalog.html', context=data)

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

def add_game(request):
    if request.method == 'POST':
        # ДОБАВЛЯЕМ request.FILES для обработки изображений
        form = AddGameModelForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Сохраняем игру с изображением
                game = form.save()
                return redirect('catalog')
            except Exception as e:
                form.add_error(None, f'Ошибка при сохранении игры: {str(e)}')
                print(f" Ошибка сохранения: {str(e)}")
        else:
            print("Форма содержит ошибки:")
            for field, errors in form.errors.items():
                print(f"   {field}: {', '.join(errors)}")
    else:
        form = AddGameModelForm()
    
    data = {
        'title': 'Добавить игру',
        'form': form,
        'menu': menu,
    }
    return render(request, 'games/add_game.html', context=data)

def upload_file(request):
    upload_result = None
    error_message = None
    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Проверяем размер файла
                uploaded_file = request.FILES['file']
                if uploaded_file.size > 10 * 1024 * 1024:
                    form.add_error('file', 'Файл слишком большой (максимум 10MB)')
                else:
                    uploaded_file_obj = form.save()
                    
                    upload_result = {
                        'original_name': uploaded_file_obj.file.name,
                        'saved_name': uploaded_file_obj.file.name,
                        'file_url': uploaded_file_obj.file.url,
                        'file_size': uploaded_file_obj.file_size,
                        'description': uploaded_file_obj.description,
                        'db_id': uploaded_file_obj.id
                    }
                    
            except Exception as e:
                error_message = f'Ошибка при загрузке файла: {str(e)}'
                print(f"Ошибка загрузки файла: {str(e)}")
        else:
            print("Форма загрузки файла содержит ошибки:")
            for field, errors in form.errors.items():
                print(f"   {field}: {', '.join(errors)}")
    else:
        form = UploadFileForm()
    
    # Получаем список загруженных файлов ИЗ БД
    uploaded_files = UploadFiles.objects.all().order_by('-uploaded_at')
    
    data = {
        'title': 'Загрузка файлов',
        'form': form,
        'menu': menu,
        'upload_result': upload_result,
        'error_message': error_message,
        'uploaded_files': uploaded_files,
    }
    return render(request, 'games/upload_file.html', context=data)