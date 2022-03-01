from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        print(response.content)
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post('/user/login', data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_metod = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(
            f"/user/{user_id_from_auth_metod}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    def test_get_userinfo_other_user(self):
        # REGISTER NEW USER_1
        data_1 = self.prepare_registration_data()
        response_register = MyRequests.post("/user/", data=data_1)
        user1_id = response_register.json()["id"]
        username_1 = data_1["username"]

        # LOGIN OLD USER_2
        data_2 = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response_login = MyRequests.post('/user/login', data=data_2)

        auth_sid_user2 = self.get_cookie(response_login, "auth_sid")
        token_user2 = self.get_header(response_login, "x-csrf-token")

        # GET INFO BY NEW USER_1 WITH LOGIN OLD USER_2
        response = MyRequests.get(
            f"/user/{user1_id}",
            headers={"x-csrf-token": token_user2},
            cookies={"auth_sid": auth_sid_user2}
        )

        Assertions.assert_json_value_by_name(response, "username", username_1, f"Incorrect value 'username' for user")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")
