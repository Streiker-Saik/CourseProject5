from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    """
    Сериализатор для модели Users.
    Показывает поля:
        id(int): Уникальный идентификатор пользователя.
        first_name(str): Имя пользователя.
        last_name(str): Фамилия пользователя.
        chat_id(id): ID телеграмма пользователя
    """

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "chat_id",)


class UserCreateSerializer(ModelSerializer):
    """
    Сериализатор для создания модели Users.
    Показывает поля:
        id(int): Уникальный идентификатор пользователя
        email(str): Почта пользователя
        chat_id(id): ID телеграмма пользователя
        password(str): Ввод пароля
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "chat_id", "password")

    def create(self, validated_data):
        """Создает нового пользователя и хэширует его пароль."""
        user = User(**validated_data)
        user.set_password(validated_data.pop("password"))
        user.save()
        return user



