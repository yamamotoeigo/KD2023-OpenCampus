import os
import cv2
import time
import pandas as pd
from detector import Detector
from .base_camera import BaseCamera
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'protocol_whitelist;file,rtp,udp'

class Video(BaseCamera):
    #camera = [None] * BaseCamera.movie_num
    camera = {}
    d = Detector()

    @staticmethod
    def frames(num):
        # 現在のスクリプトのディレクトリを取得
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # 一つ上のディレクトリを取得
        parent_dir = os.path.dirname(current_dir)

        # videoというフォルダへのパスを生成
        video_dir = os.path.join(parent_dir, 'video')
        
        #print("using frames method in Video class")
        # d = Detector2()
        print("****frames() in Video class with "+str(num))
        # Video.camera[num] = cv2.VideoCapture(video_dir + "/lab_{i}.mp4".format(i=num))

        Video.camera[0] = cv2.VideoCapture(video_dir + "/camera1.mp4")
        Video.camera[1] = cv2.VideoCapture(video_dir + "/camera2.mp4")
        # Video.camera[0] = cv2.VideoCapture(video_dir + "/camera1_fps10.mp4")
        # Video.camera[1] = cv2.VideoCapture(video_dir + "/camera2_fps10.mp4")
        fps = Video.camera[num].get(cv2.CAP_PROP_FPS)
        print(f'----fps: {fps}----')

        if not Video.camera[num].isOpened():
            print('Could not start lab video stream_{i}'.format(i=num))
            Video.camera[num].release()
            return
        else:
            print('Start lab_video_{i}.sdp.'.format(i=num))

        #set paramaters -> upperとunderの値をそれぞれyolov3,v5,MNv2を実施し決定する
        #info_listはそれぞれの手法のobject, time, fpsのリストが格納されている
        #e = Experiment()
        #info_list = e.run(num, d)


        basetime = time.time()
        # basetime2 = time.time()
        f_count = 0  #the number of images per 1 sec
        count = 0  #the number of images
        object_list=[]  #the number of objects in images for csvfile
        object_list.append(0) # 初期値
        time_list=[]  #the time of inference in an image for csvfile
        fps_list=[]  #fps list
        print(Video.camera[num])

        while True:
            # read current frame
            try:
                _, img = Video.camera[num].read()
                img = cv2.resize(img, dsize=(640, 480))
                #img, n_o, tm = d.detect(img, count) #inference
                # if -> 最初の画像の処理, else -> 最初以外
                # detect(img, 前の画像に映る対象物の数)
                # img -> 解析画像, n_o -> 対象物の数, tm -> 処理時間
                img, n_o, tm = Video.d.detect(img, object_list[count])
                object_list.append(n_o)
                time_list.append(tm)
                #To 6:4(Cut center field)
                #img = img[0:512,83:416] 
                f_count += 1
                count += 1
                now = time.time()
                #print(f'detect time:{now - detect_starttime}s')
                #print("1 detect time:{}".format(now - detect_starttime))
                seconds = now - basetime
                # if -> 処理が1秒経つとfpsを計算し表示する
                if seconds >= 1:
                    basetime = time.time()
                    print("fps:{}".format(f_count))
                    fps_list.append(f_count)
                    f_count = 0
                # encode as a jpeg image and return it
                
                #save videos
                #writer.write(img)
                yield cv2.imencode('.jpg', img)[1].tobytes()
                #else:
                #    Video.camera[num].set(cv2.CAP_PROP_POS_FRAMES, 0)
            except Exception as e:
                #writer.release()
                # print("Can not read image or resize in Camera class. So release")
                print(f'Error in video.py: {e}') 
                return
