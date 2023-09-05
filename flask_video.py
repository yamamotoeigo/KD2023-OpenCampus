# インポートセクション
from itertools import count  # 無限の整数のイテレータを提供するための関数
from flask import Flask, render_template, request, jsonify, Response  # Flask関連のライブラリをインポート
import time  # 時間に関する関数を提供するモジュール
import datetime  # 日付と時間に関する関数を提供するモジュール
import os  # OS関連の操作を提供するモジュール
import shutil  # ファイルやディレクトリの操作を提供するモジュール
from streams.video import Video  # Videoクラスをインポート

# 定義セクション
frame = {}  # フレームデータを格納するためのディクショナリ
REP_TIME = 86400  # 代表的な時間を定義（24時間を秒で表したもの）
DISPLAY_NUM = 50  # 表示するフレーム数を定義
start_time = time.time()  # 開始時間を取得
app = Flask(__name__)  # Flaskアプリケーションを初期化

@app.route("/")  # ルートURLへのアクセスを処理
def minato():
    return render_template('minato2.html')  # minato2.htmlをレンダリングしてクライアントに送信

@app.route("/index")  # /indexへのアクセスを処理
def index():
    return render_template('index.html')  # index.htmlをレンダリングしてクライアントに送信

@app.route("/bus_stream3")  # /bus_stream3へのアクセスを処理
def bus_stream3():
    return render_template('bus_stream3.html')  # bus_stream3.htmlをレンダリングしてクライアントに送信

@app.route("/bus_stream2")  # /bus_stream2へのアクセスを処理
def bus_stream2():
    return render_template('bus_stream2.html')  # bus_stream2.htmlをレンダリングしてクライアントに送信

def gen(camera, num):  # ビデオストリーミングのためのジェネレータ関数
    while True:  # 無限ループ
        frame[num] = camera.get_frame(num)  # カメラからフレームを取得
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame[num] + b'\r\n')  # フレームデータを送信

@app.route('/video_feed/<int:num>')  # /video_feed/<num>へのアクセスを処理
def video_feed(num):
    return Response(gen(Video(), num),mimetype='multipart/x-mixed-replace; boundary=frame')  # ビデオストリームをレスポンスとして送信

@app.route("/abstract")
def abstract():
    return render_template('abstract.html')

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=30080, threaded=True)  # Flaskアプリケーションを起動