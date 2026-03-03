import pytz
from datetime import datetime
from typing import List

from config.config import settings

class Notifier:
    def __init__(self):
        self.timezone = pytz.timezone(settings.NOTIFICATION_TIMEZONE)

    def format_message(self, manager: dict) -> str:
        name = manager["name"]
        count = manager["count"]

        # Склоняем слово "откликов"
        if count % 10 == 1 and count % 100 != 11:
            word = "отклик"
        elif 2 <= count % 10 <= 4 and (count % 100 < 10 or count % 100 >= 20):
            word = "отклика"
        else:
            word = "откликов"

        return f"Здравствуйте, {name}! У вас {count} новых {word}, требующих обработки."

    def send_notification(self, manager: dict) :
        message = self.format_message(manager)
        timestamp = datetime.now(self.timezone).isoformat()
        print("\n" + "=" * 50)
        print(f"📧 УВЕДОМЛЕНИЕ ДЛЯ МЕНЕДЖЕРА #{manager['manager_id']}")
        print(f"👤 {manager['manager_name']}")
        print(f"📊 Новых откликов: {manager['new_responses_count']}")
        print(f"📝 Сообщение: {message}")
        print(f"🕐 {timestamp}")
        print("=" * 50 + "\n")

    async def send_bulk_notifications(self, managers: dict):
        results = []
        for manager in managers:
            if manager.new_responses_count > 0:
                result = self.send_notification(manager)
                results.append(result)
