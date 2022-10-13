import re
import urllib.parse
from urllib.parse import quote

from ._base import Provider


class GoogleTranslateProvider(Provider):
    def __init__(self):
        super().__init__()
        self._host = 'https://translate.google.com'
        self._headers = self._get_headers()

    def _get_headers(self) -> dict:
        return {
            'Referer': self._host,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/55.0.2883.87 Safari/537.36",
        }

    def translate(self, from_language: str, to_language: str, text: str) -> str:
        html_data = self._session.get(self._host, headers=self._headers).text
        tkk = re.findall("tkk:'(.*?)'", html_data)[0]
        tk = self.acquire(text, tkk)

        response = self._session.get(
            'https://translate.googleapis.com/translate_a/single',
            params={
                'client': 'webapp',
                'sl': from_language,
                'tl': to_language,
                'dt': ['at', 'bd', 'ex', 'ld', 'md', 'qca', 'rw', 'rm', 'ss', 't'],
                'ie': 'UTF-8',
                'oe': 'UTF-8',
                'source': 'bh',
                'ssel': 0,
                'tsel': 0,
                'kc': 1,
                'tk': tk,
                'q': quote(text),
            },
        )

        response.raise_for_status()
        response_text = response.json()[0][0][0]
        return urllib.parse.unquote_plus(response_text)

    def _xr(self, a, b):
        size_b = len(b)
        c = 0
        while c < size_b - 2:
            d = b[c + 2]
            d = ord(d[0]) - 87 if 'a' <= d else int(d)
            d = (a % 2**32) >> d if '+' == b[c + 1] else a << d
            a = a + d & (2**32-1) if '+' == b[c] else a ^ d
            c += 3
        return a


    def _ints(self, text):
        ints = []
        for v in text:
            int_v = ord(v)
            if int_v < 2**16:
                ints.append(int_v)
            else:
                # unicode, emoji
                ints.append(int((int_v - 2**16) / 2**10 + 55296))
                ints.append(int((int_v - 2**16) % 2**10 + 56320))
        return ints


    def acquire(self, text, tkk):
        ints = self._ints(text)
        size = len(ints)
        e = []
        g = 0

        while g < size:
            l = ints[g]
            if l < 2**7: # 128(ascii)
                e.append(l)
            else:
                if l < 2**11: # 2048
                    e.append(l >> 6 | 192)
                else:
                    if (l & 64512) == 55296 and g + 1 < size and ints[g + 1] & 64512 == 56320:
                        g += 1
                        l = 65536 + ((l & 1023) << 10) + (ints[g] & 1023)
                        e.append(l >> 18 | 240)
                        e.append(l >> 12 & 63 | 128)
                    else:
                        e.append(l >> 12 | 224)
                    e.append(l >> 6 & 63 | 128) ##
                e.append(l & 63 | 128)
            g += 1

        b = tkk if tkk != '0' else ''
        d = b.split('.')
        b = int(d[0]) if len(d) > 1 else 0

        a = b
        for value in e:
            a += value
            a = self._xr(a, '+-a^+6')
        a = self._xr(a, '+-3^+b+-f')
        a ^= int(d[1]) if len(d) > 1 else 0
        if a < 0:
            a = (a & (2**31-1)) + 2**31
        a %= int(1E6)
        return '{}.{}'.format(a, a ^ b)


