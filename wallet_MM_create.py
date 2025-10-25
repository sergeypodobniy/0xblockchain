"""
🔑 wallet_MM_create.py - Генератор множественных кошельков

Функциональность:
- 🔑 Генерация seed-фраз (12 или 24 слова) на английском языке
- 💼 Создание множественных кошельков из одной seed-фразы
- 📊 Экспорт в Excel с приватными ключами и адресами
- 🗂️ Автоматическое создание папки wallet/ с датой
- 🔄 Поддержка добавления данных в существующие файлы

Параметры генерации:
- input_words: количество seed-фраз для генерации
- input_length: 12 или 24 слова в seed-фразе
- input_key: количество кошельков на одну seed-фразу

Выходные данные:
- Excel файлы с колонками: wallet address, private keys, sid fraze
- Автоматическое именование: wallet_MM_YYYY-MM-DD_HH-MM-SS.xlsx
- Безопасное хранение в папке wallet/ (игнорируется Git)

⚠️ ВАЖНО: Файлы с приватными ключами НЕ должны попадать в Git!

Автор: sergeypodobniy
Дата: 2025
"""

from mnemonic import Mnemonic
from web3 import Web3
import pandas as pd
from eth_account import Account
import os
from datetime import datetime

def get_user_input(prompt, valid_values):
    while True:
        try:
            value = int(input(prompt))
            if value in valid_values:
                return value
            else:
                print(f"Пожалуйста, введите одно из следующих значений: {valid_values}")
        except ValueError:
            print("Пожалуйста, введите корректное число.")

input_words = get_user_input('Сколько сид фраз генерировать?\n', range(1, 1000))
input_length = get_user_input('Сколько слов использовать, 12 или 24?\n', [12, 24])
input_key = get_user_input('Сколько кошельков генерировать к одной сид фразе?\n', range(1, 1000))

w3 = Web3(Web3.HTTPProvider())

def gen_key(input_words, input_length, input_key):
    Account.enable_unaudited_hdwallet_features()
    data = []
    mnemo = Mnemonic("english")

    for m in range(input_words):
        words = mnemo.generate(strength=128 if input_length == 12 else 256)

        for i in range(input_key):
            acct = Account.from_mnemonic(
                words,
                account_path=f"m/44'/60'/0'/0/{i}"
            )
            addr = acct.address
            key = w3.to_hex(acct._private_key)
            data.append({'wallet address': addr, 'private keys': key, 'sid fraze': words})

    df = pd.DataFrame(data, columns=['wallet address', 'private keys', 'sid fraze'])

    # Создание папки 'wallet', если она не существует
    wallet_dir = os.path.join(os.getcwd(), 'wallet')
    if not os.path.exists(wallet_dir):
        os.makedirs(wallet_dir)

    # Генерация имени файла с датой создания
    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"wallet_MM_{current_date}.xlsx"
    file_path = os.path.join(wallet_dir, file_name)

    # Сохранение данных в файл
    if not os.path.isfile(file_path):
        df.to_excel(file_path, index=False)
    else:
        with pd.ExcelWriter(file_path, mode='a', engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False, header=False)

gen_key(input_words, input_length, input_key)
