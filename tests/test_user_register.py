import pytest

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from datetime import datetime
import allure


@allure.epic("Registration cases")
class TestUserRegister(BaseCase):
    @allure.description("This test successfully create user")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.description("User with such an email already exists")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email=email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    @allure.description("Unsuccessful registration: incorrect email")
    def test_create_user_incorrect_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email=email)
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", \
            f"Unexpected response content {response.content}"

    @pytest.mark.parametrize(
        argnames=["username", "content_text"],
        argvalues=(
            [
                "T",
                "The value of 'username' field is too short"
            ],
            [
                "Sumvituperatadefinitionestevisvisaliafallidomingeasumvituperatadefinitionestevisvisaliafallidomingeasumvituperatadefinitionestevisvisaliafallidomingeasumvituperatadefinitionestevisvisaliafallidomingeasumvituperatadefinitionestevisvisaliafallidomingeaqa",
                "The value of 'username' field is too long"
            ]
        ),
        ids=["Short username", "Long username"]
    )
    @allure.description("Unsuccessful registration: incorrect username")
    def test_incorrect_name(self, username, content_text):
        data = self.prepare_registration_data(username=username)
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        print(f"Error- {response.text}")
        assert response.content.decode("utf-8") == content_text, f"Unexpected response content {response.content}"

    @pytest.mark.parametrize(
        argnames=["data", "content_text"],
        argvalues=(
            [
                {
                    'password': '123',
                    'username': 'Test',
                    'firstName': 'learnqa',
                    'lastName': 'learnqa'
                },
                "The following required params are missed: email"
            ],
            [
                {
                    'username': 'Test',
                    'firstName': 'learnqa',
                    'lastName': 'learnqa',
                    'email': f'test{datetime.now().strftime("%m%d%Y%H%M%S")}@example.com'
                },
                "The following required params are missed: password"
            ],
            [
                {
                    'password': '123',
                    'firstName': 'learnqa',
                    'lastName': 'learnqa',
                    'email': f'test{datetime.now().strftime("%m%d%Y%H%M%S")}@example.com'
                },
                "The following required params are missed: username"
            ],
            [
                {
                    'password': '123',
                    'username': 'Test',
                    'lastName': 'learnqa',
                    'email': f'test{datetime.now().strftime("%m%d%Y%H%M%S")}@example.com'
                },
                "The following required params are missed: firstName"
            ],
            [
                {
                    'password': '123',
                    'username': 'Test',
                    'firstName': 'learnqa',
                    'email': f'test{datetime.now().strftime("%m%d%Y%H%M%S")}@example.com'
                },
                "The following required params are missed: lastName"
            ]
        ),
        ids=[
            "Without email",
            "Without password",
            "Without username",
            "Without firstName",
            "Without lastName"
        ]
    )
    @allure.description("Unsuccessful registration: without a required parameter")
    def test_check_required_param(self, data, content_text):
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == content_text, \
            f"Unexpected response content {response.content}"
