import base64
import decimal
import hashlib
import hmac
import json
import logging
import os
import time
import unittest
from urllib.parse import quote
import requests
from dotenv import load_dotenv
import exception
from model.order_model import OrderList
from util import encrypt
import redis
from util.aiodb_util import db

cache = {'login_user': {
    "id": 0,
    "name": "caravaggio",
    "password": "caravaggio1234",
    "token": ""
}}

BASE_URL = 'http://localhost:8005/rabbit'


def log(msg: str):
    print('{} | {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), msg))


def print_pretty_json(json_str: str):
    print(json.dumps(json.loads(json_str), indent=2, sort_keys=False))


def get_auth_headers():
    return {'Authorization': cache['login_user']['token']}


async def init_aiodb(evloop):
    await db.create_pool(evloop)


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        log('Test Start')
        r = requests.get('http://localhost:8005/rabbit/system/version')
        response: dict = r.json()
        log('version={}'.format(response["version"]))

        data = {'name': cache['login_user']['name'], 'password': cache['login_user']['password']}
        r = requests.post(url='http://localhost:8005/rabbit/users/login', data=json.dumps(data))
        if r.status_code is not requests.codes.ok:
            log('login error, status code={}'.format(r.status_code.numerator))
            print_pretty_json(r.text)
            raise Exception('login error, status code={}'.format(r.status_code.numerator))
        response: dict = r.json()
        print_pretty_json(r.text)
        cache['login_user']['id'] = response['data']['id']
        cache['login_user']['token'] = response['data']['token']
        log('-----------------------------------------------')
        # print(cache)

    def test_md5(self):
        """
        check md5 outcome is as expect
        """
        result = "2a5e99038b039317fc5eecda5afb5acf"
        salt = os.getenv('SALT1')
        raw_password = "1234qwer"
        encrypt_pwd = encrypt.md5(raw_password + ':' + salt)
        logging.info('hello')
        log('raw password = {}'.format(raw_password))
        log('hashed password = {}'.format(encrypt_pwd))
        self.assertEqual(result, encrypt_pwd)

    def test_jwt(self):
        salt2 = os.getenv('SALT2')
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

    def test_login(self):
        r = requests.get('http://localhost:8005/rabbit/system/version')
        response: dict = r.json()
        print(f'version={response["version"]}')

        data = {'name': cache['login_user']['name'], 'password': cache['login_user']['password']}
        r = requests.post(url='http://localhost:8005/rabbit/users/login', data=json.dumps(data))
        response: dict = r.json()
        print_pretty_json(r.text)
        cache['login_user']['id'] = response['data']['id']
        cache['login_user']['token'] = response['data']['token']
        print(cache)

    def test_get_users_list(self):
        params = {'pageIndex': 1, 'pageSize': 10}
        # params['user_id'] = [1, 3, 5]
        r = requests.get(url=BASE_URL + '/users', params=params, headers=get_auth_headers)
        print_pretty_json(r.text)
        json_content = r.json()
        self.assertEqual(0, json_content['code'])

    def test_401_check(self):
        params = {'pageIndex': 1, 'pageSize': 10}
        headers = {'Authorization': cache['login_user']['token'] + 'extra_string_to_make_it_fail'}
        r = requests.get(url='http://localhost:8005/rabbit/users', params=params, headers=headers)
        print_pretty_json(r.text)
        json_content = r.json()
        self.assertEqual(401, json_content['code'])

    def test_get_products(self):
        params = {'pageIndex': 1, 'pageSize': 50}
        # params['id'] = [2, 7]
        r = requests.get(url=BASE_URL + '/products', params=params, headers=get_auth_headers())
        print_pretty_json(r.text)
        json_content = r.json()
        self.assertEqual(0, json_content['code'])

    def test_purchase_product(self):
        from service.product_sv import product_service
        from model.page_model import Page
        from random import randrange
        import asyncio

        loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(init_aiodb(evloop=loop))
        products: list = loop.run_until_complete(product_service.get_products(page=Page(index=1, size=50), ids=[]))['data']
        product_count = len(products)
        random_numbers = set()
        for i in range(5):
            if len(random_numbers) > 2:
                break
            random_numbers.add(randrange(product_count))

        purchase_items = []
        total_price = decimal.Decimal('0')
        for index in random_numbers:
            product = products[index]
            product['quantity'] = randrange(1, 9)
            total_price += product['price'] * decimal.Decimal(product['quantity'])
            product['price'] = str(product['price'])
            log(f'id={product["id"]}, quantity={product["quantity"]}, price={product["price"]}')
            product['productId'] = product['id']
            product.pop('id', None)
            purchase_items.append(product)
        log(f'total price = {total_price}')
        r = requests.post(url=BASE_URL + '/orders', data=json.dumps(purchase_items), headers=get_auth_headers())
        print_pretty_json(r.text)
        json_content = r.json()
        self.assertEqual(0, json_content['code'])


if __name__ == '__main__':
    unittest.main()
