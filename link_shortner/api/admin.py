from django.contrib import admin
from .models import Tokens  # импортируем модель Tokens


@admin.register(Tokens)
class TokenAdmin(admin.ModelAdmin):
    """Настройки админки для модели Токенов"""
    list_display = (  # указываем список отображаемых полей
        'full_url',
        'short_url',
        'requests_count',
        'created_date',
        'is_active'
    )
    search_fields = ('full_url', 'short_url')  # поля по которым можно искать нужный токен
    ordering = ('-created_date',)  # все токены отсортируем по дате создания так чтобы последние были сверху
