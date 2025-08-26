import requests

from config import settings


class TelegramService:
    """
    Сервисный класс работы с Telegram
    Методы:
        send_message(chat_id: int, message: str) -> None
            Метод отправки сообщений пользователю в телеграмм
    """

    @staticmethod
    def send_message(chat_id: int, message: str) -> None:
        """Метод отправки сообщений пользователю в телеграмм"""
        params = {
            "text": message,
            "chat_id": chat_id,
        }
        url = f"{settings.TELEGRAM_URL}{settings.BOT_TELEGRAM_TOKEN}/sendMessage"

        requests.get(url, params=params)
