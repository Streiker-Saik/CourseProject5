import datetime

from django.db import models
from django.utils import timezone

from config import settings


class Habit(models.Model):
    """
    Представление привычки.
    Атрибуты:
        owner (ForeignKey): Создатель привычки
        place (str): Место привычки
        time (datetime): Дата и время выполнения привычки
        action (str): Действие привычки
        is_pleasant (bool): Признак приятной привычки
        related_habit (ForeignKey): Привычка, которая связана с другой привычкой
        periodicity (int): Периодичность выполнения привычки для напоминания в днях (по умолчанию ежедневная)
        reward (str): Вознаграждение за привычку
        time_to_complete (DurationField): Время на выполнение.
        is_public (bool): Признак, можно ли опубликовать привычку.
    """

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        related_name="habits",
        verbose_name="Создатель привычки",
        help_text="Введите ID создателя привычки (пользователя)",
    )
    place = models.CharField(max_length=255, verbose_name="Место", help_text="Введите место выполнения")
    time = models.DateTimeField(verbose_name="Время", help_text="Введите время начала")
    action = models.CharField(max_length=255, verbose_name="Действие", help_text="Введите действия привычки")
    is_pleasant = models.BooleanField(
        default=False, verbose_name="Признак приятной привычки", help_text="Отметьте, если привычка является приятной"
    )
    related_habit = models.ForeignKey(
        "self",
        models.SET_NULL,
        related_name="habits",
        blank=True,
        null=True,
        verbose_name="Связанная привычка",
        help_text="Введите ID связанной привычки, если она есть",
    )
    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name="Периодичность выполнения",
        help_text="Введите периодичность выполнения привычки в днях",
    )
    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Вознаграждение",
        help_text="Введите вознаграждение за выполнение привычки",
    )
    time_to_complete = models.DurationField(
        verbose_name="Время на выполнение", help_text="Введите приблизительное время на выполнение привычки"
    )
    is_public = models.BooleanField(
        default=False, verbose_name="Признак публичности", help_text="Отметьте, если привычку можно публиковать"
    )

    def __str__(self) -> str:
        """
        Строковое представление привычки
        :return: Действие: <action>. Время: <time>. Место: <place>.
        """

        time_utc = self.time
        # устанавливаем время для текущего часового пояса, если часовой пояс не указан устанавливаем в текущую
        if isinstance(time_utc, datetime.datetime):
            local_time = time_utc.astimezone(timezone.get_current_timezone())
        else:
            local_time = timezone.make_aware(self.time)
        return f"Действие: {self.action}, Время: {local_time.strftime('%H:%M:%S')}, Место: {self.place}"

    class Meta:
        verbose_name = "привычка"
        verbose_name_plural = "привычки"
