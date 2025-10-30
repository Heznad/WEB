from django.contrib import admin
from django.contrib import messages
from django.utils.safestring import mark_safe
from .models import Game, Review, Tag, Cart, CartItem, Genre, UploadFiles

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
        'image', #Добавил поле image
        'image_preview',
        'description',
        'genres',
        'tags',
        'time_create', 
        'time_update',  
    ]

    prepopulated_fields = {"slug": ("title",)}
    
    filter_horizontal = ['genres', 'tags']
    
    readonly_fields = ['time_create', 'time_update', 'image_preview']
    
    #Добавил пользовательское поле для отображения изображения из админ панели в форме редактирования
    @admin.display(description="Текущее изображение")
    def image_preview(self, obj):
        if obj and obj.image:
            return mark_safe(f'''
                <div style="margin: 10px 0;">
                    <img src="{obj.image.url}" width="300" style="object-fit: contain; border-radius: 8px; border: 2px solid #ddd;" />
                    <div style="margin-top: 8px; font-size: 12px; color: #666;">
                        <strong>Текущее изображение:</strong><br>
                        {obj.image.name}
                    </div>
                </div>
            ''')
        return mark_safe('<div style="color: #999; font-style: italic;">Изображение не загружено</div>')
    
    @admin.display(description="Цена в USD")
    def price_in_usd(self, obj):
        if obj and obj.price:
            exchange_rate = 95
            usd_price = obj.price / exchange_rate
            return f"${usd_price:.2f}"
        return "$0.00"
    
    @admin.display(description="Возраст игры")
    def game_age(self, obj):
        if obj and obj.year_release:
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
        return "Не указан"
    
    @admin.display(description="Краткая информация")
    def brief_info(self, obj):
        if obj:
            tags_count = obj.tags.count()
            genres_count = obj.genres.count()
            return f"{genres_count} жанра, {tags_count} тегов"
        return "Нет данных"
    
    @admin.action(description="Опубликовать игры")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=True)
        self.message_user(request, f"{count} игр опубликовано", messages.SUCCESS)
    
    @admin.action(description="Скидка 10 процентов")
    def apply_discount_10(self, request, queryset):
        updated_count = 0
        for game in queryset:
            if game.price > 0:
                from decimal import Decimal
                game.price = game.price * Decimal('0.9')
                game.save()
                updated_count += 1
        
        self.message_user(request, f"Скидка применена к {updated_count} играм", messages.SUCCESS)

@admin.register(UploadFiles)
class UploadFilesAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_filename', 'file_preview', 'description', 'file_size_formatted', 'uploaded_at')
    list_display_links = ('id', 'original_filename')
    list_filter = ['uploaded_at']
    search_fields = ['original_filename', 'description']
    readonly_fields = ['uploaded_at', 'file_size', 'original_filename', 'file_preview_large']
    
    fields = [
        'original_filename',
        'file',
        'file_preview_large',
        'description',
        'file_size',
        'uploaded_at',
    ]
    
    def file_size_formatted(self, obj):
        if obj.file_size < 1024:
            return f"{obj.file_size} байт"
        elif obj.file_size < 1024 * 1024:
            return f"{obj.file_size / 1024:.1f} KB"
        else:
            return f"{obj.file_size / (1024 * 1024):.1f} MB"
    file_size_formatted.short_description = 'Размер файла'
    
    @admin.display(description="Файл")
    def file_preview(self, obj):
        if obj.file:
            file_extension = obj.file.name.split('.')[-1].lower()
            if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                return mark_safe(f'<img src="{obj.file.url}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />')
            else:
                return f"📄 {file_extension.upper()}"
        return "❌"
    
    @admin.display(description="Предпросмотр файла")
    def file_preview_large(self, obj):
        if obj.file:
            file_extension = obj.file.name.split('.')[-1].lower()
            if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                return mark_safe(f'''
                    <div style="margin: 10px 0;">
                        <img src="{obj.file.url}" width="300" style="object-fit: contain; border-radius: 8px; border: 2px solid #ddd;" />
                        <div style="margin-top: 8px; font-size: 12px; color: #666;">
                            <strong>Предпросмотр:</strong> {obj.file.name}
                        </div>
                    </div>
                ''')
            else:
                return mark_safe(f'''
                    <div style="margin: 10px 0; padding: 20px; background: #f5f5f5; border-radius: 8px; text-align: center;">
                        <div style="font-size: 48px; margin-bottom: 10px;">📄</div>
                        <div style="font-size: 14px; color: #666;">
                            <strong>Файл:</strong> {obj.original_filename}<br>
                            <strong>Тип:</strong> {file_extension.upper()}
                        </div>
                    </div>
                ''')
        return mark_safe('<div style="color: #999; font-style: italic;">Файл не загружен</div>')

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