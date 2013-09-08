from base64 import b64encode
import requests
import json
import unittest

from taarifa_backend import app, db
from taarifa_backend.models import User
from taarifa_backend.api import user_datastore


class TaarifaTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.data = {"email": "taarifa_test@example.com",
                     "password": "password"}
        user_datastore.create_user(email="username", password="password")

    def tearDown(self):
        db.connection.drop_database(app.config['MONGODB_SETTINGS']['db'])

    def _create_admin(self, data, expected_response_code, expected_increment,
                      auth=("username", "password")):
        user_count = User.objects().count()
        headers = {"content-type": "application/json"}
        if auth:
            headers["Authorization"] = "Basic " + b64encode(':'.join(auth))
        r = self.app.post("/admin", data=json.dumps(data), headers=headers)
        self.assertEquals(expected_response_code, r.status_code)
        self.assertEquals(user_count + expected_increment,
                          User.objects().count())
        return r

    def test_create_admin(self):
        self._create_admin(self.data, requests.codes.ok, 1)

    def test_create_admin_missing_fields(self):
        data = [("password", "email", "taarifa_test@example.com"),
                ("email", "password", "password")]

        for missing, k, v in data:
            r = self._create_admin({k: v},
                                   requests.codes.unprocessable_entity, 0)
            self.assertEquals([missing], eval(r.data)["Missing"])

    def test_create_admin_auth(self):
        for auth in [None, ("foo", "bar")]:
            self._create_admin(self.data, requests.codes.unauthorized, 0,
                               auth=auth)
