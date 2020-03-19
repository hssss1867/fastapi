from db import RedisClient
import requests
from multiprocessing import Pool
from requests.exceptions import ConnectionError, ConnectTimeout, ReadTimeout
VALID_STATUS_CODES = [200]
TEST_URL = 'https://www.baidu.com'
BATCH_TEST_SIZE = 100
redis = RedisClient()


def test_single_tread(proxy):
    real_proxy = {'https': 'https://' + proxy}
    print('测试', real_proxy)
    try:
        res = requests.get(TEST_URL, proxies=real_proxy, timeout=10)
        if res.status_code in VALID_STATUS_CODES:
            redis.max(proxy)
        else:
            redis.decrease(proxy)
    except (ConnectionError, ConnectTimeout, ReadTimeout):
        redis.decrease(proxy)
        print('代理请求失败', proxy)
            
            
if __name__ == '__main__':
    pool = Pool()
    pool.map(test_single_tread, redis.all())
