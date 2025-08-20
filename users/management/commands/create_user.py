from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Команда для создания пользователя по ключам email и password.
    Методы:
        add_arguments(self, parser):
            Добавляет аргументы команды: email, password.
        handle(self, *args, **options) -> None:
            Обрабатывает команду для создания пользователя.
        custom_create_superuser(email: str, password: str) -> None:
            Кастомное создание пользователя
    """

    help = "Создание пользователя с email и password."

    def add_arguments(self, parser):
        """Добавляет аргументы команды: email, password."""
        parser.add_argument("--email", type=str, help="Email для входя пользователя")
        parser.add_argument("--password", type=str, help="Пароль для входя пользователя")

    def handle(self, *args, **options) -> None:
        """Обрабатывает команду для создания суперпользователя."""
        email = options["email"]
        password = options["password"]
        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR("Пользователь с данным email уже существует."))
        else:
            self.custom_create_user(email, password)
            self.stdout.write(self.style.SUCCESS(f"Пользователь {email} создан успешно!"))

    @staticmethod
    def custom_create_user(email: str, password: str) -> None:
        """Кастомное создание пользователя"""
        user = User.objects.create(email=email)
        user.set_password(password)
        user.is_active = True
        user.save()
