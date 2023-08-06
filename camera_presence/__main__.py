import queue
import yaml
import threading
from flask import Flask, Response, current_app
from camera_presence.detection import Detection
from camera_presence.motor_control import Control

app = Flask(__name__)

feed_buffers = {}
motor_queue = queue.Queue()

def process_feed(queue):
    #Clean the feed buffer
    while not queue.empty():
        queue.get()

    while True:
        while not queue.empty():
            frame = queue.get()
            yield frame

@app.route('/')
def index():
    return current_app.send_static_file('index.html')

@app.route('/video_feed/<feed_name>')
def video_feed(feed_name):
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(
        process_feed(feed_buffers[feed_name]),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/motor/front')
def motor_front():
    motor_queue.put('front')

    return 'Ok'

@app.route('/motor/back')
def motor_back():
    motor_queue.put('back')

    return 'Ok'

def load_yaml():
    with open("config.yml", "r") as stream:
        return yaml.safe_load(stream)


def main():
    print('Main on thread: ', threading.get_ident())

    feed_buffers['test'] = queue.Queue()

    detector = Detection(
        'test',
        feed_buffers['test'],
        motor_queue
    )

    detector.run()

    motor_control = Control(motor_queue)

    motor_control.run()

    #DO !!!!!!!NOT!!!!!!! RUN WITH DEBUG, DOUBLE OF THREADS
    app.run(host='0.0.0.0', debug=False)


if __name__ == '__main__':
    main()
