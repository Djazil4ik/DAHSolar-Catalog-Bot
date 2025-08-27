import telebot
import signal
import sys
import dotenv
import logging
from telebot import types


api_key = dotenv.dotenv_values('.env')['api_key']
bot = telebot.TeleBot(str(api_key))


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

web_app = types.WebAppInfo("https://dahsolar.uz/")

is_running = True


@bot.message_handler(commands=['start'])
def start(message):
    try:
        logger.info(
            f"Пользователь {message.from_user.id} - {message.from_user.username} запустил бота.")

        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(
            "Открыть каталог DAHSolar", web_app=web_app)
        markup.add(btn1)
        bot.send_message(
            message.chat.id, "Добро пожаловать в DAHSolar!", reply_markup=markup)

    except Exception as e:
        logger.error(f"Ошибка в обработчике /start: {e}")


def signal_handler(signum, frame):
    global is_running
    logging.info("Получен сигнал завершения. Завершение работы бота...")
    is_running = False
    try:
        bot.stop_polling()
    except:
        pass
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    logger.info('=' * 50)
    logger.info('Запуск бота...')
    logger.info('=' * 50)

    try:
        bot_info = bot.get_me()
        logger.info(
            f"Бот запущен как @{bot_info.username} (ID: {bot_info.id})")

        logger.info("Начало опроса...")
        bot.polling(none_stop=True, interval=2, timeout=20)

    except Exception as e:
        logger.critical(f"Критическая ошибка: {e}")

    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем(Ctrl+C).")

    except telebot.apihelper.ApiException as api_exc:  # type: ignore
        logger.critical(f"Ошибка API Telegram: {api_exc}")

    finally:
        logger.info('Бот остановлен.')
        logger.info('=' * 50)


if __name__ == "__main__":
    main()
