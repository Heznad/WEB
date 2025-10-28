from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Status(models.IntegerChoices):
    DRAFT = 0, 'Черновик'
    PUBLISHED = 1, 'Опубликовано'

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)
    
    def in_stock(self):
        return self.filter(is_stock=True)

class Genre(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Название жанра")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('catalog_by_genre', kwargs={'genre_slug': self.slug})

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']


class Tag(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Название тега")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('catalog_by_tag', kwargs={'tag_slug': self.slug})

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']

class Game(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название игры")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    PLATFORM_CHOICES = [
        ('PS3', 'PlayStation 3'),
        ('PS4', 'PlayStation 4'),
        ('PS5', 'PlayStation 5'),
        ('XBOX', 'XBOX'),
        ('PC', 'PC'),
    ]
    platform = models.CharField(max_length=10, choices=PLATFORM_CHOICES, verbose_name="Платформа")
    
    year_release = models.IntegerField(verbose_name="Год выпуска")
    is_stock = models.BooleanField(default=True, verbose_name="В наличии")
    image = models.CharField(max_length=255, blank=True, verbose_name="Изображение")
    age_rating = models.CharField(max_length=10, verbose_name="Возрастной рейтинг")
    description = models.TextField(verbose_name="Описание")
    
    genres = models.ManyToManyField(Genre, related_name='games', verbose_name="Жанры")

    tags = models.ManyToManyField(Tag, blank=True, related_name='games', verbose_name="Теги")
    
    is_published = models.BooleanField(
        choices=Status.choices,
        default=Status.PUBLISHED,
        verbose_name="Статус"
    )
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    
    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('game_detail', kwargs={'game_slug': self.slug})

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
        ordering = ['-time_create']

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"
    
    def total_price(self):
        return sum(item.total_price() for item in self.items.all())
    
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="Корзина")
    game = models.ForeignKey(Game, on_delete=models.PROTECT, verbose_name="Игра")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return f"{self.quantity} x {self.game.title}"
    
    def total_price(self):
        return self.game.price * self.quantity

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
        unique_together = ['cart', 'game']

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    
    RATING_CHOICES = [
        (1, '1 звезда'),
        (2, '2 звезды'),
        (3, '3 звезды'),
        (4, '4 звезды'),
        (5, '5 звезд'),
    ]
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Рейтинг")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата отзыва")
    text = models.TextField(verbose_name="Текст отзыва")
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name="Игра")
    
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    
    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.game.title}"
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-date']