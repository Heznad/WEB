from django.db import models
from django.urls import reverse

class Status(models.IntegerChoices):
    DRAFT = 0, 'Черновик'
    PUBLISHED = 1, 'Опубликовано'

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)
    
    def in_stock(self):
        return self.filter(is_stock=True)

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
    genres = models.CharField(max_length=255, verbose_name="Жанры")
    
    # Дополнительные поля для управления
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

class Review(models.Model):
    author = models.CharField(max_length=100, verbose_name="Автор")
    
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
        return f"Отзыв от {self.author} на {self.game.title}"
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-date']