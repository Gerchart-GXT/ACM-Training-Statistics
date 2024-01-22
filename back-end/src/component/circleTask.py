import schedule
import time
import threading

class CircleTask:
    def __init__(self, task, TSecond):
        self.lock = threading.Lock()
        self.running = False
        self.task = task
        self.TSecond = TSecond
    
    def _lockAndRun(self):
        if not self.running:
            with self.lock:
                if not self.running:
                    self.running = True
                    self.task()
                    self.running = False
        
    def _runSchedule(self):
        while True:
            schedule.run_pending()
            time.sleep(1)
        
    def run(self):
        schedule.every(self.TSecond).seconds.do(self._lockAndRun)
        self.scheduleThread = threading.Thread(target=self._runSchedule)
        self.scheduleThread.start()

    def __del__(self):
        self.scheduleThread.join()