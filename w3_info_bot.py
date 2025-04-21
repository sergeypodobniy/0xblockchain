import requests
import schedule
import time
from datetime import datetime, timedelta
import pytz
import os
from requests.exceptions import RequestException
from termcolor import colored
from decimal import Decimal
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Токен вашего бота
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# Список ID ваших каналов или чатов
CHAT_IDS_STR = os.getenv('CHAT_IDS')
if CHAT_IDS_STR:
    CHAT_IDS = [chat_id.strip() for chat_id in CHAT_IDS_STR.split(',') if chat_id.strip()]
else:
    CHAT_IDS = []
# Ваш API-ключ от CoinMarketCap
COINMARKETCAP_API_KEY = os.getenv('COINMARKETCAP_API_KEY')
# Ваш API-ключ от Etherscan
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')

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

# Функция для проверки доступности канала или группы
def check_chat_availability(token, chat_id):
    url = f'https://api.telegram.org/bot{token}/getChat'
    payload = {
        'chat_id': chat_id
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print(f"Чат или канал с ID {chat_id} {colored('доступен', 'green')}.")
        return True
    else:
        print(f"Чат или канал с ID {chat_id} {colored('недоступен', 'red')}. Ошибка: {response.text}")
        return False

#----------------------------------#----------------------------------#----------------------------------#----------------------------------#----------------------------------

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

# Функция для отправки сообщения в Telegram
def send_message(token, chat_id, text):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"Ошибка при отправке сообщения в чат {chat_id}: {response.text}")

#----------------------------------#----------------------------------#----------------------------------#----------------------------------#----------------------------------

# Основная функция для отправки сообщений
def job():
    if not check_telegram_bot_token(TELEGRAM_BOT_TOKEN):
        return

    if not check_coinmarketcap_api_key(COINMARKETCAP_API_KEY):
        return

    if not check_etherscan_api_key(ETHERSCAN_API_KEY):
        return

    available_chats = []
    for chat_id in CHAT_IDS:
        if check_chat_availability(TELEGRAM_BOT_TOKEN, chat_id):
            available_chats.append(chat_id)
        else:
            print(f"Чат с ID {chat_id} недоступен. Пропускаем.")

    if not available_chats:
        print("Нет доступных чатов для отправки сообщений.")
        return

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

    message = (f'Цена Биткоина: ${btc_price}\n'
               f'Цена Эфира: ${eth_price}\n'
               f'Стоимость газа (gwei): {gas_price}\n'
               f'{fear_and_greed_info}\n'
               f'Доминирование Биткоина: {btc_dominance}%')

    for chat_id in available_chats:
        send_message(TELEGRAM_BOT_TOKEN, chat_id, message)

# Планировщик для выполнения задачи в 12:00 по московскому времени
def schedule_job():
    # Устанавливаем часовой пояс Москвы
    moscow_tz = pytz.timezone('Europe/Moscow')
    # Устанавливаем время выполнения задачи
    target_time = moscow_tz.localize(datetime.now()).replace(hour=12, minute=0, second=0, microsecond=0)
    # Если текущее время больше целевого, планируем на следующий день
    if datetime.now(moscow_tz) > target_time:
        target_time += timedelta(days=1)
    # Вычисляем задержку до целевого времени
    delay = (target_time - datetime.now(moscow_tz)).total_seconds()
    # Планируем задачу
    schedule.every(delay).seconds.do(job)
    # Планируем задачу на следующий день после выполнения текущей
    schedule.every().day.at("12:00").do(job)

# Настройка планировщика
schedule_job()

# Бесконечный цикл для выполнения задач
while True:
    schedule.run_pending()
    time.sleep(1)
