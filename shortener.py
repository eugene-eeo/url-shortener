from uuid import uuid4
from collections import deque
import hashlib
import string


ENCODE = '0123456789' + string.ascii_letters


def to_base_62(n):
    s = deque()
    while n > 0:
        s.appendleft(ENCODE[n % 62])
        n = n // 62
    return ''.join(k for k in s)


def shorten(url):
    h = hashlib.sha256(url.encode('utf-8'))
    h.update(uuid4().bytes)
    u = int('0x' + h.hexdigest().replace('-', ''), 0)
    return to_base_62(u)
