from django import template
from ..models import Game  # Импортируем модель Game

register = template.Library()

@register.simple_tag()
def get_games():
    # Возвращаем игры из БД вместо статических данных
    return Game.objects.all()

@register.simple_tag()
def get_genres():
    # Получаем уникальные жанры из БД
    all_genres = set()
    games = Game.objects.all()
    for game in games:
        # Разделяем строку жанров на отдельные жанры
        genres_list = [genre.strip() for genre in game.genres.split(',')]
        for genre in genres_list:
            all_genres.add(genre)
    return sorted(list(all_genres))