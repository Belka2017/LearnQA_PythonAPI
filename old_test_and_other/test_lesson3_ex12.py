import requests
import json

class TestHeaders:
    def test_header(self):
        responce = requests.get(" https://playground.learnqa.ru/api/homework_header")
        header_actual = responce.headers.get("x-secret-homework-header")
        header_expected = 'Some secret value'

        assert "x-secret-homework-header" in responce.headers, "Header does not contain a parameter 'x-secret-homework-header'"
        assert header_actual == header_expected, "Parameter 'x-secret-homework-header' value in cookies is incorrect"

