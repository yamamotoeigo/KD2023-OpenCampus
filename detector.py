import cv2
import time
import torch
from YOLOv5s import detector_yolov5s as dy5s
from YOLOv8m import detector_yolov8m as dy8m
from YOLOv8l import detector_yolov8l as dy8l


class Detector():
    def __init__(self):
        self.dy5s = dy5s.Detector_yolov5s()
        self.dy8m = dy8m.Detector_yolov8m()
        self.dy8l = dy8l.Detector_yolov8l()
        self.start = True
        self.under = 4  # max value of MobileNetV2
        self.upper = 14  # max value of YOLOv5
        

    def detect(self, image, count):  # count->the number of objects in previous image
        # 最初だけYOLOv3
        if self.start:
            self.start = False
            return self.dy5s.detector(image)
        # Switching algorithm
        # 0 <= x < 4
        if 0 <= count < self.under:
            return self.dy5s.detector(image)
        # 4 <= x < 14
        elif self.under <= count < self.upper:
            return self.dy8m.detector(image)
        # 14 <= x
        else:
            return self.dy8l.detector(image)

# d = Detector()
# img = cv2.imread("/home/yamamoto/workspace/open-campus-yamamoto/test.jpg")
# img, num, tm = d.detect(img, 1)
# print("ok")
# print(f'num object:{num}')