
# Проект "Трекер привычек"

## Содержание:
- [Описание](#описание)
- [Проверить версию Python](#проверить-версию-python)
- [Установка Poetry](#установка-poetry)
- [Установка](#установка)
- [Тестирование](#тестирование)
- [Запуск проекта](#запуск-проекта)
- [Кастомные команды](#кастомные-команды)
- [Структура проекта](#структура-проекта)
- [Приложение chats](#приложение-chats)
  - [Models chats](#models-chats)
    - [Habit](#habit)
  - [Paginators chats](#paginators-chats)
    - [ChatsPaginator](#chatspaginator)
  - [Serializers chats](#serializers-chats)
    - [HabitCreateSerializer](#habitcreateserializer)
    - [HabitSerializer](#habitserializer)
  - [Validators chats](#validators-chats)
- [Приложение users](#приложение-users)
  - [Admin users](#admin-users)
  - [Models users](#models-users)
    - [User](#user)
  - [Permissions users](#permissions-users)
  - [Serializers users](#serializers-users)
  - [Urls user](#urls-users)
  - [Views user](#views-users)

   
## Описание:

Трекер привычек, работает через телеграм и создан с помощью Django.

[<- на начало](#содержание)


## Проверить версию Python:

Убедитесь, что у вас установлен Python (версия 3.x). Вы можете проверить установленную версию Python, выполнив команду:
```
python --version
```

[<- на начало](#содержание)


## Установка Poetry:
- Если у вас еще не установлен Poetry, вы можете установить его, выполнив следующую команду
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```
- Проверить Poetry добавлен в ваш PATH.
    ```bash
    poetry --version
    ```

[<- на начало](#содержание)


## Установка:
- Клонируйте репозиторий:
    ```bash
    git clone git@github.com:Streiker-Saik/CourseProject5.git
    ```
- Перейдите в директорию проекта:
    ```
    cd CourseProject_4
    ```
### При использовании PIP:
- Активируйте виртуальное окружение
    ```
    python -m venv <имя_вашего окружения>
    <имя_вашего_окружения>\Scripts\activate
    ```
- Установите зависимости
    ```bash
    pip install -r requirements.txt
    ```
### При использование POETRY:
- Активируйте виртуальное окружение
    ```bash
    poetry shell
    ```
- Установите необходимые зависимости:
    ```bash
    poetry install
    ```
- Зайдите в файл .env.example и следуйте инструкция

[<- на начало](#содержание)


## Тестирование:
- Запустить тесты 
  ```bash
  python manage.py test
  ```
- Запустить с покрытием тесты
  ```bash
  coverage run --source='.' manage.py test
  ```
    - Записать/обновить в файл html
    ```bash
    coverage html
    ```
    - Вывести в терминал
    ```bash
    coverage report
    ```

[<- на начало](#содержание)

---
## Запуск проекта:
- Чтобы запустить сервер разработки, выполните следующую команду:
  ```bash
  python manage.py runserver
  ```

[<- на начало](#содержание)

---
## Кастомные команды
### csu
Команда для создания суперпользователя по ключам email, password и chat_id.
Если не указано, то: email='admin@example.com', password='admin', chat_id=1.
```bash
python manage.py csu
```
или
```
python manage.py csu --email ввести_адрес_почты --password ввести_пароль --chat_id ввести_id_телеграмма
```
### cu
Команда для создания пользователя по ключам email, password и chat_id.
```
python manage.py cu --email ввести_адрес_почты --password ввести_пароль --chat_id ввести_id_телеграмма
```

[<- на начало](#содержание)

---
## Структура проекта:
```
DjangoREST/
├── config/
|   ├── __init__.py
|   ├── asgi.py
|   ├── celery.py # настройка Celery
|   ├── settings.py # настройки проекта
|   ├── urls.py # маршрутизация проета
|   └── wsgi.py
├── chats/ # приложение отправки сообщений
|   ├── migrations/ # пакет миграции моделей
|   |   ├── 0001_initial.py
|   |   ├── ...
|   |   └── __init__.py
|   ├── admin.py 
|   ├── apps.py
|   ├── models.py # модели БД
|   ├── paginators.py # права доступа
|   ├── seriazers.py # сериализаторы приложения
|   ├── tasks # отложенные задачи
|   ├── tests.py 
|   ├── urls.py # маршрутизация приложения
|   ├── validators # валидаторы сериализаторов
|   └── views.py # конструктор контроллеров
├── users/ # приложение аутефикации
|   ├── management/
|   |   └── commands
|   |   |   ├── __init__.py
|   |   |   ├── csu.py # Создание суперюзера
|   |   |   └── create_user.py # Создание пользователя
|   |   └── __init__.py
|   ├── migrations/ # пакет миграции моделей
|   |   ├── 0001_initial.py
|   |   ├── ...
|   |   └── __init__.py
|   ├── admin.py 
|   ├── apps.py
|   ├── models.py # модели БД
|   ├── permissions.py # права доступа
|   ├── seriazers.py # сериализаторы приложения
|   ├── tests.py 
|   ├── urls.py # маршрутизация приложения
|   └── views.py # конструктор контроллеров
├── .env
├── .flake8 # настройка для flake8
├── .gitignore
├── poetry.lock
├── pypproject.toml # зависимости для poetry
├── README.md
└── requirements.txt # зависимости для pip
```

[<- на начало](#содержание)

---


# Приложение chats:
## Models chats:
### Habit:
Представление привычки.
- Атрибуты:
  - owner (ForeignKey): Создатель привычки
  - place (str): Место привычки
  - time (datetime): Дата и время выполнения привычки
  - action (str): Действие привычки
  - is_pleasant (bool): Признак приятной привычки
  - related_habit (ForeignKey): Привычка, которая связана с другой привычкой
  - periodicity (int): Периодичность выполнения привычки для напоминания в днях (по умолчанию ежедневная)
  - reward (str): Вознаграждение за привычку
  - time_to_complete (DurationField): Время на выполнение.
  - is_public (bool): Признак, можно ли опубликовать привычку.

[<- на начало](#содержание)

---
## Paginators chats:
### ChatsPaginator:
Пагинатор для приложения chats
К-во элементов 5 (максимум 10) на странице

[<- на начало](#содержание)

---
## Serializers chats:
### HabitCreateSerializer:
Сериализатор для создания модели Habit
- Исключены поля:
  - owner(ForeignKey): Создатель привычки.
### HabitSerializer:
Сериализатор для модели Habit
- Отображаются поля:
  - id(int): Уникальный идентификатор привычки.
  - owner(ForeignKey): Создатель привычки.
  - place (str): Место привычки.
  - time (datetime): Дата и время выполнения привычки
  - action (str): Действие привычки
  - is_pleasant (bool): Признак приятной привычки
  - related_habit (ForeignKey): Привычка, которая связана с другой привычкой
  - periodicity (int): Периодичность выполнения привычки для напоминания в днях (по умолчанию ежедневная)
  - reward (str): Вознаграждение за привычку
  - time_to_complete (DurationField): Время на выполнение.
  - is_public (bool): Признак, можно ли опубликовать привычку.

[<- на начало](#содержание)

---
## Validators chats:
### RelatedOrRewardValidator:
Валидатор проверки одновременно связанная привычка и вознаграждение
ValidationError: Если в заполнено сразу связанная привычка и вознаграждение
### TimeToCompleteValidator:
Валидатор проверки времени на выполнение.
ValidationError: Если время превышает 120 секунд
### RelatedHabitValidator:
Валидатор проверки связанные привычки
ValidationError: Если связанная привычка не является приятной
### IsPleasantValidator:
Валидатор проверки приятной привычки.
ValidationError: Если у приятной привычки есть связанная привычка
ValidationError: Если у приятной привычки есть вознаграждение
### PeriodicityValidator:
Валидатор периода выполнения привычки.
ValidationError: Если период выполнения больше 7 дней

[<- на начало](#содержание)

---
# Приложение users:
## Admin users
### CustomUserAdmin
Класс для работы администратора с пользователями
- Атрибуты:
  - ordering - сортировка по email
  - list_filter - фильтрация активный пользователь или нет
  - exclude - исключит поле пароля
  - list_display - выводит на экран: email, id в телеграмме, супер юзер, сотрудник, активный
  - search_fields - поиск по: email, id в телеграмме

[<- на начало](#содержание)

---
## Models users
### User:
Представление кастомного пользователя, расширяющее AbstractUser.
Поле авторизации с username изменено на email. Так же username обязательное поле при авторизации
- Атрибуты:
  - username: Логин **отключен**
  - email(str): Уникальный email
  - chat_id(int): ID пользователя в телеграмме

[<- на начало](#содержание)

---
## Permissions users:
### IsOwner:
Право владельцам
### IsProfileOwner:
Право владельца профиля

[<- на начало](#содержание)

---
## Serializers users:
### UserSerializer:
Сериализатор для модели Users.
- Показывает поля: 
  - id(int): Уникальный идентификатор пользователя.
  - first_name(str): Имя пользователя.
  - last_name(str): Фамилия пользователя
  - chat_id(id): ID телеграмма пользователя
### UserCreateSerializer:
Сериализатор для создания модели Users.
- Показывает поля:
  - id(int): Уникальный идентификатор пользователя
  - email(str): Почта пользователя
  - chat_id(id): ID телеграмма пользователя
  - password(str): Ввод пароля

[<- на начало](#содержание)

---
## Urls users:
- Получение токена пользователя (доступны методы: **POST**)  
  http://127.0.0.1:8000/users/token/
- Обновление токена пользователя (доступны методы: **POST**)  
  http://127.0.0.1:8000/users/token/refresh/
- Список пользователей (доступны методы: **GET**)
  http://127.0.0.1:8000/users/
- Создание пользователя (доступны методы: **POST**)
  http://127.0.0.1:8000/users/register/
- Получение одного пользователя (доступны методы: **GET**)
  http://127.0.0.1:8000/users/(pk)/
  - где (pk) - это, целое число PrimaryKey, ID пользователя
- Редактирование пользователя (доступны методы: **PUT/PATH**)
  http://127.0.0.1:8000/users/(pk)/update/
  - где (pk) - это, целое число PrimaryKey, ID пользователя
- Удаление пользователя (доступны методы: **DELETE**)
  http://127.0.0.1:8000/users/(pk)/delete/
  - где (pk) - это, целое число PrimaryKey, ID пользователя

[<- на начало](#содержание)

---
## Views users:
### UserListAPIView:
Представление для получения списка всех пользователей (GET)
- Доступ:
  - авторизованному пользователю
### UserCreateAPIView:
Представление для создания пользователя (POST)
- Методы:
  - perform_create(self, serializer) -> None:  
  Сохраняет нового пользователя и устанавливает его активным.
- Доступ:
  - Всем
### UserRetrieveAPIView:
Представление для получения пользователя по идентификатору (GET)
- Доступ:
  - авторизованному пользователю
### UserUpdateAPIView:
Представление для обновления пользователя по идентификатору (PUT/PATH)
- Доступ:
  - авторизованному пользователю:
    - владелец
### UserDestroyAPIView:
Представление для удаления пользователя по идентификатору (DELETE)
- Доступ:
  - сотрудник

[<- на начало](#содержание)

---