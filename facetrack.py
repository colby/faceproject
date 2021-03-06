#!/usr/bin/env python2
import cv2
from threading import Thread

def face_detect(frame, face_cascade):
    # Read the image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    return frame

class CameraFrenk(object):
    def __init__(self, index):
        self.cap = cv2.VideoCapture(index)
        self.cap.set(cv2.cv.CV_CAP_PROP_FPS, 120)
        self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
        self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
        self.rval, self.frame = self.cap.read()

        # Create the haar cascade
        # Get user supplied values
        casc_path = "./haarcascade_frontalface_alt.xml"
        self.face_cascade = cv2.CascadeClassifier(casc_path)


    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def read(self):
        return (self.rval, self.frame)

    def update(self):
        while True:
            self.rval, self.frame = self.cap.read()
            #self.frame = face_detect(self.frame, self.face_cascade)

def main():
    cv2.namedWindow("preview")

    x0 = CameraFrenk(1)
    x0.start()
    x1 = CameraFrenk(2)
    x1.start()

    capture_threads = (x0, x1)

    while True:
        for capture_thread in capture_threads:
            rval, frame = capture_thread.read()
            cv2.imshow("preview", frame)
            cv2.waitKey(1)

    cv2.destroyWindow("preview")

if __name__ == '__main__':
    main()
