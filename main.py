import random
import requests
from datetime import datetime, timedelta


class RoutePlannerBot:
    def __init__(self):
        self.bot_token = "8429153542:AAHEvX3Ow-AdfHg6Lc5chRi5V6OWj8-ALT8"
        self.chat_id = None  # Нужно получить
        self.telegram_url = f"https://api.telegram.org/bot{self.bot_token}/"

        self.route_options = {
            "Маршрутка+элка+пешком": "🚌 Музыка новая",
            "Автобус X+пешком от фабрики": "🚇Тишина",
            "Маршрутка+338": "🚕 Подкаст",
            "Автобус X + длинная прогулка": "🚶 Подкаст",
            "Автобус X + 889": "🚴 Музыка новая"
        }

    def get_chat_id(self):
        """Получить Chat ID автоматически"""
        url = self.telegram_url + "getUpdates"
        try:
            response = requests.get(url)
            updates = response.json()

            if updates["result"]:
                self.chat_id = updates["result"][0]["message"]["chat"]["id"]
                print(f"✅ Chat ID получен: {self.chat_id}")
                return True
            else:
                print("❌ Напишите сообщение боту и попробуйте снова")
                return False
        except Exception as e:
            print(f"❌ Ошибка получения chat_id: {e}")
            return False

    def send_message(self, text):
        """Отправка сообщения в Telegram"""
        if not self.chat_id:
            if not self.get_chat_id():
                return False

        url = self.telegram_url + "sendMessage"
        data = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML"
        }

        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print("✅ Сообщение отправлено в Telegram")
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


# Использование
def main():
    bot = RoutePlannerBot()

    print("🤖 Бот маршрутов запущен!")
    print("📱 Напишите любое сообщение вашему боту в Telegram")

    # Получаем chat_id
    if bot.get_chat_id():
        plan = bot.generate_route_plan(5)
        bot.send_message(plan)
        print("✅ План отправлен в Telegram!")
    else:
        print("❌ Не удалось получить chat_id")


if __name__ == "__main__":
    main()