import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

import exceptions


load_dotenv()


PRACTICUM_TOKEN = os.getenv("PRACTICUM_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


logging.basicConfig(
    level=logging.DEBUG,
    format=(
        "%(asctime)s, %(levelname)s, %(message)s"
    ),
    handlers=[logging.FileHandler("log.txt", encoding="UTF-8"),
              logging.StreamHandler(sys.stdout)])


def check_tokens():
    """Проверяет доступность переменных окружения."""
    tokens = [PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]
    return all(tokens)


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception as error:
        logging.error(f"Не удалось отправить сообщение - {error}")
        raise exceptions.MessageSendingError(
            f"Сообщение не отправлено - {error}"
        )
    else:
        logging.debug(f"Бот отправил сообщение: {message}")


def get_api_answer(timestamp):
    """Делает запрос к единственному эндпоинту API-сервиса."""
    params = {"from_date": timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS,
                                params=params)
        if response.status_code != HTTPStatus.OK:
            logging.error("Ответ от API не получен.")
            raise exceptions.ApiConnectError(
                "Ответ от API не получен."
            )
        logging.info(
            "Ответ от API получен."
        )
    except Exception as error:
        logging.error(f"Неверный код ответа: {error}")
        raise exceptions.ApiConnectError(
            f"При обращени к API возникла ошибка: {error}")
    return response.json()


def check_response(response):
    """
    Проверяет ответ API на соответствие документации.
    из урока API сервиса Практикум.Домашка.
    """
    if not isinstance(response, dict):
        raise TypeError("Неверный тип данных.")
    if "homeworks" not in response:
        raise KeyError("Такого ключа homeworks не существует.")
    if "current_date" not in response:
        raise KeyError("Такого ключа current_date не существует.")
    if not isinstance(response["homeworks"], list):
        raise TypeError("Неверный тип данных.")
    return response["homeworks"]


def parse_status(homework):
    """
    Извлекает из информации.
    о конкретной домашней работе статус этой работы.
    """
    if "status" not in homework:
        raise KeyError("Ключ status не найден.")
    if "homework_name" not in homework:
        raise KeyError("Ключ homework_name не найдет.")
    homework_status = homework["status"]
    if homework_status not in HOMEWORK_VERDICTS:
        raise ValueError("Нет такого статуса.")
    verdict = HOMEWORK_VERDICTS[homework["status"]]
    homework_name = homework["homework_name"]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        logging.critical("Ошибка переменных окружения.")
        sys.exit("Бот недоступен.")
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    error_message = ""
    last_status_message = ""

    while True:
        try:
            response = get_api_answer(timestamp)
            homework = check_response(response)
            if homework:
                status_message = parse_status(homework[0])
            else:
                status_message = ("Бот успешно запущен.")
            if status_message != last_status_message:
                send_message(bot, status_message)
                last_status_message = status_message
            else:
                logging.debug("Новые статусы отсутствуют.")
                timestamp = response.get("current_date")
        except exceptions.NotTelegramSending as error:
            message = f"Сбой в работе программы: {error}"
            logging.error(message)
        except Exception as error:
            error_message = f"Сбой в работе программы: {error}"
            logging.error(error_message)
            if error_message != last_status_message:
                send_message(bot, error_message)
                last_status_message = error_message
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
