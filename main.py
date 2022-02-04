from json.decoder import JSONDecodeError
import requests

payload = {"name": "User"}
responce = requests.get("https://playground.learnqa.ru/api/hello")
print(responce.text)

try
    parsed_responce_txt = responce.json()
    print(parsed_responce_txt)
except JSONDecodeError:
    print("Response is not a JSON")