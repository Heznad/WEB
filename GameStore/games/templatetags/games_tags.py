from django import template
import games.views as views

register = template.Library()

@register.simple_tag()
def get_games():
    return views.games_db

@register.simple_tag()
def get_genres():
    all_genres = set()
    for game in views.games_db:
        for genre in game['genres']:
            all_genres.add(genre)
    return sorted(list(all_genres))