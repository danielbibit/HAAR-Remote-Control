import queue
import yaml
# from multiprocessing import Process, Queue
import threading
from flask import Flask, Response
from camera_presence.detection import Detection

app = Flask(__name__)

feed_buffers = {}


@app.route('/video_feed/<feed_name>')
def video_feed(feed_name):
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(
        Detection.process_feed(feed_buffers[feed_name]),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


def load_yaml():
    with open("config.yml", "r") as stream:
        return yaml.safe_load(stream)


def main():
    print('Main on thread: ', threading.get_ident())

    # config_file = load_yaml()

    # for key, feed_config in config_file['feeds'].items():
    #     print('Creating detection worker for: ', key)

    feed_buffers['test'] = queue.Queue()

    detector = Detection(
        'test',
        feed_buffers['test']
    )

    detector.run()

    #DO !!!!!!!NOT!!!!!!! RUN WITH DEBUG, DOUBLE OF THREADS
    app.run(host='0.0.0.0', debug=False)


if __name__ == '__main__':
    main()
