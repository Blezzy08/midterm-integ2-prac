import unittest

from app import create_app
from app.security import hash_password, verify_password


class HealthEndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_health_endpoint_returns_ok(self):
        response = self.client.get("/api/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})


class PasswordSecurityTestCase(unittest.TestCase):
    def test_password_hash_is_salted_and_verifiable(self):
        password = "correct horse battery staple"

        password_hash = hash_password(password)

        self.assertNotEqual(password_hash, password)
        self.assertTrue(verify_password(password, password_hash))
        self.assertFalse(verify_password("wrong password", password_hash))
        self.assertNotEqual(hash_password(password), password_hash)


if __name__ == "__main__":
    unittest.main()
