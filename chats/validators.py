import datetime

from rest_framework.validators import ValidationError


class RelatedOrRewardValidator:
    """
    Валидатор проверки одновременно связанная привычка и вознаграждение
    ValidationError: Если в заполнено сразу связанная привычка и вознаграждение
    """

    def __init__(self, related_field: str, reward_field: str) -> None:
        """
        Инициализатор валидатора.
        :param related_field: Название поля связанной привычки
        :param reward_field: Поля вознаграждение за привычку
        """

        self.related_field = related_field
        self.reward_field = reward_field

    def __call__(self, value: dict) -> None:
        """
        Проверяет что одновременно не заполнен поля: related_habit и reward.
        :param value: Словарь, содержащий проверяемое значение
        :raise ValidationError: Если в заполнено сразу связанная привычка и вознаграждение
        """

        if value.get(self.related_field) and value.get(self.reward_field):
            raise ValidationError("Не может быть заполнено одновременно: связанная привычка и вознаграждение")


class TimeToCompleteValidator:
    """
    Валидатор проверки времени на выполнение.
    ValidationError: Если время превышает 120 секунд
    """

    def __init__(self, time_to_complete_field: str) -> None:
        """
        Инициализатор валидатора.
        :param time_to_complete_field: Поля времени на выполнения
        """

        self.time_to_complete_field = time_to_complete_field

    def __call__(self, value: dict) -> None:
        """
        Проверяет, что время на выполнение не превышает 120 секунд.
        :param value: Словарь, содержащий проверяемое значение
        :raise ValidationError: Если время превышает 120 секунд
        """
        time_to_complete = value.get(self.time_to_complete_field)
        if time_to_complete:
            if time_to_complete > datetime.timedelta(seconds=120):
                raise ValidationError("Время на выполнение не может превышать 120 секунд")


class RelatedHabitValidator:
    """
    Валидатор проверки связанные привычки
    ValidationError: Если связанная привычка не является приятной
    """

    def __init__(self, related_field: str) -> None:
        """
        Инициализатор валидатора.
        :param related_field: Поля связанной привычки
        """

        self.related_field = related_field

    def __call__(self, value: dict) -> None:
        """
        Проверяет, что связанная привычка является приятной.
        :param value: Словарь, содержащий проверяемое значение
        :raise ValidationError: Если связанная привычка не является приятной
        """

        tmp_value = value.get(self.related_field)
        if tmp_value:
            if not tmp_value.is_pleasant:
                raise ValidationError("Связанна привычка должна быть приятной")


class IsPleasantValidator:
    """
    Валидатор проверки приятной привычки.
    ValidationError: Если у приятной привычки есть связанная привычка
    ValidationError: Если у приятной привычки есть вознаграждение
    """

    def __init__(self, is_pleasant_field: str) -> None:
        """
        Инициализатор валидатора.
        :param is_pleasant_field: Поля признака приятной привычки
        """

        self.is_pleasant_field = is_pleasant_field

    def __call__(self, value: dict) -> None:
        """
        Проверяет, что связанная привычка является приятной.
        :param value: Словарь, содержащий проверяемое значение
        :raise ValidationError: Если у приятной привычки есть связанная привычка
        :raise ValidationError: Если у приятной привычки есть вознаграждение
        """

        is_pleasant = value.get(self.is_pleasant_field)
        if is_pleasant:
            related_habit = value.get("related_habit")
            reward = value.get("reward")
            if related_habit:
                raise ValidationError("У приятной привычки не может быть связанной привычки")
            if reward:
                raise ValidationError("У приятной привычки не может быть вознаграждения")


class PeriodicityValidator:
    """
    Валидатор периода выполнения привычки.
    ValidationError: Если период выполнения больше 7 дней
    """

    def __init__(self, periodicity_field: str) -> None:
        """
        Инициализатор валидатора.
        :param periodicity_field: Поля периодичности выполнения привычки
        """

        self.periodicity_field = periodicity_field

    def __call__(self, value: dict) -> None:
        """
        Проверяет, что связанная привычка является приятной.
        :param value: Словарь, содержащий проверяемое значение
        :raise ValidationError: Если период выполнения больше 7 дней
        """
        periodicity_field = value.get(self.periodicity_field)
        if periodicity_field:
            if value.get(self.periodicity_field) > 7:
                raise ValidationError("Нельзя выполнять привычку реже чем 1 раз в 7 дней")
