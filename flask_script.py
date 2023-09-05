# coding: utf-8
from flask import Flask, render_template, request, jsonify, Response
import time
import datetime
import os
import shutil
from streams.camera import Camera
from streams.video import Video

#Difinition
frame = [None] * 4
REP_TIME = 86400
DISPLAY_NUM =50
start_time = time.time()
persons_file_1 = "/home/mizutani/flask/templates/data/bus1"
persons_file_2 = "/home/mizutani/flask/templates/data/bus2"
app = Flask(__name__)
#camera = Camera(2)

@app.route("/")
def minato():
    return render_template('minato2.html')

@app.route("/lab")
def lab():
    return render_template('lab.html')

@app.route("/bus_stream0")
def bus_stream0():
    return render_template('bus_stream0.html')

@app.route("/bus_stream1")
def bus_stream1():
    return render_template('bus_stream1.html')

@app.route("/bus_stream2")
def bus_stream2():
    return render_template('bus_stream2.html')

@app.route("/bus_stream3")
def bus_stream3():
    return render_template('bus_stream3.html')

@app.route("/abstract")
def abstract():
    return render_template('abstract.html')

# def get_persons(persons_file):
#     f = open(persons_file, "r")
#     p = f.readlines()
#     persons = ["<p>"+i+"</p>" for i in p]
#     if len(persons) > DISPLAY_NUM:
#         persons = persons[len(persons) - DISPLAY_NUM:len(persons)-1]
#     persons = "".join(persons)
#     return persons

def gen(camera, num):
    """Video streaming generator function."""
    # Cameraクラスのframes()の結果が順次返ってくるため、それをhtmlへ送る
    while True:
        frame[num] = camera.get_frame(num)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame[num] + b'\r\n')

@app.route('/video_feed/<int:num>')
def video_feed(num):
    """Real-time streaming route. Put this in the src attribute of an img tag."""
    # Cameraクラスのオブジェクトをgen()に渡す
    # Cameraクラスのオブジェクトを生成し、親クラスのBaseCameraクラスが生成され、__init__でスレッドがスタート
    return Response(gen(Camera(), num),mimetype='multipart/x-mixed-replace; boundary=frame')
    #return Response(gen(Camera(2), num),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    #start_time = time.time()
    app.run(debug=False, host='0.0.0.0', port=20080, threaded=True)
    # app.run(debug=False, host='0.0.0.0', port=80, threaded=True)
    #app.run(host='0.0.0.0', port=20080, ssl_context=('/home/mizutani/docor.cer', '/home/mizutani/docor.key'), threaded=True, debug=True)
