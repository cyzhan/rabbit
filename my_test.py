import base64
import hashlib
import hmac
import json
import unittest
from urllib.parse import quote
from model.order_model import OrderList
from util import encrypt
import redis


class MyTestCase(unittest.TestCase):
    def test_md5(self):
        result = "2a5e99038b039317fc5eecda5afb5acf"
        salt = "fepwhgZeiTVpeugDkYc63T"
        raw_password = "1234qwer"
        encrypt_pwd = encrypt.md5(raw_password + ':' + salt)
        print('raw password = {}'.format(raw_password))
        print('hashed password = {}'.format(encrypt_pwd))
        self.assertEqual(result, encrypt_pwd)

    def test_jwt(self):
        salt2 = 'fkpora039jgadjfjlsir'
        header = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
        payload = 'eyJpZCI6NSwibmFtZSI6InJ1Ynk2NjYiLCJlbWFpbCI6InJ1YnlAZ29kYW1uLmNvbSIsImV4cCI6MTY0NDkwODg2NH0'
        string = "{}.{}".format(header, payload)
        raw = hmac.new(bytes(salt2, encoding="utf-8"), bytes(string, encoding="utf-8"),
                       digestmod=hashlib.sha256).digest()
        signature = str(base64.b64encode(raw), 'utf-8')
        # signature = str(base64.urlsafe_b64encode(raw), 'utf-8')
        print("signature1 = " + signature)
        print("signature2 = " + quote(signature))

    def test_my_redis(self):
        r = redis.Redis(host='inno.odds-machine.com', port=6379, db=0)
        r.set('abc', '123')
        v = r.get('abc')
        print('v = {}'.format(v))

    def test_validator(self):
        json_str = '''
        [{"productId": 1, "quantity": 5}, {"productId": 2, "quantity": 3}]
        '''
        # val = [{'productId': 1, 'quantity': 5}, {'productId': 2, 'quantity': 3}]
        val = json.loads(json_str)
        model = OrderList(items=val)
        print(model.dict())
        # print(model.items)


if __name__ == '__main__':
    unittest.main()
