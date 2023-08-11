import RPi.GPIO as GPIO
from threading import Thread
import time

class Control:
    def __init__(self, queue):
        # [1_frente, 1_tras, 2_frente, 2_tras]
        self.pins = [21, 26, 19, 13]
        GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

        self.queue = queue
        self.turn_time = 0.25

    def front(self):
        print('From motor thread, front')
        self.stop()
        GPIO.output(self.pins[0], GPIO.HIGH)
        GPIO.output(self.pins[2], GPIO.HIGH)

    def back(self):
        print('From motor thread, back')
        self.stop()
        GPIO.output(self.pins[1], GPIO.HIGH)
        GPIO.output(self.pins[3], GPIO.HIGH)

    def left(self):
        print('From motor thread, left')
        self.stop()

        GPIO.output(self.pins[2], GPIO.HIGH)
        GPIO.output(self.pins[1], GPIO.HIGH)

        time.sleep(self.turn_time)

        self.stop()

    def right(self):
        print('From motor thread, right')
        self.stop()

        GPIO.output(self.pins[0], GPIO.HIGH)
        GPIO.output(self.pins[3], GPIO.HIGH)

        time.sleep(self.turn_time)

        self.stop()

    def stop(self):
        print('From motor thread, STOP!')
        for pin in self.pins:
            GPIO.output(pin, GPIO.LOW)

    def test_motor(self, n):
        GPIO.output(self.pins[n], GPIO.HIGH)
        time.sleep(5)
        GPIO.output(self.pins[n], GPIO.LOW)

    def worker(self):
        while True:
            data = self.queue.get()
            if data == 'front':
                self.front()
            elif data == 'back':
                self.back()
            elif data == 'left':
                self.left()
            elif data == 'right':
                self.right()
            elif data == 'stop':
                self.stop()

    def run(self):
        # self.test_motor(3)
        t1 = Thread(target=self.worker, daemon=True)
        t1.start()

