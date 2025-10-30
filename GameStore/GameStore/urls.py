from django.contrib import admin
from django.urls import path, include
from games.views import page_not_found

handler404 = page_not_found

admin.site.site_header = "GameStore - Панель администрирования"
admin.site.index_title = "Управление игровым магазином"
admin.site.site_title = "Админка GameStore"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('games.urls')),
]
