import requests
from pyquery import PyQuery as pq
from fake_useragent import UserAgent
import time


def getip(link):
    ua = UserAgent(use_cache_server=False)
    headers = {"User-Agent": ua.random}
    res = requests.get(link, headers=headers,)
    doc = pq(res.text)
    info = doc('tr.odd')
    for i in info.items():
        print(i('td:nth-child(6)').text() + ":" + i('td:nth-child(2)').text() + ":" + i('td:nth-child(3)').text())
        print('======')


if __name__ == '__main__':
    urls = ['https://www.xicidaili.com/wn/%i' % int(i) for i in range(2)]
    for url in urls:
        getip(url)
        time.sleep(5)
    print('finished!!')