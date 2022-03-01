from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    def test_edit_user_without_auth(self):
        # REGISTER NEW USER
        data = self.prepare_registration_data()
        response_register = MyRequests.post("/user/", data=data)
        user_id = response_register.json()["id"]

        # EDIT
        new_username = "NewUsername"
        responce_edit = MyRequests.put(
            f"/user/{user_id}",
            data={"username": new_username}
        )

        Assertions.assert_code_status(responce_edit, 400)
        Assertions.assert_text_error(responce_edit, "Auth token not supplied")

    def test_edit_email_without_ad(self):
        # REGISTER NEW USER
        data = self.prepare_registration_data()
        response_register = MyRequests.post("/user/", data=data)
        user_id = response_register.json()["id"]
        email = data['email']
        password = data['password']

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response_login = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # EDIT
        new_mail = 'testexample.com'
        response = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_mail}
        )

        Assertions.assert_code_status(response, 400)
        Assertions.assert_text_error(response, "Invalid email format")

    def test_edit_other_user(self):
        # REGISTER USER_1
        data_register_user_1 = self.prepare_registration_data()
        response_register_user_1 = MyRequests.post("/user/", data=data_register_user_1)
        user_id_1 = response_register_user_1.json()["id"]

        Assertions.assert_code_status(response_register_user_1, 200)

        # REGISTER USER_2
        data_register_user_2 = self.prepare_registration_data()
        response_register_user_2 = MyRequests.post("/user/", data=data_register_user_2)
        email_user_2 = data_register_user_2["email"]
        password_user_2 = data_register_user_2["password"]

        Assertions.assert_code_status(response_register_user_2, 200)

        # LOGIN USER_2
        login_data_user_2 = {
            'email': email_user_2,
            'password': password_user_2
        }
        response_login_user_2 = MyRequests.post("/user/login", data=login_data_user_2)

        auth_sid_user_2 = self.get_cookie(response_login_user_2, "auth_sid")
        token_user_2 = self.get_header(response_login_user_2, "x-csrf-token")

        # EDIT USER_1 WITH AUTH USER_2
        new_firstname = "Update"

        response = MyRequests.put(
            f"/user/{user_id_1}",
            headers={"x-csrf-token": token_user_2},
            cookies={"auth_sid": auth_sid_user_2},
            data={"firsName": new_firstname}
        )

        Assertions.assert_code_status(response, 400)
        Assertions.assert_text_error(response, "No data to update")

    def test_edit_firstname_is_short(self):
        # REGISTER NEW USER
        data = self.prepare_registration_data()
        response_register = MyRequests.post("/user/", data=data)
        user_id = response_register.json()["id"]
        email = data['email']
        password = data['password']

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response_login = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # EDIT
        new_firstname = 't'
        response = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_firstname}
        )

        Assertions.assert_code_status(response, 400)
        assert response.json()["error"] == "Too short value for field firstName"