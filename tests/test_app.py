import unittest
from uuid import uuid4

from fastapi import HTTPException

from src.app import activities, signup_for_activity, unregister_from_activity


class SignupCapacityTests(unittest.TestCase):
    def setUp(self):
        self.activity_name = f"Capacity test {uuid4()}"
        activities[self.activity_name] = {
            "max_participants": 1,
            "participants": ["existing@mergington.edu"],
        }

    def tearDown(self):
        del activities[self.activity_name]

    def test_rejects_signup_when_activity_is_full(self):
        with self.assertRaises(HTTPException) as error:
            signup_for_activity(self.activity_name, "new@mergington.edu")

        self.assertEqual(error.exception.status_code, 400)
        self.assertEqual(error.exception.detail, "Activity is full")

    def test_allows_signup_when_spot_is_available(self):
        activities[self.activity_name]["participants"].clear()

        result = signup_for_activity(self.activity_name, "new@mergington.edu")

        self.assertEqual(result["message"], f"Signed up new@mergington.edu for {self.activity_name}")
        self.assertEqual(
            activities[self.activity_name]["participants"],
            ["new@mergington.edu"],
        )

    def test_allows_signup_after_unregister_frees_capacity(self):
        with self.assertRaises(HTTPException):
            signup_for_activity(self.activity_name, "new@mergington.edu")

        unregister_from_activity(self.activity_name, "existing@mergington.edu")
        result = signup_for_activity(self.activity_name, "new@mergington.edu")

        self.assertEqual(result["message"], f"Signed up new@mergington.edu for {self.activity_name}")
        self.assertEqual(
            activities[self.activity_name]["participants"],
            ["new@mergington.edu"],
        )


if __name__ == "__main__":
    unittest.main()
