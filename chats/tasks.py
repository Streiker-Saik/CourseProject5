import datetime
import logging

import requests
from celery import shared_task
from django.utils import timezone

from chats.models import Habit
from config import settings

logger = logging.getLogger(__name__)


@shared_task
def send_tg_message(chat_id: int, message: str) -> None:
    """Метод отправки сообщений пользователю в телеграмм"""
    params = {
        "text": message,
        "chat_id": chat_id,
    }
    url = f"{settings.TELEGRAM_URL}{settings.BOT_TELEGRAM_TOKEN}/sendMessage"

    requests.get(url, params=params)


@shared_task
def send_habit_reminder() -> None:
    """Отправка напоминаний о выполнении привычки"""

    logger.info("Отправка напоминаний запущена")
    time_now = timezone.now()
    logger.info(f"Текущее время {time_now}")
    # Фильтруем привычки, которые от(включительно) текущего времени и до + час
    habits = (
        Habit.objects.select_related("owner")
        .filter(time__gte=time_now, time__lte=time_now + datetime.timedelta(hours=1))
        .exclude(owner__chat_id__isnull=True)
    )
    logger.info(f"Привычек в этом часу: {len(habits)}")

    for habit in habits.order_by("time"):
        chat_id = habit.owner.chat_id
        logger.info(f"Чат id_user: {chat_id}")
        if chat_id:
            message = f"У вас запланировано выполнение привычки:\n" f"{str(habit)}"
            send_tg_message.delay(chat_id=chat_id, message=message)
        logger.info("Сообщение успешно отправлено")
