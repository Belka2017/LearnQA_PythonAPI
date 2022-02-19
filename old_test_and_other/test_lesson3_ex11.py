import requests

class TestCookie:
    def test_cookie_examination(self):
        responce = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        cookie_actual = responce.cookies.get("HomeWork")
        cookie_expected = 'hw_value'
        assert "HomeWork" in responce.cookies, "Сookie does not contain a parameter 'HomeWork'"
        assert cookie_actual == cookie_expected, "Parameter value in cookies is incorrect"
