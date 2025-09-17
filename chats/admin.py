from django.contrib import admin

from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """
    Класс для работы администратора с привычками
    Атрибуты:
        ordering - сортировка: владельцу
        list_filter - фильтрация: приятная привычка, публичная
        list_display - выводит на экран: владелец, признак приятной, связанная привычка, вознаграждение, публичная
        search_fields - поиск по: владельцу
    """

    ordering = ("owner",)
    list_filter = (
        "is_pleasant",
        "is_public",
    )
    list_display = ("owner", "is_pleasant", "related_habit", "reward", "is_public")
    search_fields = ("owner",)
