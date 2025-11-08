# Стандартные модули Django
from django.http import HttpResponseNotFound, Http404, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.db import connection
from django.conf import settings
from django.urls import reverse_lazy

# Система аутентификации и контроля доступа
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Классовые представления
from django.views.generic import (
    ListView, DetailView, TemplateView, FormView, 
    CreateView, UpdateView, DeleteView
)

# Модели приложения
from .models import (
    Game, Review, Status, Genre, Tag, UploadFiles, 
    Cart, CartItem, GameComment, GameLike
)

# Формы приложения
from .forms import (
    AddGameModelForm, UploadFileForm, ReviewForm, GameCommentForm
)

# Импортируем наш миксин
from .utils import DataMixin

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

class GamesHome(DataMixin, ListView):
    template_name = 'games/index.html'
    context_object_name = 'games'
    title_page = 'Главная страница'
    
    def get_queryset(self):
        return Game.published.in_stock()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context) 

class GamesCatalog(DataMixin, ListView):
    template_name = 'games/catalog.html'
    context_object_name = 'games'
    title_page = 'Каталог'
    
    def get_queryset(self):
        return Game.published.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context) 

class GameDetail(DataMixin, DetailView):
    model = Game
    template_name = 'games/game_detail.html'
    context_object_name = 'game'
    slug_url_kwarg = 'game_slug'
    
    def get_queryset(self):
        return Game.published.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['game'].title)

class GamesByTag(DataMixin, ListView):
    template_name = 'games/catalog.html'
    context_object_name = 'games'
    allow_empty = True
    
    def get_queryset(self):
        return Game.published.filter(tags__slug=self.kwargs['tag_slug'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        
        # Используем миксин для добавления жанров и тегов
        mixin_context = self.get_mixin_context(context, title=f'Каталог - Тег: {tag.name}')
        mixin_context['current_tag'] = tag
        mixin_context['is_empty'] = not self.get_queryset().exists()
        return mixin_context

class GamesByGenre(DataMixin, ListView):
    template_name = 'games/catalog.html'
    context_object_name = 'games'
    allow_empty = True
    
    def get_queryset(self):
        return Game.published.filter(genres__slug=self.kwargs['genre_slug'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre = get_object_or_404(Genre, slug=self.kwargs['genre_slug'])
        
        # Используем миксин для добавления жанров и тегов
        mixin_context = self.get_mixin_context(context, title=f'Каталог - {genre.name}')
        mixin_context['current_genre'] = genre
        mixin_context['is_empty'] = not self.get_queryset().exists()
        return mixin_context

class AboutView(DataMixin, TemplateView):
    template_name = 'games/about.html'
    title_page = 'О нашем магазине'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about'] = about_db
        return self.get_mixin_context(context)

class ReviewsView(DataMixin, ListView):
    template_name = 'games/reviews.html'
    context_object_name = 'reviews'
    title_page = 'Отзывы'
    
    def get_queryset(self):
        return Review.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)

class AddGameView(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddGameModelForm
    template_name = 'games/add_game.html'
    success_url = reverse_lazy('catalog')
    title_page = 'Добавить игру'
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)

class UpdateGameView(LoginRequiredMixin, DataMixin, UpdateView):
    model = Game
    form_class = AddGameModelForm
    template_name = 'games/add_game.html'
    success_url = reverse_lazy('catalog')
    slug_url_kwarg = 'game_slug'
    title_page = 'Редактирование игры'
    
    def get_queryset(self):
        return Game.published.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем флаг, что это редактирование
        context['is_edit'] = True
        return self.get_mixin_context(context, title=f'Редактирование: {self.object.title}')

class DeleteGameView(LoginRequiredMixin,DataMixin, DeleteView):
    model = Game
    template_name = 'games/delete_game.html'
    success_url = reverse_lazy('catalog')
    slug_url_kwarg = 'game_slug'
    context_object_name = 'game'
    title_page = 'Удаление игры'
    
    def get_queryset(self):
        return Game.published.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=f'Удаление: {self.object.title}')

class UploadFileView(DataMixin, FormView):
    form_class = UploadFileForm
    template_name = 'games/upload_file.html'
    success_url = reverse_lazy('upload_file')
    title_page = 'Загрузка файлов'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uploaded_files'] = UploadFiles.objects.all().order_by('-uploaded_at')
        return self.get_mixin_context(context)
    
    def form_valid(self, form):
        try:
            uploaded_file = self.request.FILES['file']
            if uploaded_file.size > 10 * 1024 * 1024:
                form.add_error('file', 'Файл слишком большой (максимум 10MB)')
                return self.form_invalid(form)
            
            uploaded_file_obj = form.save()
            
            # Добавляем результат в extra_context
            self.extra_context['upload_result'] = {
                'original_name': uploaded_file_obj.file.name,
                'saved_name': uploaded_file_obj.file.name,
                'file_url': uploaded_file_obj.file.url,
                'file_size': uploaded_file_obj.file_size,
                'description': uploaded_file_obj.description,
                'db_id': uploaded_file_obj.id
            }
            
        except Exception as e:
            form.add_error(None, f'Ошибка при загрузке файла: {str(e)}')
            return self.form_invalid(form)
        
        return super().form_valid(form)

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

class ReviewsView(DataMixin, ListView):
    """Страница отзывов с формой добавления"""
    template_name = 'games/reviews.html'
    context_object_name = 'reviews'
    title_page = 'Отзывы'
    
    def get_queryset(self):
        return Review.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        context['games'] = Game.published.in_stock()
        return self.get_mixin_context(context)

class AddReviewView(LoginRequiredMixin, DataMixin, CreateView):
    """Добавление отзыва"""
    form_class = ReviewForm
    template_name = 'games/add_review.html'
    success_url = reverse_lazy('reviews')
    title_page = 'Добавить отзыв'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)

class CartView(LoginRequiredMixin, DataMixin, DetailView):
    """Просмотр корзины"""
    template_name = 'games/cart.html'
    context_object_name = 'cart'
    title_page = 'Корзина'
    
    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

class GameDetail(DataMixin, DetailView):
    model = Game
    template_name = 'games/game_detail.html'
    context_object_name = 'game'
    slug_url_kwarg = 'game_slug'
    
    def get_queryset(self):
        return Game.published.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Добавляем комментарии
        context['comments'] = GameComment.objects.filter(
            game=self.object, 
            is_published=True
        )
        context['comment_form'] = GameCommentForm()
        
        # Добавляем информацию о лайках
        if self.request.user.is_authenticated:
            try:
                user_like = GameLike.objects.get(
                    user=self.request.user, 
                    game=self.object
                )
                context['user_reaction'] = user_like.value
            except GameLike.DoesNotExist:
                context['user_reaction'] = 0
        else:
            context['user_reaction'] = 0
        
        # Считаем общее количество лайков и дизлайков
        likes_count = GameLike.objects.filter(game=self.object, value=1).count()
        dislikes_count = GameLike.objects.filter(game=self.object, value=-1).count()
        context['likes_count'] = likes_count
        context['dislikes_count'] = dislikes_count
        
        # Проверяем, есть ли игра в корзине пользователя
        if self.request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=self.request.user)
                in_cart = CartItem.objects.filter(cart=cart, game=self.object).exists()
                context['in_cart'] = in_cart
            except Cart.DoesNotExist:
                context['in_cart'] = False
        else:
            context['in_cart'] = False
            
        return self.get_mixin_context(context, title=context['game'].title)

