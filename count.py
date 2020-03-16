from db import RedisClient
import time


db = RedisClient()
while True:
    print(db.count())
    time.sleep(10)
