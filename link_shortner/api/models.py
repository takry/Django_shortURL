from django.db import models
import random  # импортируем модуль random для генерации короткой ссылки

from django.conf import settings  # подтягиваем значение констант из фала настроек

class Tokens(models.Model):
    """Модель для хранения токенов"""
    full_url = models.URLField(unique=True)
    short_url = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        blank=True
    )
    requests_count = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_date',)  # сортировка по дате создания токена

    def save(self, *args, **kwargs):
        """
        При создании токена достаточно только полной ссылки,
        короткая ссылка генерируется автоматически.
        Перед сохранением объекта токен проверяется на уникальность
        """
        if not self.short_url:
            while True:  # цикл будет повторять до тех пор пока не сгенерирует уникальную ссылку
                self.short_url = ''.join(
                    random.choices(
                        settings.CHARACTERS,  # алфавит для генерации короткой ссылки мы будем хранить в файле настроек
                        k=settings.TOKEN_LENGTH  # длину короткой ссылки тоже
                    )
                )
                if not Tokens.objects.filter(  # проверка на уникальность
                    short_url=self.short_url
                ).exists():
                    break
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.short_url} -> {self.full_url}'