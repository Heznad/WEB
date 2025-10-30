from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from .models import Game

class AddGameForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        min_length=2,
        label="Название игры",
        widget=forms.TextInput(attrs={
            'class': 'form-input', 
            'placeholder': 'Введите название игры на любом языке'
        }),
        error_messages={
            'min_length': 'Слишком короткое название (минимум 2 символа)',
            'required': 'Название игры обязательно для заполнения',
            'max_length': 'Название слишком длинное (максимум 255 символов)'
        }
    )
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Цена (руб)",
        min_value=0,
        max_value=100000,
        widget=forms.NumberInput(attrs={
            'class': 'form-input', 
            'placeholder': '0.00',
            'step': '0.01'
        }),
        error_messages={
            'required': 'Укажите цену игры',
            'min_value': 'Цена не может быть отрицательной',
            'max_value': 'Слишком большая цена (максимум 100 000 руб)'
        }
    )
    platform = forms.ChoiceField(
        choices=Game.PLATFORM_CHOICES,
        label="Платформа",
        widget=forms.Select(attrs={'class': 'form-select'}),
        error_messages={
            'required': 'Выберите платформу'
        }
    )
    year_release = forms.IntegerField(
        label="Год выпуска",
        min_value=1990,
        max_value=2024,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'placeholder': '2024'
        }),
        error_messages={
            'required': 'Укажите год выпуска',
            'min_value': 'Год должен быть не ранее 1990',
            'max_value': 'Год должен быть не позднее 2024'
        }
    )
    description = forms.CharField(
        label="Описание игры",
        widget=forms.Textarea(attrs={
            'class': 'form-textarea', 
            'rows': 4,
            'placeholder': 'Опишите игру, её особенности, геймплей...'
        }),
        required=False,
        validators=[
            MinLengthValidator(10, message="Описание должно содержать минимум 10 символов"),
            MaxLengthValidator(1000, message="Описание слишком длинное (максимум 1000 символов)")
        ]
    )
    
    age_rating = forms.ChoiceField(
        choices=[
            ('3+', '3+'),
            ('6+', '6+'),
            ('12+', '12+'),
            ('16+', '16+'),
            ('18+', '18+'),
        ],
        label="Возрастной рейтинг",
        initial="18+",
        widget=forms.Select(attrs={'class': 'form-select'}),
        error_messages={
            'required': 'Укажите возрастной рейтинг'
        }
    )
    
    is_stock = forms.BooleanField(
        label="В наличии",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )
    
    is_published = forms.BooleanField(
        label="Опубликовать сразу",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )

    def clean_title(self):
        """Кастомная валидация для поля title"""
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 2:
            raise ValidationError('Название должно содержать минимум 2 символа')   
        # Проверяем на недопустимые символы (например, только спецсимволы)
        if all(not char.isalnum() for char in title):
            raise ValidationError('Название должно содержать буквы или цифры')     
        return title
    
    def clean_year_release(self):
        """Кастомная валидация для года выпуска"""
        year = self.cleaned_data.get('year_release')
        if year < 1990:
            raise ValidationError('Слишком старый год выпуска (минимум 1990)') 
        if year > 2024:
            raise ValidationError('Год выпуска не может быть в будущем')
        return year
    
    def clean_price(self):
        """Кастомная валидация для цены"""
        price = self.cleaned_data.get('price')
        if price == 0:
            raise ValidationError('Цена не может быть нулевой')          
        return price
    