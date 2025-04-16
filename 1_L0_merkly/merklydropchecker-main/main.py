import os
from collections import defaultdict

# Путь к директории и файлу adresses.txt
current_directory = os.path.dirname(os.path.abspath(__file__))
addresses_file_path = os.path.join(current_directory, 'adresses.txt')

# Чтение адресов для сравнения и приведение их к нижнему регистру
with open(addresses_file_path, 'r') as file:
    addresses_to_compare = [line.strip().lower() for line in file.readlines()]

address_points = {}
points_count = defaultdict(int)

# Обработка файлов с суффиксом points.txt
for filename in os.listdir(current_directory):
    if filename.endswith('points.txt'):
        points = int(filename.split('points')[0])
        filepath = os.path.join(current_directory, filename)

        with open(filepath, 'r') as file:
            addresses = file.readlines()

            for address in addresses:
                address = address.strip().lower()
                if address in addresses_to_compare:
                    if address in address_points:
                        address_points[address] += points
                    else:
                        address_points[address] = points

# Подсчет количества кошельков для каждого количества поинтов
for points in address_points.values():
    points_count[points] += 1

# Запись результатов в файл result.txt
result_file_path = os.path.join(current_directory, 'result.txt')
with open(result_file_path, 'w') as file:
    for address, points in address_points.items():
        file.write(f'{address}: {points}\n')

    file.write('\nКоличество кошельков по количеству поинтов:\n')
    for points, count in sorted(points_count.items()):
        file.write(f'{points} points - {count} wallets\n')

print("Все адреса успешно обработаны и сохранены в result.txt")
