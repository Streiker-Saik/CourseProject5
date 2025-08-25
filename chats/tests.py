from django.db import connection
from rest_framework import status

from rest_framework.test import APITestCase
from chats.models import Habit
from users.models import User


class ChatsHabitTestCase(APITestCase):

    def setUp(self):
        # Сброс счетчиков до 1
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE users_user_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE chats_habit_id_seq RESTART WITH 1;")
        # Создание обычного пользователя
        self.user = User.objects.create(email="user1@test.com", password="user1", chat_id=2)
        self.client.force_authenticate(user=self.user)
        self.habit_pleasant = Habit.objects.create(
            owner=self.user,
            place="Кухня",
            time="2025-08-26T08:00:00+03:00",
            action="Приготовить смузи",
            is_pleasant=True,
            periodicity=1,
            time_to_complete="00:01:30",
            is_public=True
        )
        self.habit_and_related_habit = Habit.objects.create(
            owner=self.user,
            place="Дом",
            time="2025-08-26T07:00:00+03:00",
            action="Провести утреннюю зарядку",
            related_habit=self.habit_pleasant,
            periodicity=1,
            time_to_complete="00:02:00",
            is_public=True
        )
        self.habit_and_reward = Habit.objects.create(
            owner=self.user,
            place="Офис",
            time="2025-08-26T09:00:00+03:00",
            action="Сделать перерыв на разминку",
            periodicity=1,
            reward="Чаша любимого супа на обед",
            time_to_complete="00:01:00",
        )

    def test_list_habit_public(self) -> None:
        """Тестирование просмотра списка публичных привычек"""
        response = self.client.get("/chats/habits/public/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.habit_pleasant.pk,
                        "place": "Кухня",
                        "time": "2025-08-26T08:00:00+03:00",
                        "action": "Приготовить смузи",
                        "is_pleasant": True,
                        "periodicity": 1,
                        "reward": None,
                        "time_to_complete": "00:01:30",
                        "is_public": True,
                        "owner": self.user.pk,
                        "related_habit": None,
                    },
                    {
                        "id": self.habit_and_related_habit.pk,
                        "owner": self.user.pk,
                        "place": "Дом",
                        "time": "2025-08-26T07:00:00+03:00",
                        "action": "Провести утреннюю зарядку",
                        "is_pleasant": False,
                        "related_habit": self.habit_pleasant.pk,
                        "periodicity": 1,
                        "reward": None,
                        "time_to_complete": "00:02:00",
                        "is_public": True
                    },
                ],
            }
        )

    def test_list_habit_user(self) -> None:
        """Тестирование просмотра списка привычек пользователя"""
        response = self.client.get("/chats/habits/my/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "count": 3,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.habit_pleasant.pk,
                        "owner": self.user.pk,
                        "place": "Кухня",
                        "time": "2025-08-26T08:00:00+03:00",
                        "action": "Приготовить смузи",
                        "is_pleasant": True,
                        "related_habit": None,
                        "periodicity": 1,
                        "reward": None,
                        "time_to_complete": "00:01:30",
                        "is_public": True,
                    },
                    {
                        "id": self.habit_and_related_habit.pk,
                        "owner": self.user.pk,
                        "place": "Дом",
                        "time": "2025-08-26T07:00:00+03:00",
                        "action": "Провести утреннюю зарядку",
                        "is_pleasant": False,
                        "related_habit": self.habit_pleasant.pk,
                        "periodicity": 1,
                        "reward": None,
                        "time_to_complete": "00:02:00",
                        "is_public": True
                    },
                    {
                        "id": self.habit_and_reward.pk,
                        "owner": self.user.pk,
                        "place": "Офис",
                        "time": "2025-08-26T09:00:00+03:00",
                        "action": "Сделать перерыв на разминку",
                        "is_pleasant": False,
                        "related_habit": None,
                        "periodicity": 1,
                        "reward": "Чаша любимого супа на обед",
                        "time_to_complete": "00:01:00",
                        "is_public": False
                    },
                ]
            }
        )

    def test_create_habit(self) -> None:
        """Тестирование создания привычки"""
        data = {
            "place": "Улица",
            "time": "2025-08-26T17:00:00",
            "action": "Прогулка на свежем воздухе",
            "is_pleasant": True,
            "periodicity": 1,
            "time_to_complete": "00:01:00",
            "owner": self.user.pk
        }
        response = self.client.post("/chats/habits/create/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        latest_habit = Habit.objects.latest("pk")
        self.assertEqual(
            response.json(),
            {
                "id": latest_habit.pk,
                "place": "Улица",
                "time": "2025-08-26T17:00:00+03:00",
                "action": "Прогулка на свежем воздухе",
                "is_pleasant": True,
                "related_habit": None,
                "periodicity": 1,
                "reward": None,
                "time_to_complete": "00:01:00",
                "is_public": False
            },
        )
        habit = Habit.objects.get(id=latest_habit.pk)
        self.assertEqual(habit.owner, self.user)

    def test_retrieve_habit(self) -> None:
        """Тестирование просмотра привычки"""
        response = self.client.get(f"/chats/habits/{self.habit_pleasant.pk}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "id": self.habit_pleasant.pk,
                "place": "Кухня",
                "time": "2025-08-26T08:00:00+03:00",
                "action": "Приготовить смузи",
                "is_pleasant": True,
                "periodicity": 1,
                "reward": None,
                "time_to_complete": "00:01:30",
                "is_public": True,
                "owner": self.user.pk,
                "related_habit": None,
            },
        )

    def test_partial_update_habit(self) -> None:
        """Тестирование частичного обновления привычки"""

        data = {"time_to_complete": "00:02:00"}
        response = self.client.patch(f"/chats/habits/{self.habit_pleasant.pk}/update/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": self.habit_pleasant.pk,
                "place": "Кухня",
                "time": "2025-08-26T08:00:00+03:00",
                "action": "Приготовить смузи",
                "is_pleasant": True,
                "periodicity": 1,
                "reward": None,
                "time_to_complete": "00:02:00",
                "is_public": True,
                "owner": self.user.pk,
                "related_habit": None,
            },
        )

    def test_update_habit(self) -> None:
        """Тестирование полного обновления привычки"""

        data = {
            "place": "Кухня",
            "time": "2025-08-26T08:00:00+03:00",
            "action": "Приготовить смузи",
            "is_pleasant": True,
            "periodicity": 1,
            "time_to_complete": "00:02:00",
            "is_public": True,
            "owner": self.user.pk,
        }
        response = self.client.put(f"/chats/habits/{self.habit_pleasant.pk}/update/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "id": self.habit_pleasant.pk,
                "place": "Кухня",
                "time": "2025-08-26T08:00:00+03:00",
                "action": "Приготовить смузи",
                "is_pleasant": True,
                "periodicity": 1,
                "reward": None,
                "time_to_complete": "00:02:00",
                "is_public": True,
                "owner": self.user.pk,
                "related_habit": None,
            },
        )

    def test_destroy_habit(self) -> None:
        """Тестирование удаления привычки"""

        response = self.client.delete(f"/chats/habits/{self.habit_pleasant.pk}/delete/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Habit.objects.filter(id=self.habit_pleasant.pk).exists())

    def test_invalid_reward_and_related_habit(self) -> None:
        """Тестирование изменения привычки, при наличии вознаграждения и связанной привычки сразу"""
        data = {"reward": "Вознаградить себя", "related_habit": self.habit_pleasant.pk}
        response = self.client.patch(f"/chats/habits/{self.habit_and_related_habit.pk}/update/", data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Не может быть заполнено одновременно: связанная привычка и вознаграждение",
            response.data.get("non_field_errors"),
        )

    def test_invalid_time_to_complete(self) -> None:
        """Тестирование изменения привычки, при завышенном времени на выполнение"""
        data = {"time_to_complete": "00:02:10"}
        response = self.client.patch(f"/chats/habits/{self.habit_pleasant.pk}/update/", data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Время на выполнение не может превышать 120 секунд",
            response.data.get("non_field_errors"),
        )

    def test_invalid_related_habit(self) -> None:
        """Тестирование изменения привычки, при указании связанной привычки без признака приятной"""
        data = {"related_habit": self.habit_and_reward.pk}
        response = self.client.patch(f"/chats/habits/{self.habit_and_related_habit.pk}/update/", data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Связанна привычка должна быть приятной",
            response.data.get("non_field_errors"),
        )

    def test_invalid_is_pleasant_and_reward(self) -> None:
        """Тестирование изменения привычки, при приятной привычке не должно быть вознаграждение"""

        data = {"is_pleasant": True, "reward": "Вознаградить себя"}
        response = self.client.patch(f"/chats/habits/{self.habit_pleasant.pk}/update/", data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "У приятной привычки не может быть вознаграждения",
            response.data.get("non_field_errors"),
        )

    def test_invalid_is_pleasant(self) -> None:
        """Тестирование изменения привычки, при приятной привычке не должно быть связанной привычки"""

        data = {"is_pleasant": True, "related_habit": self.habit_and_reward.pk}
        response = self.client.patch(f"/chats/habits/{self.habit_pleasant.pk}/update/", data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "У приятной привычки не может быть связанной привычки",
            response.data.get("non_field_errors"),
        )

    def test_invalid_periodicity(self) -> None:
        """Тестирование изменения привычки, с некорректной периодичностью"""

        data = {"periodicity": 8}
        response = self.client.patch(f"/chats/habits/{self.habit_pleasant.pk}/update/", data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Нельзя выполнять привычку реже чем 1 раз в 7 дней",
            response.data.get("non_field_errors"),
        )

class PermChatsHabitTestCase(APITestCase):

    def setUp(self):
        # Сброс счетчиков до 1
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE users_user_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE chats_habit_id_seq RESTART WITH 1;")
        # Создание обычного пользователя
        self.user = User.objects.create(email="user1@test.com", password="user1", chat_id=2)

        self.habit_pleasant = Habit.objects.create(
            owner=self.user,
            place="Кухня",
            time="2025-08-26T08:00:00+03:00",
            action="Приготовить смузи",
            is_pleasant=True,
            periodicity=1,
            time_to_complete="00:01:30",
            is_public=False
        )

    def test_not_authenticated(self) -> None:
        """Тестирование доступа не авторизованного пользователя"""
        response = self.client.get("/chats/habits/public/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get("/chats/habits/my/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post("/chats/habits/create/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(f"/chats/habits/{self.habit_pleasant.pk}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(f"/chats/habits/{self.habit_pleasant.pk}/update/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(f"/chats/habits/{self.habit_pleasant.pk}/update/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(f"/chats/habits/{self.habit_pleasant.pk}/delete/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_permissions(self) -> None:
        """Тестирование доступа без наличия прав владельца"""

        self.user_2 = User.objects.create(email="user2@test.com", password="user2", chat_id=3)
        self.client.force_authenticate(user=self.user_2)

        response = self.client.patch(f"/chats/habits/{self.habit_pleasant.pk}/update/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.put(f"/chats/habits/{self.habit_pleasant.pk}/update/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(f"/chats/habits/{self.habit_pleasant.pk}/delete/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)