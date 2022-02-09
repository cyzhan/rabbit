import unittest

from model.user_model import User
from util import encrypt


class MyTestCase(unittest.TestCase):
    def test_md5(self):
        result = "2a5e99038b039317fc5eecda5afb5acf"
        salt = "fepwhgZeiTVpeugDkYc63T"
        raw_password = "1234qwer"
        encrypt_pwd = encrypt.md5(raw_password + ':' + salt)
        print('raw password = {}'.format(raw_password))
        print('hashed password = {}'.format(encrypt_pwd))
        self.assertEqual(result, encrypt_pwd)


if __name__ == '__main__':
    unittest.main()
