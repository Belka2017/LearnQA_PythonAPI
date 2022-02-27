import requests
import json

class Test:
    def test_user_agent1(self):
        resp = requests.get("https://playground.learnqa.ru/ajax/api/user_agent_check",
                        headers={
                            "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}
                        )
        print(f'Device = {resp.json()["device"]}')
        print(f'Browser = {resp.json()["browser"]}')
        print(f'Platform = {resp.json()["platform"]}')
        #print(resp.json())