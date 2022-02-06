import unittest

from model.user_model import User


class MyTestCase(unittest.TestCase):
    def test_pydantic1(self):
        external_data = {
            'id': 1,
            'name': 'raphael',
            'email': 'raphael@gogo33.com'
        }
        user1 = User(**external_data)
        self.assertEqual(user1.id, 1)  # add assertion here

    def test_pydantic2(self):
        external_data = {
            'name': 'raphael',
            'email': 'raphael@gogo33.com'
        }
        user1 = User(**external_data)
        self.assertEqual(user1.id, 1)

    def test_pydantic3(self):
        external_data = {
            'id': 1,
            'name': 'raphael',
            'signup_ts': 'broken'
        }
        user1 = User(**external_data)
        self.assertEqual(user1.id, 1)


if __name__ == '__main__':
    unittest.main()
