from ultralytics import YOLO
import torch
import numpy as np
import time
import cv2
import matplotlib.pyplot as plt

print(f'\nyolo-v8m')
# print(f'GPUの使用可否: {torch.cuda.is_available()}')
# print(f'利用可能なGPU数: {torch.cuda.device_count()}')
# print(f'GPU名: {torch.cuda.get_device_name()}')

# 画像の縁に色付きの線を引く (YOLOv5は青色)
class Detector_yolov8m():
    def __init__(self):
        # モデルの読み込み
        self.model = YOLO('yolov8m.pt')
        
    def draw_edge(self, image, band_width=20, color=[255,255,255]):
        height, width, channel = image.shape[0], image.shape[1], image.shape[2] # 画像サイズ取得
        image = image.copy()
        # 1. bottom line
        image[height - band_width:height, :, :] = color
        # 2. top line
        image[0: band_width, :, :] = color
        # 3. left line
        image[:, 0:band_width, :] = color
        # 4. right line
        image[:, width - band_width:width, :] = color
        return image


    # yolov5sの実行
    def detector(self, image):
        print("----------YOLOv8m----------")
        time_sta = time.time()
        # 推論を行う
        # image: 画像, save: 推論結果の画像を保存するか, conf: 信頼度の閾値, device: GPUの使用
        results = self.model(image, save=False, conf=0.5, iou=0.4, classes=0, device=2)
        
        # 検出した画像の二次元配列を取得
        results_detected = results[0].plot()
        # BGRからRGBに変換
        # res_plotted_rgb = cv2.cvtColor(results_detected, cv2.COLOR_BGR2RGB)
        # 検出した画像の縁に色付きの線を引く（検出に使用しているアルゴリズムを見分けるため）
        image = self.draw_edge(image=results_detected, band_width=20, color=[255,0,0])

        # 検出したオブジェクトの数
        num_objects = len(results[0].boxes)
        print(f'object:{num_objects}')
        time_end = time.time()
        tim = time_end - time_sta
        
        return image, num_objects, tim
