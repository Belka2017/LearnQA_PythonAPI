import requests
import time

resp1 = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job')
obj = resp1.json()
token = {'token': obj['token']}
t = obj['seconds']

resp2 = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job', params=token)
obj2 = resp2.json()
status = obj2['status']
if status == 'Job is NOT ready':
    print(f'Status before {t} sec: {status}')
else:
    print(f'Incorrect status for task before {t} sec')

time.sleep(t)
resp3 = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job', params=token)
obj3 = resp3.json()
status = obj3['status']
if status == 'Job is ready':
    print(f"Status after {t} sec : {status}")
else:
    print(f'Incorrect status for task after {t} sec')
print(f"Result: {obj3['result']}")
