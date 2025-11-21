import random
import os
import requests
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()


class RoutePlannerBot:
    def __init__(self):
        self.bot_token = os.getenv("BOT_TOKEN")
        if not self.bot_token:
            raise ValueError("BOT_TOKEN не найден в переменных окружения. Создайте .env файл с BOT_TOKEN")
        
        self.telegram_url = f"https://api.telegram.org/bot{self.bot_token}/"
        self.last_update_id = 0  # Для отслеживания последнего обработанного обновления

        self.route_options = {
            "Маршрутка+элка+пешком": "🚌 Музыка новая",
            "Автобус X+пешком от фабрики": "🚇Тишина",
            "Маршрутка+338": "🚕 Подкаст",
            "Автобус X + длинная прогулка": "🚶 Подкаст",
            "Автобус X + 889": "🚴 Музыка новая"
        }

    def send_message(self, chat_id, text):
        """Отправка сообщения в Telegram"""
        url = self.telegram_url + "sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }

        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print(f"✅ Сообщение отправлено в чат {chat_id}")
                return True
            else:
                print(f"❌ Ошибка отправки: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return False

    def generate_route_plan(self, days=5):
        """Генерация плана маршрутов"""
        today = datetime.now()

        message = "🏠 <b>ПЛАН МАРШРУТОВ ДО ДОМА</b> 🏠\n\n"

        for day in range(1, days + 1):
            route, description = random.choice(list(self.route_options.items()))
            date = today + timedelta(days=day - 1)

            message += f"<b>День {day}</b> ({date.strftime('%d.%m')})\n"
            message += f"📍 Маршрут: <b>{route}</b>\n"
            message += f"📝 {description}\n"

            if day < days:
                message += "━━━━━━━━━━━━━━━━━━━━\n"

        message += f"\n🎲 Сгенерировано: {datetime.now().strftime('%d.%m.%Y %H:%M')}"

        return message

    def get_updates(self):
        """Получение обновлений от Telegram (long polling)"""
        url = self.telegram_url + "getUpdates"
        params = {
            "offset": self.last_update_id + 1,
            "timeout": 30  # Long polling на 30 секунд
        }

        try:
            response = requests.get(url, params=params, timeout=35)
            if response.status_code == 200:
                data = response.json()
                if data.get("ok"):
                    return data.get("result", [])
            return []
        except Exception as e:
            print(f"❌ Ошибка получения обновлений: {e}")
            return []

    def process_message(self, message):
        """Обработка входящего сообщения"""
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "")
        message_id = message.get("message_id")
        
        if chat_id:
            print(f"📨 Получено сообщение от {chat_id}: {text}")
            # Генерируем и отправляем план маршрутов
            plan = self.generate_route_plan(5)
            self.send_message(chat_id, plan)
            return True
        return False

    def run(self):
        """Основной цикл работы бота"""
        print("🤖 Бот маршрутов запущен!")
        print("📱 Ожидание сообщений...")
        print("💡 Отправьте любое сообщение боту, и он сгенерирует план маршрутов\n")

        while True:
            try:
                updates = self.get_updates()
                
                for update in updates:
                    update_id = update.get("update_id")
                    self.last_update_id = update_id

                    # Обрабатываем сообщения
                    if "message" in update:
                        message = update["message"]
                        self.process_message(message)

                # Небольшая задержка перед следующим запросом
                time.sleep(1)

            except KeyboardInterrupt:
                print("\n\n🛑 Бот остановлен пользователем")
                break
            except Exception as e:
                print(f"❌ Ошибка в основном цикле: {e}")
                time.sleep(5)  # Пауза при ошибке


# Использование
def main():
    try:
        bot = RoutePlannerBot()
        bot.run()
    except ValueError as e:
        print(f"❌ {e}")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")


if __name__ == "__main__":
    main()