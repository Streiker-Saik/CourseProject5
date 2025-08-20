from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Представление кастомного пользователя, расширяющее AbstractUser.
    Поле авторизации с username изменено на email.
    Так же username обязательное поле при авторизации
    Атрибуты:
        username: Логин отключен
        email(str): Уникальный email
        chat_id(int): ID пользователя в телеграмме
    """

    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    chat_id = models.IntegerField(
        verbose_name="ID пользователя",
        help_text="Введите свой ID пользователя в телеграмме"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["chat_id"]

    def __str__(self) -> str:
        """
        Строковое представление класса.
        :return: Email
        """
        return f"{self.email}"

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
