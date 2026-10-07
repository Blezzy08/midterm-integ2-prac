import unittest

from flask import g

from app import create_app
from app.security import hash_password, require_role, verify_password


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

    def test_password_helpers_reject_invalid_inputs(self):
        password_hash = hash_password("valid password")

        with self.assertRaises(ValueError):
            hash_password("")
        with self.assertRaises(TypeError):
            hash_password(None)
        with self.assertRaises(ValueError):
            verify_password("", password_hash)
        with self.assertRaises(ValueError):
            verify_password("valid password", "")
        with self.assertRaises(TypeError):
            verify_password("valid password", None)


class RoleBasedAccessControlTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()

    def test_admin_role_can_access_admin_resource(self):
        @require_role("admin")
        def admin_resource():
            return {"status": "ok"}, 200

        with self.app.test_request_context():
            g.user_role = "admin"
            self.assertEqual(admin_resource(), ({"status": "ok"}, 200))

    def test_user_role_cannot_access_admin_resource(self):
        @require_role("admin")
        def admin_resource():
            return {"status": "ok"}, 200

        with self.app.test_request_context():
            g.user_role = "user"
            response, status = admin_resource()
            self.assertEqual(status, 403)
            self.assertEqual(response.get_json(), {"error": "Insufficient permissions"})

    def test_missing_role_is_unauthenticated(self):
        @require_role("user")
        def user_resource():
            return {"status": "ok"}, 200

        with self.app.test_request_context():
            response, status = user_resource()
            self.assertEqual(status, 401)
            self.assertEqual(response.get_json(), {"error": "Authentication required"})

    def test_admin_can_access_user_resource(self):
        @require_role("user")
        def user_resource():
            return {"status": "ok"}, 200

        with self.app.test_request_context():
            g.user_role = "admin"
            self.assertEqual(user_resource(), ({"status": "ok"}, 200))


if __name__ == "__main__":
    unittest.main()
