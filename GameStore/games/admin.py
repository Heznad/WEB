from django.contrib import admin
from django.contrib import messages
from .models import Game,Review,Tag,Cart,CartItem,Genre

class PriceRangeFilter(admin.SimpleListFilter):
    title = 'Ценовой диапазон'
    parameter_name = 'price_range'
    
    def lookups(self, request, model_admin):
        return [
            ('0-1000', 'До 1000 руб'),
            ('1000-2000', '1000-2000 руб'),
            ('2000-3000', '2000-3000 руб'),
            ('3000+', 'Выше 3000 руб'),
        ]
    
    def queryset(self, request, queryset):
        if self.value() == '0-1000':
            return queryset.filter(price__lte=1000)
        elif self.value() == '1000-2000':
            return queryset.filter(price__gt=1000, price__lte=2000)
        elif self.value() == '2000-3000':
            return queryset.filter(price__gt=2000, price__lte=3000)
        elif self.value() == '3000+':
            return queryset.filter(price__gt=3000)
        return queryset

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'price', 'platform', 'year_release', 
        'is_stock', 'is_published', 'time_create',
        'price_in_usd', 'game_age', 'brief_info'
    )
    
    list_display_links = ('title',)
    list_editable = ('is_stock', 'is_published', 'price')
    ordering = ['-time_create']
    search_fields = ['title', 'description']
    list_filter = [
        'platform', 
        'is_stock', 
        'is_published', 
        'genres',
        PriceRangeFilter,
    ]
    list_per_page = 20
    
    actions = ['set_published', 'apply_discount_10']
    
    fields = [
        'title',
        'slug', 
        'price',
        'platform',
        'year_release',
        'is_stock',
        'is_published',
        'age_rating',
        'image',
        'description',
        'genres',
        'tags',
        'time_create', 
        'time_update',  
    ]

    prepopulated_fields = {"slug": ("title",)}
    
    filter_horizontal = ['genres', 'tags']
    
    readonly_fields = ['time_create', 'time_update']
    
    @admin.display(description="Цена в USD")
    def price_in_usd(self, obj):
        exchange_rate = 95
        usd_price = obj.price / exchange_rate
        return f"${usd_price:.2f}"
    
    @admin.display(description="Возраст игры")
    def game_age(self, obj):
        from datetime import datetime
        current_year = datetime.now().year
        age = current_year - obj.year_release
        
        if age == 0:
            return "Новый релиз"
        elif age == 1:
            return "1 год"
        elif 2 <= age <= 4:
            return f"{age} года"
        else:
            return f"{age} лет"
    
    @admin.display(description="Краткая информация")
    def brief_info(self, obj):
        tags_count = obj.tags.count()
        genres_count = obj.genres.count()
        return f"{genres_count} жанра, {tags_count} тегов"
    
    @admin.action(description="Опубликовать выбранные игры")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=True)
        self.message_user(request, f"{count} игр опубликовано", messages.SUCCESS)
    
    @admin.action(description="Применить скидку 10 процентов")
    def apply_discount_10(self, request, queryset):
        updated_count = 0
        for game in queryset:
            if game.price > 0:
                from decimal import Decimal
                game.price = game.price * Decimal('0.9')
                game.save()
                updated_count += 1
        
        self.message_user(request, f"Скидка применена к {updated_count} играм", messages.SUCCESS)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ['name']
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ['name']
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total_items', 'total_price')
    list_display_links = ('id', 'user')
    list_filter = ['created_at']
    readonly_fields = ('created_at', 'updated_at')

    def total_items(self, obj):
        return obj.total_items()
    total_items.short_description = 'Всего товаров'

    def total_price(self, obj):
        return f"{obj.total_price()} ₽"
    total_price.short_description = 'Общая стоимость'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'game', 'quantity', 'total_price', 'added_at')
    list_display_links = ('id', 'game')
    list_filter = ['added_at']
    readonly_fields = ('added_at',)

    def total_price(self, obj):
        return f"{obj.total_price()} ₽"
    total_price.short_description = 'Общая стоимость'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'game', 'rating', 'date', 'is_published')
    list_display_links = ('id', 'user')
    list_editable = ('is_published',)
    list_filter = ['rating', 'is_published', 'date']
    search_fields = ['user__username', 'game__title', 'text']
    ordering = ['-date']
    list_per_page = 20