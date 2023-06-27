# Face detection and tracking based on https://github.com/gdiepen/face-recognition
# https://answers.opencv.org/question/207286/why-imencode-taking-so-long/
import cv2
import dlib
import time
import json
# from multiprocessing import Process
from threading import Thread

import paho.mqtt.client as mqtt
import base64

class Detection:
    def __init__(self, name, queue):
        self.frame_counter = 0

        self.current_face_id = 0
        self.face_trackers = {}
        self.write_to_flask_enabled = True
        self.web_fps = 15
        self.web_resolution = [480, 480]
        self.queue = queue

    def process_feed(queue):
        #Clean the feed buffer
        while not queue.empty():
            queue.get()

        while True:
            while not queue.empty():
                frame = queue.get()
                yield frame




    def write_to_flask(self, image, buffer):
        ret, buffer2 = cv2.imencode('.png', image)

        buffer.put(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer2.tobytes() + b'\r\n')

    def worker(self):
        capture = cv2.VideoCapture(0)

        rc, feedTestSize = capture.read()
        print('Feed shape')
        print(feedTestSize.shape)

        rectangleColor = (0, 165, 255)

        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + '/haarcascade_frontalface_alt2.xml')

        while True:
            #---------STARTING TIMER--------------------
            time_get_frame = time.time()
            #Capture next frame
            rc, fullSizeBaseImage = capture.read()

            self.frame_counter += 1
            #---------ENDING TIMER----------------------


            #---------STARTING TIMER--------------------
            time_resizing = time.time()

            #Resize the image to 320x240
            baseImage = fullSizeBaseImage

            #---------ENDING TIMER----------------------

            # resultImage = baseImage.copy()

            #---------ENDING TIMER----------------------

            if (self.frame_counter % 5) == 0:
                #For the face detection, we need to make use of a gray
                #colored image so we will convert the baseImage to a
                #gray-based image
                #---------STARTING TIMER--------------------
                time_grey = time.time()
                gray = cv2.cvtColor(baseImage, cv2.COLOR_BGR2GRAY)

                #---------ENDING TIMER----------------------

                #Now use the haar cascade detector to find all faces
                #in the image
                #---------STARTING TIMER--------------------
                time_detecting = time.time()

                faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.8,
                    minNeighbors=5,
                    minSize=(60, 60),
                    # maxSize=(120, 120),
                )

                #---------ENDING TIMER----------------------

                #We need to convert it to int here because of the
                #requirement of the dlib tracker. If we omit the cast to
                #int here, you will get cast errors since the detector
                #returns numpy.int32 and the tracker requires an int
                for (_x,_y,_w,_h) in faces:
                    x = int(_x)
                    y = int(_y)
                    w = int(_w)
                    h = int(_h)

                    if self.write_to_flask_enabled:
                        cv2.rectangle(baseImage, (x-10, y-20), (x + w+10 , y + h+20), rectangleColor, 2)

                    #calculate the centerpoint
                    x_bar = x + 0.5 * w
                    y_bar = y + 0.5 * h



            if self.write_to_flask_enabled and self.frame_counter % self.web_fps:
                #---------STARTING TIMER--------------------
                time_to_flask = time.time()

                baseImage = cv2.resize(fullSizeBaseImage, tuple(self.web_resolution))

                self.write_to_flask(baseImage, self.queue)

                #---------ENDING TIMER--------------------

    def run(self):
        t1 = Thread(target=self.worker, daemon=True)
        t1.start()
        # p1 = Process(target=self.worker)
        # p1.start()
