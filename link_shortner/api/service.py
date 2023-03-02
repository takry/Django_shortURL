from django.http import HttpResponse
from django.shortcuts import redirect

from .models import Tokens


def get_full_url(url: str) -> str:
    """
    Достаем полную ссылку по short_url
    Если ссылки нет в базе или она не активна
    возвращаем ошибку.
    Если все ок, то добавляем к счетчику статистики 1
    и возвращаем полную ссылку.
    """
    try:  # Пробуем достать токен, если его нет райзим ошибку, если он есть но не активен - райзим ошибку.
        token = Tokens.objects.get(short_url__exact=url)
        if not token.is_active:
            raise KeyError('Token is no longer available')
    except Tokens.DoesNotExist:
        raise KeyError('Try another url. No such urls in DB')
    token.requests_count += 1  # добавляем 1 к счетчику в случае удачного извлечения токена
    token.save() # сохраняем изменный экземпляр токена в БД 
    return token.full_url


def redirection(request, short_url):
    """Перенаправляем пользователя по ссылке"""
    try:
        full_link = get_full_url(short_url)  # получает полный адрес по короткой ссылке
        return redirect(full_link)  # перенаправляем пользователя по ссылке
    except Exception as e:
        return HttpResponse(e.args)  # если что-то не так, райзим ошибку