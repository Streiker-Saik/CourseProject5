from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from users.models import User
from users.permissions import IsProfileOwner
from users.serializers import UserCreateSerializer, UserSerializer


class UserListAPIView(ListAPIView):
    """
    Представление для получения списка всех пользователей (GET)
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateAPIView(CreateAPIView):
    """
    Представление для создания пользователя (POST)
    Методы:
        perform_create(self, serializer) -> None:
            Сохраняет нового пользователя и устанавливает его активным.
    """

    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer) -> None:
        """Сохраняет нового пользователя и устанавливает его активным."""
        serializer.save(is_active=True)


class UserRetrieveAPIView(RetrieveAPIView):
    """
    Представление для получения пользователя по идентификатору (GET)
    Методы:
        get_serializer_class(self):
            Определяет, какой сериализатор использовать для ответа.
            Возвращает UserSerializer для администраторов и владельца,
            а UserGeneralSerializer для обычных пользователей.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateAPIView(UpdateAPIView):
    """Представление для обновления пользователя по идентификатору (PUT/PATH)"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsProfileOwner]

    @swagger_auto_schema(operation_description="Полное обновление пользователя", operation_id="users_update")
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Частичное обновление пользователя", operation_id="users_partial_update"
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class UserDestroyAPIView(DestroyAPIView):
    """Представление для удаления пользователя по идентификатору (DELETE)"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(operation_id="users_delete")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
