import hashlib


def md5(string):
    m = hashlib.md5()
    m.update(string.encode(encoding='utf-8'))
    return m.hexdigest()


def sha256(string):
    sha = hashlib.sha256()
    sha.update(string.encode(encoding='utf-8'))
    return sha.hexdigest()
