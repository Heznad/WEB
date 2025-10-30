import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import pre_delete


def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
         'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
         'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
         'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '',
         'э': 'e', 'ю': 'yu', 'я': 'ya',
         
         'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D',
         'Е': 'E', 'Ё': 'Yo', 'Ж': 'Zh', 'З': 'Z', 'И': 'I',
         'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
         'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T',
         'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': 'C', 'Ч': 'Ch',
         'Ш': 'Sh', 'Щ': 'Shch', 'Ь': '', 'Ы': 'Y', 'Ъ': '',
         'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'}
    
    return "".join(map(lambda x: d[x] if x in d else x, s))

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
    
    def save(self, *args, **kwargs):
        if not self.slug:
            transliterated_name = translit_to_eng(self.name)
            self.slug = slugify(transliterated_name)
        super().save(*args, **kwargs)

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
    
    def save(self, *args, **kwargs):
        if not self.slug:
            transliterated_name = translit_to_eng(self.name)
            self.slug = slugify(transliterated_name)
        super().save(*args, **kwargs)

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
    image = models.ImageField(
        upload_to="games/%Y/%m/%d/",
        blank=True,
        null=True,
        verbose_name="Изображение",
        default=None,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])
        ]
    )
    age_rating = models.CharField(max_length=10, verbose_name="Возрастной рейтинг")
    description = models.TextField(verbose_name="Описание")
    
    genres = models.ManyToManyField(Genre, related_name='games', verbose_name="Жанры")
    tags = models.ManyToManyField(Tag, blank=True, related_name='games', verbose_name="Теги")
    
    is_published = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
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
    
    def save(self, *args, **kwargs):
        if not self.slug:
            transliterated_title = translit_to_eng(self.title)
            self.slug = slugify(transliterated_title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
        ordering = ['-time_create']

def upload_files_unique_name(instance, filename):
    """Генерирует уникальное имя файла"""
    original_name = filename
    
    # Разделяем имя и расширение
    if '.' in original_name:
        name_part = original_name[:original_name.rindex('.')]
        ext_part = original_name[original_name.rindex('.'):]
    else:
        name_part = original_name
        ext_part = ''

    # Генерируем уникальный суффикс
    suffix = str(uuid.uuid4())[:8]

    # Создаем новое имя файла
    new_filename = f"{name_part}_{suffix}{ext_part}"
    
    # Возвращаем путь для сохранения
    return f"uploads_model/{new_filename}"

class UploadFiles(models.Model):
    file = models.FileField(
        upload_to=upload_files_unique_name,
        verbose_name="Файл",
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf', 'txt', 'zip', 'rar'])
        ]
    )
    description = models.CharField(
        max_length=200, 
        blank=True, 
        verbose_name="Описание файла"
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Время загрузки"
    )
    file_size = models.IntegerField(
        verbose_name="Размер файла (байт)",
        default=0
    )
    original_filename = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Оригинальное имя файла"
    )

    def __str__(self):
        return f"Файл: {self.original_filename}"

    def save(self, *args, **kwargs):
        if self.file and not self.original_filename:
            # Сохраняем оригинальное имя файла при первом сохранении
            self.original_filename = self.file.name
        
        if self.file:
            # Обновляем размер файла
            self.file_size = self.file.size
        
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Загруженный файл'
        verbose_name_plural = 'Загруженные файлы'
        ordering = ['-uploaded_at']

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



@receiver(post_save, sender=Game)
def create_upload_files_record(sender, instance, created, **kwargs):
    """Автоматически создает запись в UploadFiles при загрузке изображения игры"""
    if instance.image and instance.image.name:
        # Проверяем, нет ли уже такой записи
        if not UploadFiles.objects.filter(file=instance.image.name).exists():
            UploadFiles.objects.create(
                file=instance.image.name,  # Сохраняем путь к файлу
                description=f'Изображение для игры: {instance.title}',
                file_size=instance.image.size,
                original_filename=instance.image.name.split('/')[-1]  # Только имя файла
            )

@receiver(pre_delete, sender=UploadFiles)
def remove_file_from_games(sender, instance, **kwargs):
    """При удалении файла из UploadFiles также удаляет его из связанных игр"""
    if instance.file:
        # Находим все игры, которые используют этот файл
        games_with_file = Game.objects.filter(image=instance.file.name)
        
        for game in games_with_file:
            # Удаляем изображение у игры
            game.image.delete(save=False)  # Удаляем файл с диска
            game.image = None  # Очищаем поле
            game.save()