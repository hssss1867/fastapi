import requests
from pyquery import PyQuery as pq
import time


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}


class Crawler(object):

    def getip(self, link):
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
