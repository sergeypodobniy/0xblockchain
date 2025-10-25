"""
🎛️ w3_info_get_bot.py - Интерактивный Telegram-бот для мониторинга криптовалют

Функциональность:
- 🎛️ Интерактивное меню с кнопками
- 💰 Получение курса любой криптовалюты по символу (BTC, ETH, SOL, BNB и др.)
- 📊 Те же данные, что и в автоматическом боте
- 🔄 Обработка callback-запросов и текстовых сообщений
- 🎯 Команды: /start, кнопки, ввод криптовалюты

Особенности:
- Использует python-telegram-bot библиотеку
- Поддерживает conversation handler для диалогов
- Обрабатывает inline-кнопки и текстовые сообщения
- Безопасная загрузка API ключей из переменных окружения

Автор: sergeypodobniy
Дата: 2025
"""

import requests
import time
from datetime import datetime, timedelta
import pytz
import os
from requests.exceptions import RequestException
from termcolor import colored
from decimal import Decimal
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler


# Загрузка переменных окружения из файла .env
load_dotenv()
# Токен вашего бота
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# Ваш API-ключ от CoinMarketCap
COINMARKETCAP_API_KEY = os.getenv('COINMARKETCAP_API_KEY')
# Ваш API-ключ от Etherscan
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')

print('-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x')
# Функция для проверки доступности Telegram бота
def check_telegram_bot_token(token):
    url = f'https://api.telegram.org/bot{token}/getMe'
    response = requests.get(url)
    if response.status_code == 200:
        print(f"TELEGRAM_BOT_TOKEN {colored('доступен', 'green')}.")
        return True
    else:
        print(f"TELEGRAM_BOT_TOKEN {colored('недоступен', 'red')}. Ошибка: {response.text}")
        return False

# Функция для проверки доступности CoinMarketCap API ключа
def check_coinmarketcap_api_key(api_key):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(f"COINMARKETCAP_API_KEY {colored('доступен', 'green')}.")
        return True
    else:
        print(f"COINMARKETCAP_API_KEY {colored('недоступен', 'red')}. Ошибка: {response.text}")
        return False

def check_etherscan_api_key(api_key):
    # Проверяем наличие ключа
    if not api_key:
        raise ValueError("ETHERSCAN_API_KEY не установлен")

    # Базовый URL для проверки
    base_url = "https://api.etherscan.io/api"

    try:
        # Делаем тестовый запрос для проверки валидности ключа
        response = requests.get(
            f"{base_url}?module=account&action=balance&address=0x0&tag=latest&apikey={api_key}",
            timeout=10
        )

        # Проверяем статус ответа
        if response.status_code == 200:
            data = response.json()
            # Проверяем наличие ошибки в ответе
            if data.get('status') == '1':
                print(f"ETHERSCAN_API_KEY {colored('доступен', 'green')}.")
                return True
            else:
                raise ValueError(f"Ошибка Etherscan API: {data.get('message')}")
        else:
            raise RequestException(f"Ошибка запроса: {response.status_code}")

    except RequestException as e:
        print(f"Не удалось проверить API ключ: {str(e)}")
        return False

    return False

print('-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x')

