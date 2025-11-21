# Telegram Route Planner Bot

Telegram бот для генерации планов маршрутов до дома.

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd doroga
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл `.env` на основе `env.example`:
```bash
cp env.example .env
```

4. Заполните `.env` файл:
```
BOT_TOKEN=ваш_токен_бота
CHAT_ID=ваш_chat_id (опционально, можно получить автоматически)
```

## Получение токена бота

1. Найдите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен в `.env` файл

## Получение Chat ID

Chat ID можно получить двумя способами:

1. **Автоматически**: Запустите бота и отправьте ему любое сообщение. Бот автоматически определит ваш Chat ID.

2. **Вручную**: Добавьте Chat ID в `.env` файл. Чтобы узнать свой Chat ID:
   - Найдите [@userinfobot](https://t.me/userinfobot) в Telegram
   - Отправьте ему любое сообщение
   - Он вернет ваш Chat ID

## Запуск

```bash
python main.py
```

## Деплой

### Heroku

1. Установите [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

2. Создайте приложение:
```bash
heroku create your-app-name
```

3. Установите переменные окружения:
```bash
heroku config:set BOT_TOKEN=your_bot_token
heroku config:set CHAT_ID=your_chat_id
```

4. Деплой:
```bash
git push heroku main
```

### Docker

1. Соберите образ:
```bash
docker build -t route-planner-bot .
```

2. Запустите контейнер:
```bash
docker run --env-file .env route-planner-bot
```

### PythonAnywhere

1. Загрузите файлы через веб-интерфейс или Git
2. Создайте задачу в Task Scheduler:
   - Команда: `python3.10 /home/yourusername/doroga/main.py`
   - Интервал: по необходимости

### VPS/Сервер

1. Установите зависимости:
```bash
pip3 install -r requirements.txt
```

2. Создайте `.env` файл с переменными окружения

3. Настройте cron для автоматического запуска:
```bash
crontab -e
# Добавьте строку (например, каждый день в 8:00):
0 8 * * * cd /path/to/doroga && /usr/bin/python3 main.py
```

## Структура проекта

```
doroga/
├── main.py              # Основной код бота
├── requirements.txt     # Зависимости Python
├── .env                 # Переменные окружения (не коммитится)
├── env.example          # Пример конфигурации
├── .gitignore          # Игнорируемые файлы
└── README.md           # Документация
```

## Безопасность

⚠️ **ВАЖНО**: Никогда не коммитьте файл `.env` в Git! Он содержит чувствительные данные (токен бота).

## Лицензия

MIT

