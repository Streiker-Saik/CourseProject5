import datetime
import logging

from celery import shared_task
from django.utils import timezone

from chats.models import Habit
from chats.services import TelegramService

logger = logging.getLogger(__name__)


@shared_task
def send_habit_reminder() -> None:
    """Отправка напоминаний о выполнении привычки"""

    logger.info("Отправка напоминаний запущена")
    time_now = timezone.now()
    logger.info(f"Текущее время {time_now}")
    # Фильтруем привычки, которые от(включительно) текущего времени и до + час
    habits = Habit.objects.filter(time__gte=time_now, time__lte=time_now + datetime.timedelta(hours=1)).order_by(
        "time"
    )
    logger.info(f"Привычек в этом часу: {len(habits)}")
    try:
        for habit in habits:
            chat_id = habit.owner.chat_id
            logger.info(f"Чат id_user: {chat_id}")
            if chat_id:
                message = f"У вас запланировано выполнение привычки:\n" f"{str(habit)}"
                TelegramService.send_message(chat_id=chat_id, message=message)
            logger.info("Сообщение успешно отправлено")
    except Exception as exc_info:
        logger.error(f"Ошибка {str(exc_info)}")
