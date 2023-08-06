import cv2
import time
import json
from threading import Thread

import base64

class Detection:
    def __init__(self, name, feed_queue, motor_queue):
        self.frame_counter = 0

        self.current_face_id = 0
        self.face_trackers = {}
        self.write_to_flask_enabled = True
        self.web_fps = 10
        self.web_resolution = [854, 480]
        self.feed_queue = feed_queue
        self.motor_queue = motor_queue

    def write_to_flask(self, image, buffer):
        ret, buffer2 = cv2.imencode('.png', image)

        buffer.put(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer2.tobytes() + b'\r\n')

    def write_image(self, image):
        print('Writing Cropped shape')
        print(image.shape)

        cv2.imwrite(self.write_image_output + str(time.time()) + '.png', image)

    def worker(self):
        capture = cv2.VideoCapture(0)

        capture.set(3, 640)
        capture.set(4, 480)

        rc, feedTestSize = capture.read()
        print('Feed shape')
        print(feedTestSize.shape)

        rectangleColor = (0, 165, 255)

        # faceCascade = cv2.CascadeClassifier('/home/pi/HAAR-Remote-Control/camera_presence/haarcascade_frontalface_alt2.xml')
        faceCascade = cv2.CascadeClassifier('/home/pi/HAAR-Remote-Control/camera_presence/cascade.xml')

        while True:
            #Capture next frame
            rc, fullSizeBaseImage = capture.read()

            self.frame_counter += 1
            # print(self.frame_counter)

            #Resize the image to 320x240
            baseImage = fullSizeBaseImage

            if (self.frame_counter % 5) == 0:
                gray = cv2.cvtColor(baseImage, cv2.COLOR_BGR2GRAY)

                faces = faceCascade.detectMultiScale(
                    gray,
                    # scaleFactor=1.8,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(20, 20),
                    # maxSize=(120, 120),
                )
                # faces = faceCascade.detectMultiScale(gray, 50, 50)

                for (_x,_y,_w,_h) in faces:
                    print('GOT IT!')
                    self.motor_queue.put('stop')
                    x = int(_x)
                    y = int(_y)
                    w = int(_w)
                    h = int(_h)

                    if self.write_to_flask_enabled:
                        cv2.rectangle(baseImage, (x-10, y-20), (x + w+10 , y + h+20), rectangleColor, 2)


            if self.write_to_flask_enabled and self.frame_counter % self.web_fps:
                # baseImage = cv2.resize(fullSizeBaseImage, tuple(self.web_resolution))

                self.write_to_flask(baseImage, self.feed_queue)
                # self.write_to_flask(gray, self.feed_queue)
                # self.write_image(crop_img)

    def run(self):
        t1 = Thread(target=self.worker, daemon=True)
        t1.start()
