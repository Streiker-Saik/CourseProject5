from django.db.models import QuerySet
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from chats.models import Habit
from chats.paginators import ChatsPaginator
from chats.serializers import HabitCreateSerializer, HabitSerializer
from users.permissions import IsOwner


class HabitListAPIView(ListAPIView):
    """
    Представление для получения списка всех привычек (GET).
    Методы:
        get_queryset(self) -> QuerySet:
            Возвращает queryset привычек, принадлежащих аутентифицированному пользователю.
    """

    serializer_class = HabitSerializer
    pagination_class = ChatsPaginator

    @swagger_auto_schema(operation_id="habits_user_list")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet:
        """
        Возвращает queryset привычек, принадлежащих аутентифицированному пользователю.
        :return: QuerySet Habit
        """

        user = self.request.user
        return Habit.objects.filter(owner=user).order_by("id")


class PublicHabitListAPIView(ListAPIView):
    """
    Представление для получения списка всех публичных привычек (GET).
    """

    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_public=True).order_by("id")
    pagination_class = ChatsPaginator

    @swagger_auto_schema(operation_id="habits_public_list")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class HabitCreateAPIView(CreateAPIView):
    """
    Представление для создания новой привычки (POST)
    Методы:
        perform_create(self, serializer) -> None:
            Сохраняет новую привычку с текущим пользователем как владельцем.
    """

    serializer_class = HabitCreateSerializer

    @swagger_auto_schema(operation_id="habit_create")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer) -> None:
        """Сохраняет новую привычку с текущим пользователем как владельцем."""
        serializer.save(owner=self.request.user)


class HabitRetrieveAPIView(RetrieveAPIView):
    """Представление для получения привычки по идентификатору (GET)"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()

    @swagger_auto_schema(operation_id="habit_read")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class HabitUpdateAPIView(UpdateAPIView):
    """Представление для обновления привычки по идентификатору (PUT/PATH)"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsOwner,
    )

    @swagger_auto_schema(operation_description="Полное обновление привычки", operation_id="habit_update")
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Частичное обновление привычки", operation_id="habit_partial_update")
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class HabitDestroyAPIView(DestroyAPIView):
    """Представление для удаления привычки по идентификатору (DELETE)"""

    queryset = Habit.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsOwner,
    )

    @swagger_auto_schema(operation_id="habit_delete")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
