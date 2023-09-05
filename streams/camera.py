import os
import cv2
import time
import pandas as pd
from detector import Detector
from .base_camera import BaseCamera
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'protocol_whitelist;file,rtp,udp'

class Camera(BaseCamera):
    #camera = [None] * BaseCamera.movie_num
    camera = {}
#   d = Detector()

    @staticmethod
    def frames(num):
        
        # 現在のスクリプトのディレクトリを取得
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # 一つ上のディレクトリを取得
        parent_dir = os.path.dirname(current_dir)

        # videoというフォルダへのパスを生成
        video_dir = os.path.join(parent_dir, 'video')
        
        #print("using frames method in Camera class")
        d = Detector() # オブジェクト生成
        print("****frames() in Camera class with "+str(num))
        Camera.camera[num] = cv2.VideoCapture(video_dir + "/stream_{i}.sdp".format(i=num))
        if not Camera.camera[num].isOpened():
            print('Could not start stream_{i}.sdp.'.format(i=num))
            Camera.camera[num].release()
            return
        else:
            print('Start stream_{i}.sdp.'.format(i=num))

        fps = Camera.camera[num].get(cv2.CAP_PROP_FPS) # FPS確認
        print(fps)
        
        basetime = time.time()
        # basetime2 = time.time()
        f_count = 0 #frame count
        count = 0 # object_listの添字
        object_list=[] # 検出した対象物の数
        object_list.append(0) # 初期値
        time_list=[] # 一枚の処理時間
        fps_list=[] # fps
        # 最初の映像が始まる時の誤差
        

        while True:
            # read current frame
            try:
                _, img = Camera.camera[num].read()
                # img = cv2.resize(img, dsize=(640, 480)) # 画像を(640, 480)にリサイズ
                img = cv2.resize(img, dsize=(1080, 720)) # 画像を(640, 480)にリサイズ
                # Detector2に移譲、 第一引数:画像, 第二引数:前の画像の対象物の数
                # img:画像, n_o:検出した対象物の数, tm:画像1枚の処理時間
                img, n_o, tm = d.detect(img, object_list[count]) 
                object_list.append(n_o) # 対象物数をリストへ
                time_list.append(tm) # 処理時間をリストへ
                f_count += 1
                count += 1
                now = time.time()
                seconds = now - basetime
                # FPS計算
                if seconds >= 1:
                    basetime = time.time()
                    print("fps:{}".format(f_count))
                    fps_list.append(f_count)
                    f_count = 0

                """
                # もし経過時間が10秒ならcsvファイルに保存する
                seconds2 = now -basetime2
                if seconds2 >= 10:
                    # 提案手法のcsvファイル作成
                    num = 90
                    text = "dy3"
                    #dfO = pd.DataFrame(object_list)
                    dfT = pd.DataFrame(time_list)
                    dfF = pd.DataFrame(fps_list)
                    dfT[1] = dfF
                    #dfO[2] = dfF
                    #rt = time.time() - basetime2
                    #print(f'time:{rt}')
                    dfT.columns = ['処理時間', 'FPS']
                    dfT.to_csv(f'./csv_camera/{num}_{text}.csv', index=True)
                    print("compleat to csv!")
                """

                # encode as a jpeg image and return it
                # 順次画像を返していく
                yield cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 100])[1].tobytes()
            except Exception as e:
                # print("Can not read image or resize in Camera class. So release")
                print(f'Error in camera.py: {e}')
                #Camera.camera[num].release()
                """ 
                # 提案手法のcsvファイル作成
                num = 30
                text = "dy3"
                #dfO = pd.DataFrame(object_list)
                dfT = pd.DataFrame(time_list)
                dfF = pd.DataFrame(fps_list)
                dfT[1] = dfF
                #dfO[2] = dfF
                #rt = time.time() - basetime2
                #print(f'time:{rt}')
                dfT.columns = ['処理時間', 'FPS']
                dfT.to_csv(f'./csv_camera/{num}_{text}.csv', index=True)
                print("compleat to csv!")
                """

                return

