import requests
from requests.exceptions import ConnectionError, ConnectTimeout
url1 = 'https://www.xicidaili.com/'
url = 'https://www.baidu.com/'
proxies = {'https': 'https://113.247.252.114:9090'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}


def get_proxy():
    res = requests.get('http://127.0.0.1:8000/get')
    proxies = {'https' : 'https://'+res.text[1:-1]}
    return proxies
# res = requests.get(url, proxies=get_proxy(),timeout=15)


def f1():
    try:
        res = requests.get(url, proxies=proxies, timeout=10, headers=headers)
        print(res.status_code)
    except (ConnectionError, ConnectTimeout) as e:
        print(e)


# res = requests.get(url, proxies=proxies,timeout=5)
# print(res.status_code)
i = 0
while i < 5:
    f1()
    i += 1
