from django import forms
from django.core.exceptions import ValidationError
from .models import Game, UploadFiles, Review, GameComment

class AddGameModelForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'price', 'platform', 'year_release', 'description', 
                 'age_rating', 'image', 'is_stock', 'is_published']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input', 
                'placeholder': 'Введите название игры'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-input', 
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'platform': forms.Select(attrs={'class': 'form-select'}),
            'year_release': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': '2024'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea', 
                'rows': 4,
                'placeholder': 'Опишите игру...'
            }),
            'age_rating': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '18+'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-file',
                'accept': 'image/*'
            }),
        }
        
        labels = {
            'title': 'Название игры',
            'price': 'Цена (руб)',
            'platform': 'Платформа',
            'year_release': 'Год выпуска',
            'description': 'Описание игры',
            'age_rating': 'Возрастной рейтинг',
            'image': 'Изображение игры',
            'is_stock': 'В наличии',
            'is_published': 'Опубликовать сразу',
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        
        # Если изображение не загружено (None, False или пустое значение)
        if not image:
            return image
        
        # Если это существующее изображение (уже есть в базе), пропускаем проверку
        if hasattr(image, 'name') and not hasattr(image, 'file'):
            return image
        
        # Проверяем только новые загружаемые файлы
        if hasattr(image, 'size'):
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Размер изображения не должен превышать 5MB')
        
        if hasattr(image, 'content_type'):
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if image.content_type not in allowed_types:
                raise ValidationError('Допустимы только изображения: JPEG, PNG, GIF, WebP')
        
        return image

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 2:
            raise ValidationError('Название должно содержать минимум 2 символа')
        if title and not title[0].isupper():
            raise ValidationError('Название должно начинаться с заглавной буквы')
        if all(not char.isalnum() for char in title):
            raise ValidationError('Название должно содержать буквы или цифры')
        
        return title

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price == 0:
            raise ValidationError('Цена не может быть нулевой')
        if price < 100:
            raise ValidationError('Цена слишком низкая (минимум 100 руб)')
        if price > 50000:
            raise ValidationError('Цена слишком высокая (максимум 50 000 руб)')
        return price

    def clean_year_release(self):
        year = self.cleaned_data.get('year_release')
        if year < 1990:
            raise ValidationError('Слишком старый год выпуска (минимум 1990)')
        if year > 2024:
            raise ValidationError('Год выпуска не может быть в будущем')
        return year

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFiles
        fields = ['file', 'description']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'form-file',
                'accept': '.jpg,.jpeg,.png,.pdf,.txt,.zip,.rar'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Необязательное описание файла...'
            }),
        }
        labels = {
            'file': 'Выберите файл для загрузки',
            'description': 'Описание файла',
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['game', 'rating', 'title', 'text']
        widgets = {
            'game': forms.Select(attrs={
                'class': 'form-select',
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите заголовок отзыва (необязательно)'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4,
                'placeholder': 'Напишите ваш отзыв об игре...'
            }),
        }
        labels = {
            'game': 'Игра',
            'rating': 'Ваша оценка',
            'title': 'Заголовок отзыва',
            'text': 'Текст отзыва',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['game'].queryset = Game.published.in_stock()

class GameCommentForm(forms.ModelForm):
    class Meta:
        model = GameComment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Напишите ваш комментарий...'
            }),
        }
        labels = {
            'text': 'Комментарий',
        }