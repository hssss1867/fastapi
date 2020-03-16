from fastapi import FastAPI
from db import RedisClient
import uvicorn
app = FastAPI()

client = RedisClient()

@app.get("/get")
def get():
    return client.random()


if __name__ == '__main__':
    uvicorn.run(app=app,
                host='0.0.0.0',
                port=8000)
