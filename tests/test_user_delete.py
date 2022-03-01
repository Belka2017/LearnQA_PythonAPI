from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserDelete(BaseCase):
    def test_delete_user_id_2(self):
        data_login = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response_login = MyRequests.post("/user/login", data=data_login)
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        response_delete = MyRequests.delete(
            "/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_code_status(response_delete, 400)
        Assertions.assert_text_error(response_delete, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")

    def test_delete_user(self):
        data_register = self.prepare_registration_data()
        response_register = MyRequests.post("/user/", data=data_register)
        user_id = response_register.json()["id"]
        email = data_register['email']
        password = data_register['password']

        data_login = {
            'email': email,
            'password': password
        }
        response_login = MyRequests.post("/user/login", data=data_login)
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        response_delete = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_code_status(response_delete, 200)

        response_get = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response_get, 404)
        Assertions.assert_text_error(response_get, "User not found")

    def test_delete_other_user(self):
        data_register_user_1 = self.prepare_registration_data()
        response_register_user_1 = MyRequests.post("/user/", data=data_register_user_1)
        user_id_1 = response_register_user_1.json()["id"]

        Assertions.assert_code_status(response_register_user_1, 200)

        data_register_user_2 = self.prepare_registration_data()
        response_register_user_2 = MyRequests.post("/user/", data=data_register_user_2)
        email_user_2 = data_register_user_2['email']
        password_user_2 = data_register_user_2['password']

        Assertions.assert_code_status(response_register_user_2, 200)

        login_data_user_2 = {
            'email': email_user_2,
            'password': password_user_2
        }
        response_login_user_2 = MyRequests.post("/user/login", data=login_data_user_2)
        auth_sid_user_2 = self.get_cookie(response_login_user_2, "auth_sid")
        token_user_2 = self.get_header(response_login_user_2, "x-csrf-token")

        response_delete = MyRequests.delete(
            f"/user/{user_id_1}",
            headers={"x-csrf-token": token_user_2},
            cookies={"auth_sid": auth_sid_user_2},
        )

        Assertions.assert_code_status(response_delete, 400)
