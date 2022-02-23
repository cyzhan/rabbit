from typing import Union


def response_ok(data=None, new_token=None) -> dict:
    response = {'code': 0, 'msg': 'ok'}
    if data is not None:
        response['data'] = data
    if new_token is not None:
        response['newToken'] = new_token
    return response


def response_error(code: int, msg: str, new_token=None) -> dict:
    if new_token is None:
        return {'code': code, 'msg': msg}
    return {'code': code, 'msg': msg, 'newToken': new_token}

