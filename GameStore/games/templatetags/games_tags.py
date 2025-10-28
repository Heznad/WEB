from django import template
from ..models import Game, Genre, Tag  # Добавляем импорт Tag

register = template.Library()

@register.simple_tag()
def get_games():
    return Game.objects.all()

@register.simple_tag()
def get_genres():
    return Genre.objects.all().order_by('name')

@register.simple_tag()
def get_all_tags():
    return Tag.objects.all().order_by('name')