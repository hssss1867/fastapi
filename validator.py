from db import RedisClient
import aiohttp
import asyncio
from aiohttp import ClientError, ClientConnectionError
import time
import requests
from requests.exceptions import ConnectionError, ConnectTimeout
VALID_STATUS_CODES = [200]
TEST_URL = 'https://www.baidu.com'
BATCH_TEST_SIZE = 100


class Tester(object):
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('正在测试', proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=10) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redis.max(proxy)
                    else:
                        self.redis.decrease(proxy)
                        print('请求响应不合法', proxy)
            except (ClientConnectionError, ClientError, ConnectTimeout):
                self.redis.decrease(proxy)
                print('代理请求失败', proxy)

    def run(self):
        print('测试器开始运行')
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            for i in range(0,len(proxies),BATCH_TEST_SIZE):
                test_proxies = proxies[i:i + BATCH_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print('测试器发生错误', e.args)

    def test_single_tread(self, proxy):
        real_proxy = {'https': 'https://' + proxy}
        print('测试', real_proxy)
        try:
            res = requests.get(TEST_URL, proxies=real_proxy, timeout=5)
            if res.status_code in VALID_STATUS_CODES:
                self.redis.max(proxy)
            else:
                self.redis.decrease(proxy)
        except (ConnectionError, ConnectTimeout):
            self.redis.decrease(proxy)
            print('代理请求失败', proxy)

    def new_run(self):
        for ip in self.redis.all():
            self.test_single_tread(ip)


if __name__ == '__main__':
    db = RedisClient()
    tester = Tester()
    # while True:
    #     print('测试器开始')
    #     tester.run()
    #     time.sleep(5)
    for i in db.all():
        tester.test_single_tread(i)
