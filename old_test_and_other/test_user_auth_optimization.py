import pytest
import requests


class TestUserAuth:
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        responce1 = requests.post('https://playground.learnqa.ru/api/user/login', data=data)

        assert "auth_sid" in responce1.cookies, "There is no auth cookie in the responce"
        assert "x-csrf-token" in responce1.headers, "There is no CSRF token header in the responce"
        assert "user_id" in responce1.json(), "There is no user id in the responce"

        self.auth_sid = responce1.cookies.get("auth_sid")
        self.token = responce1.headers.get("x-csrf-token")
        self.user_id_from_auth_metod = responce1.json()["user_id"]

    def test_auth_user(self):
        responce2 = requests.get(
            'https://playground.learnqa.ru/api/user/auth',
            headers={'x-csrf-token': self.token},
            cookies={'auth_sid': self.auth_sid}
        )

        assert "user_id" in responce2.json(), "There is no user id in the second response"
        user_id_from_check_metod = responce2.json()["user_id"]
        print(user_id_from_check_metod)
        assert self.user_id_from_auth_metod == user_id_from_check_metod, "User id from auth method is not equal to user id from check method"

    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        if condition == 'no_cookie':
            responce2 = requests.get(
                'https://playground.learnqa.ru/api/user/auth',
                headers={'x-csrf-token': self.token}
            )
        else:
            responce2 = requests.get(
                'https://playground.learnqa.ru/api/user/auth',
                cookies={'uth_sid': self.auth_sid}
            )

        assert "user_id" in responce2.json(), "There is no user id in second responce"
        user_id_frome_check_metod = responce2.json()["user_id"]
        assert user_id_frome_check_metod == 0, f"User is athorized with condition {condition}"