import multiprocessing
from api import app
from Getter import Getter
from validator import Tester
import time
import uvicorn

TESTER_CYCLE = 10
GETTER_CYCLE = 600
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True





class Scheduler():

    def schedule_tester(self, cycle=TESTER_CYCLE):

        tester = Tester()
        while True:
            print('测试器开始运行')
            tester.new_run()
            time.sleep(cycle)

    def scheduler_getter(self, cycle=GETTER_CYCLE):
        getter = Getter()
        while True:
            print('开始抓取代理')
            getter.run()
            time.sleep(cycle)

    def scheduler_apis(self):
        uvicorn.run(app,
                    host='0.0.0.0',
                    port=8000)

    def run(self):
        global tester_process, getter_process, api_process

        if TESTER_ENABLED:
            tester_process = multiprocessing.Process(target=self.schedule_tester)
            tester_process.start()

        if GETTER_ENABLED:
            getter_process = multiprocessing.Process(target=self.scheduler_getter)
            getter_process.start()

        if API_ENABLED:
            api_process = multiprocessing.Process(target=self.scheduler_apis)
            api_process.start()
        tester_process.join()
        getter_process.join()
        api_process.join()


if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()
