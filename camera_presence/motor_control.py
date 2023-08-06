import RPi.GPIO as GPIO
from threading import Thread

class Control:
    def __init__(self, queue):
        self.queue = queue

    def front(self):
        print('From motor thread, front')

    def back(self):
        print('From motor thread, back')

    def stop(self):
        print('From motor thread, STOP!n')

    def worker(self):
        while True:
            data = self.queue.get()
            if data == 'front':
                self.front()
            elif data == 'back':
                self.back()
            elif data == 'stop':
                self.stop()

    def run(self):
        t1 = Thread(target=self.worker, daemon=True)
        t1.start()

