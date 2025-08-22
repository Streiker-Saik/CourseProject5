from rest_framework import serializers

from chats.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Habit
    Отображаются поля:
        id(int): Уникальный идентификатор привычки.
        owner(ForeignKey): Создатель привычки.
        place (str): Место привычки.
        time (datetime): Дата и время выполнения привычки
        action (str): Действие привычки
        is_pleasant (bool): Признак приятной привычки
        related_habit (ForeignKey): Привычка, которая связана с другой привычкой
        periodicity (int): Периодичность выполнения привычки для напоминания в днях (по умолчанию ежедневная)
        reward (str): Вознаграждение за привычку
        time_to_complete (DurationField): Время на выполнение.
        is_public (bool): Признак, можно ли опубликовать привычку.
    """

    class Meta:
        model = Habit
        exclude = "__all__"
