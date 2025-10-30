from django import forms
from django.core.exceptions import ValidationError
from .models import Game, UploadFiles

class AddGameModelForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'price', 'platform', 'year_release', 'description', 
                 'age_rating', 'image', 'is_stock', 'is_published'] #Добавил поле image
        
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
            'image': forms.FileInput(attrs={ #Виджет для поля image
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
            'image': 'Изображение игры', #Заголовок для поля image
            'is_stock': 'В наличии',
            'is_published': 'Опубликовать сразу',
        }

    #Валидация поля image
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Размер изображения не должен превышать 5MB')
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