import requests
import time

resp1 = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job')
obj = resp1.json()
token = {'token': obj['token']}
t = obj['seconds']

resp2 = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job', params=token)
obj2 = resp2.json()
status = obj2['status']
print(f'Status before {t} sec: {status}')

time.sleep(t)
resp3 = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job', params=token)
obj3 = resp3.json()
print(f"Status after {t} sec : {obj3['status']}")
print(f"Result: {obj3['result']}")
