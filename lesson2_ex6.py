import requests

responce = requests.get("https://playground.learnqa.ru/api/long_redirect")
print(f'Итоговый URL: {responce.url}')
print(f'Количество редиректов: {len(responce.history)}')

