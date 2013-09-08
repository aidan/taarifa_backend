import requests
import json
import unittest

from taarifa_backend.models import clear_database, User
from taarifa_backend.api import user_datastore

BASE_URL = "http://localhost:5000"


class TaarifaTest(unittest.TestCase):

    def setUp(self):
        clear_database()
        user_datastore.create_user(email="username", password="password")

    def tearDown(self):
        pass

    def _create_admin(self, data, expected_response_code, expected_increment,
                      auth=("username", "password")):
        user_count = User.objects().count()
        headers = {"content-type": "application/json"}
        r = requests.post(BASE_URL + "/admin", data=json.dumps(data),
                          headers=headers, auth=auth)
        self.assertEquals(expected_response_code, r.status_code)
        self.assertEquals(user_count + expected_increment,
                          User.objects().count())
        return r

    def test_create_admin(self):
        data = {"email": "taafira_test@example.com",
                "password": "password"}
        self._create_admin(data, requests.codes.ok, 1)

    def test_create_admin_missing_fields(self):
        data = {"email": "taafira_test@example.com",
                "password": "password"}

        for expected_missing in data.keys():
            data_copy = data.copy()
            del data_copy[expected_missing]
            r = self._create_admin(data_copy,
                                   requests.codes.unprocessable_entity, 0)
            response_data = r.json()
            self.assertEquals([expected_missing], response_data["Missing"])

    def test_create_admin_auth(self):
        data = {"email": "taafira_test@example.com",
                "password": "password"}
        for auth in [None, ("foo", "bar")]:
            self._create_admin(data, requests.codes.unauthorized, 0,
                               auth=auth)
