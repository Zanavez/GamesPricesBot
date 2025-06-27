# GamesPricesBot

Telegram бот для отслеживания цен на игры.

## Установка

1. Клонируйте репозиторий:
```bash
git clone <your-repo-url>
cd GamesPricesBot
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
venv\Scripts\activate  # для Windows
# или
source venv/bin/activate  # для Linux/macOS
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте переменные окружения:
   - Скопируйте `.env.example` в `.env`
   - Заполните `.env` файл вашими данными:
```
BOT_TOKEN=your_bot_token_here
```

## Запуск

```bash
python main.py
```

## Структура проекта

- `main.py` - точка входа в приложение
- `bot.py` - основная логика бота
- `handlers.py` - обработчики команд и сообщений
- `callback.py` - обработчики callback-запросов
- `models.py` - модели данных
- `config.py` - конфигурация приложения
- `text.py` - текстовые константы
- `requirements.txt` - зависимости Python

## Получение токена бота

1. Найдите [@BotFather](https://t.me/botfather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен в файл `.env`

## Лицензия

MIT License
