import requests
from pyquery import PyQuery as pq
from fake_useragent import UserAgent
import time


class Crawler(object):

    def getip(self, link):
        ua = UserAgent(use_cache_server=False)
        headers = {"User-Agent": ua.random}
        res = requests.get(link, headers=headers,)
        doc = pq(res.text)
        info = doc('tr.odd')
        for i in info.items():
            ip = i('td:nth-child(2)').text()
            port = i('td:nth-child(3)').text()
            yield ":".join([ip, port])

    def run(self):
        urls = ['https://www.xicidaili.com/wn/%i' % int(i) for i in range(5)]
        proxies = []
        for url in urls:
            lst = self.getip(url)
            for i in lst:
                proxies.append(i)
            time.sleep(5)
        return proxies
