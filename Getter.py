from db import RedisClient
from crawler import Crawler

POOL_UPPER_THRESHOLD = 10000


class Getter(object):
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshhold(self):
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        print('获取器开始执行')
        if not self.is_over_threshhold():
            proxies = self.crawler.run()
            for ip in proxies:
                self.redis.add(ip)
                print('已抓取', ip)
        print('结束,共抓取', self.redis.count())
        for i in self.redis.all():
            print(i, '当前分数', self.redis.score(i))


if __name__ == '__main__':
    getter = Getter()
    getter.run()
