import requests

responce = requests.get("https://playground.learnqa.ru/api/hello")
print(responce.text)
