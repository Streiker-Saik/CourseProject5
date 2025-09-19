from io import StringIO
from unittest.mock import patch, MagicMock

from django.core.management import call_command
from django.test import TestCase

from django.db import connection
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UsersUserTestCase(APITestCase):

    def setUp(self):
        # Сброс счетчиков до 1
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE users_user_id_seq RESTART WITH 1;")
        # Создание суперпользователя
        self.admin_user = User.objects.create(email="admin@test.com", password="admin", chat_id=1)
        self.admin_user.is_superuser = True
        self.admin_user.is_staff = True
        self.admin_user.save()
        # Создание обычного пользователя
        self.user = User.objects.create(email="user1@test.com", password="user1", chat_id=2)

    def test_list_users(self):
        """Тестирование просмотра списка пользователей"""

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get("/users/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            [
                {
                    "id": self.admin_user.pk,
                    "email": self.admin_user.email,
                    "first_name": "",
                    "last_name": "",
                    "chat_id": 1,
                },
                {"id": self.user.pk, "email": self.user.email, "first_name": "", "last_name": "", "chat_id": 2},
            ],
        )

    def test_create_user(self):
        """Тестирование создания активного пользователя"""
        data = {"email": "user2@test.com", "password": "user2", "chat_id": 3}
        response = self.client.post("/users/register/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email="user1@test.com")
        self.assertTrue(user.is_active)

    def test_retrieve_user(self):
        """Тестирование просмотра пользователя"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/users/{self.user.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {"id": self.user.pk, "email": self.user.email, "first_name": "", "last_name": "", "chat_id": 2},
        )

    def test_partial_update_user(self):
        """Тестирование частичного обновления пользователя"""

        data = {"first_name": "Test"}

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(f"/users/{self.user.pk}/update/", data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f"/users/{self.user.pk}/update/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {"id": self.user.pk, "email": self.user.email, "first_name": "Test", "last_name": "", "chat_id": 2},
        )

    def test_update_user(self):
        """Тестирование обновления пользователя"""

        data = {"email": self.user.email, "first_name": "Test", "chat_id": 123}

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(f"/users/{self.user.pk}/update/", data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.user)
        response = self.client.put(f"/users/{self.user.pk}/update/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {"id": self.user.pk, "email": self.user.email, "first_name": "Test", "last_name": "", "chat_id": 123},
        )

    def test_destroy_user(self):
        """Тестирование удаление пользователя"""

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/users/{self.user.pk}/delete/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f"/users/{self.user.pk}/delete/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_not_authenticated(self):
        """Тестирование доступа не авторизованного пользователя"""
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(f"/users/{self.user.pk}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(f"/users/{self.user.pk}/update/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(f"/users/{self.user.pk}/update/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(f"/users/{self.user.pk}/delete/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserCommandsTestCase(TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_csu(self, mock_stdout: MagicMock):
        """Тестирование команды создания суперпользователя"""
        call_command("csu")
        email_default = "admin@example.com"
        user = User.objects.get(email=email_default)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)

        self.assertEqual(mock_stdout.getvalue(), f"Суперпользователь {email_default} создан успешно!\n")

    @patch("users.models.User.objects.filter")
    @patch('sys.stdout', new_callable=StringIO)
    def test_csu_exists(self, mock_stdout: MagicMock, mock_filter: MagicMock):
        """Тестирование создание суперпользователя, если с данным email пользователь уже есть"""
        mock_filter.return_value.exists.return_value = True
        call_command("csu")
        self.assertEqual(mock_stdout.getvalue(), "Суперпользователь с данным email уже существует.\n")

    @patch('sys.stdout', new_callable=StringIO)
    def test_cu(self, mock_stdout: MagicMock):
        """Тестирование команды создания пользователя"""
        email = "user@example.com"
        password = "user"
        chat_id = 1
        call_command("cu", email=email, password=password, chat_id=chat_id)
        user = User.objects.get(email=email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.chat_id, chat_id)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

        self.assertEqual(mock_stdout.getvalue(), f"Пользователь {email} создан успешно!\n")

    @patch("users.models.User.objects.filter")
    @patch('sys.stdout', new_callable=StringIO)
    def test_cu_exists(self, mock_stdout: MagicMock, mock_filter: MagicMock):
        """Тестирование команды создания пользователя, если с данным email пользователь уже есть"""
        mock_filter.return_value.exists.return_value = True
        call_command("cu")
        self.assertEqual(mock_stdout.getvalue(), "Пользователь с данным email уже существует.\n")
