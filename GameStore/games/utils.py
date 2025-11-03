from django.db import models

menu = [
    {'title': "Главная", 'url_name': 'home'},
    {'title': "Каталог", 'url_name': 'catalog'},
    {'title': "Отзывы", 'url_name': 'reviews'},
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Войти", 'url_name': 'login'}
]

class DataMixin:
    paginate_by = 2
    title_page = None
    cat_selected = None
    extra_context = {}
    
    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page
            
        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = menu
            
        if self.cat_selected is not None:
            self.extra_context['cat_selected'] = self.cat_selected
    
    def get_mixin_context(self, context, **kwargs):
        context['menu'] = menu
        context['cat_selected'] = self.cat_selected if self.cat_selected is not None else 0
        context.update(kwargs)
        return context