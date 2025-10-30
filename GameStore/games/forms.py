from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from .models import Game

class AddGameModelForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'price', 'platform', 'year_release', 'description', 
                 'age_rating', 'is_stock', 'is_published']
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
        }
        labels = {
            'title': 'Название игры',
            'price': 'Цена (руб)',
            'platform': 'Платформа',
            'year_release': 'Год выпуска',
            'description': 'Описание игры',
            'age_rating': 'Возрастной рейтинг',
            'is_stock': 'В наличии',
            'is_published': 'Опубликовать сразу',
        }
        error_messages = {
            'title': {
                'required': 'Название игры обязательно для заполнения',
                'max_length': 'Название слишком длинное',
            },
            'price': {
                'required': 'Укажите цену игры',
            }
        }

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