class UpdateReviewView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm 
    template_name = 'games/update_review.html'
    pk_url_kwarg = 'review_id'
    
    def get_success_url(self):
        return reverse_lazy('reviews')
    
    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user or self.request.user.has_perm('games.can_edit_all_reviews')

class DeleteReviewView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'games/delete_review.html'
    pk_url_kwarg = 'review_id'
    
    def get_success_url(self):
        return reverse_lazy('reviews')
    
    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user or self.request.user.has_perm('games.can_edit_all_reviews')

@login_required
@require_POST
def add_to_cart(request, game_slug):
    """Добавление игры в корзину (в одно нажатие)"""
    game = get_object_or_404(Game, slug=game_slug)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        game=game,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'Игра "{game.title}" добавлена в корзину',
            'cart_total_items': cart.total_items(),
            'cart_total_price': str(cart.total_price())
        })
    
    return redirect('game_detail', game_slug=game_slug)

@login_required
@require_POST
def add_comment(request, game_slug):
    """Добавление комментария к игре"""
    game = get_object_or_404(Game, slug=game_slug)
    form = GameCommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.game = game
        comment.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Комментарий добавлен',
                'comment_id': comment.id
            })
    
    return redirect('game_detail', game_slug=game_slug)

@login_required
@require_POST
def toggle_like(request, game_slug):
    """Постановка/снятие лайка/дизлайка"""
    game = get_object_or_404(Game, slug=game_slug)
    value = int(request.POST.get('value', 0))
    
    try:
        like = GameLike.objects.get(user=request.user, game=game)
        if like.value == value:
            # Если нажата та же кнопка - убираем реакцию
            like.delete()
            current_value = 0
        else:
            # Если нажата другая кнопка - меняем реакцию
            like.value = value
            like.save()
            current_value = value
    except GameLike.DoesNotExist:
        # Если реакции не было - создаем новую
        like = GameLike.objects.create(user=request.user, game=game, value=value)
        current_value = value
    
    # Пересчитываем счетчики
    likes_count = GameLike.objects.filter(game=game, value=1).count()
    dislikes_count = GameLike.objects.filter(game=game, value=-1).count()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'current_value': current_value,
            'likes_count': likes_count,
            'dislikes_count': dislikes_count
        })
    
    return redirect('game_detail', game_slug=game_slug)

@login_required
@require_POST
def add_review_ajax(request):
    """Добавление отзыва через AJAX"""
    form = ReviewForm(request.POST)
    
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Отзыв успешно добавлен',
                'review_id': review.id
            })
    
    return redirect('reviews')

@login_required
@require_POST
def remove_from_cart(request, item_id):
    """Удаление товара из корзины"""
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        cart_item.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Товар удален из корзины',
                'cart_total_items': cart_item.cart.total_items(),
                'cart_total_price': str(cart_item.cart.total_price())
            })
            
    except CartItem.DoesNotExist:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False, 
                'error': 'Товар не найден в корзине'
            })
    
    return redirect('cart')