# Функция для получения цен Биткоина и Эфира
def get_crypto_prices(api_key):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }
    params = {
        'symbol': 'BTC,ETH'
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    btc_price = round(data['data']['BTC']['quote']['USD']['price'])
    eth_price = round(data['data']['ETH']['quote']['USD']['price'])
    return btc_price, eth_price

# Функция для получения стоимости газа (gwei) для Ethereum
def get_eth_gas_price(api_key):
    url = f'https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяем статус ответа

        data = response.json()
        if 'result' in data:
            gas_price = data['result']['ProposeGasPrice']
            # Преобразуем в Decimal для корректного округления
            decimal_price = Decimal(gas_price)
            rounded_price = round(decimal_price, 2)
            return rounded_price

        raise ValueError("Некорректный формат данных в ответе")

    except requests.exceptions.RequestException as e:
        print(colored(f"Ошибка запроса: {str(e)}", "red"))
    except ValueError as e:
        print(colored(f"Ошибка обработки данных: {str(e)}", "red"))
    except Exception as e:
        print(colored(f"Произошла непредвиденная ошибка: {str(e)}", "red"))

    return None

# Функция для получения индекса страха и жадности через Alternative.me
def get_fear_and_greed_index():
    url = 'https://api.alternative.me/fng/?limit=1'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяем статус ответа

        data = response.json()
        if 'data' in data:
            fear_and_greed_index = data['data'][0]['value']
            fear_and_greed_category = data['data'][0]['value_classification']
            return {
                'index': fear_and_greed_index,
                'category': fear_and_greed_category
            }

        raise ValueError("Некорректный формат данных в ответе")

    except requests.exceptions.RequestException as e:
        print(colored(f"Ошибка запроса: {str(e)}", "red"))
    except ValueError as e:
        print(colored(f"Ошибка обработки данных: {str(e)}", "red"))
    except Exception as e:
        print(colored(f"Произошла непредвиденная ошибка: {str(e)}", "red"))

    return None

# Функция для получения доминирования Bitcoin
def get_btc_dominance(api_key):
    url = 'https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверяем статус ответа

        data = response.json()

        # Проверяем наличие необходимых данных
        if 'data' in data:
            btc_dominance = data['data'].get('btc_dominance')

            # Округляем значения до 2 знаков после запятой
            if btc_dominance is not None:
                btc_dominance = round(Decimal(btc_dominance), 2)

            # Если показатель отсутствует, возвращаем None
            if btc_dominance is None:
                print(colored("BTC доминирование не найдено в ответе", "yellow"))

            return btc_dominance

        raise ValueError("Некорректный формат данных в ответе")

    except RequestException as e:
        print(f"Ошибка запроса: {str(e)}")
    except ValueError as e:
        print(f"Ошибка обработки данных: {str(e)}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {str(e)}")

    return None

print('-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x')

# Функция для отправки сообщения в Telegram
def send_message(context, chat_id, text):
    context.bot.send_message(chat_id=chat_id, text=text)

# Функция для обработки команды /get
def handle_get_command(update, context):
    chat_id = update.callback_query.message.chat.id if update.callback_query else update.message.chat.id

    btc_price, eth_price = get_crypto_prices(COINMARKETCAP_API_KEY)
    gas_price = get_eth_gas_price(ETHERSCAN_API_KEY)
    fear_and_greed_index = get_fear_and_greed_index()
    btc_dominance = get_btc_dominance(COINMARKETCAP_API_KEY)

    if fear_and_greed_index:
        fear_and_greed_value = fear_and_greed_index['index']
        fear_and_greed_category = fear_and_greed_index['category']
        fear_and_greed_info = f"Индекс страха и жадности: {fear_and_greed_value} ({fear_and_greed_category})"
    else:
        fear_and_greed_info = "Индекс страха и жадности недоступен."

    message = (f'Курс BTC: ${btc_price}\n'
               f'Курс ETH: ${eth_price}\n'
               f'Стоимость газа (gwei ETH): {gas_price}\n'
               f'{fear_and_greed_info}\n'
               f'Доминирование Биткоина: {btc_dominance}%')

    send_message(context, chat_id, message)

# Функция для обработки нажатия на кнопку
def button(update, context):
    query = update.callback_query
    query.answer()
    handle_get_command(update, context)

# Функция для обработки команды /start
def start(update, context):
    keyboard = [
        [InlineKeyboardButton("Получить информацию", callback_data='get_info')],
        [InlineKeyboardButton("Ввод криптовалюты", callback_data='input_crypto')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите действие:', reply_markup=reply_markup)

# Функция для обработки ввода криптовалюты
def input_crypto(update, context):
    context.bot.send_message(chat_id=update.callback_query.message.chat.id, text="Введите название криптовалюты (например BTC, ETH, SOL, BNB):")
    return "WAITING_CRYPTO"

# Функция для получения курса криптовалюты
def get_crypto_price(update, context):
    crypto_name = update.message.text.upper().strip()
    try:
        url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={crypto_name}'
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        if crypto_name in data['data']:
            price = round(data['data'][crypto_name]['quote']['USD']['price'], 4)
            message = f"Текущий курс {crypto_name}: ${price}"
        else:
            message = f"Криптовалюта {crypto_name} не найдена."
    except Exception as e:
        message = f"Произошла ошибка при получении курса криптовалюты: {str(e)}"

    send_message(context, update.message.chat.id, message)

print('-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x')

# Основная функция для запуска бота
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button, pattern='get_info'))
    dp.add_handler(CallbackQueryHandler(start, pattern='start'))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, get_crypto_price))

    updater.start_polling(timeout=30)
    updater.idle()

if __name__ == "__main__":
    main()