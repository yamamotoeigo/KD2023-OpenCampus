import time
import threading
import numpy as np
from threading import Lock

try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident

class CameraEvent(object):
    def __init__(self):
        self.events = {}

    def wait(self):
        ident = get_ident()
        if ident not in self.events:
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        now = time.time()
        remove = None
        for ident, event in self.events.items():
            if not event[0].isSet():
                event[0].set()
                event[1] = now
            else:
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        self.events[get_ident()][0].clear()

class BaseCamera(object):
    thread = {}
    frame = {}
    last_access = {}
    # event = []
    event = {}
    movie_num = 2
    semaphore = Lock()

    def __init__(self):
        # for文説明
        # 1回目のコンストラクタ -> movie_num回分、BaseCameraのリストに要素を入れて、threadリストにThread(_thread)を入れてstartする
        # 
        # print("----------------basecamera.py")
        for i in range(BaseCamera.movie_num):
            #print(f'BaseCamera outside:{i}')
            if i not in BaseCamera.thread.keys():
                #print(f"BaseCamera inside:{i}")
                BaseCamera.frame[i] = None
                BaseCamera.last_access[i] = time.time()
                BaseCamera.event[i] = CameraEvent()
                #print(f"starting threading.Thread(_thread, {i})")
                BaseCamera.thread[i] = threading.Thread(target=self._thread, args = (i,)) # _thread()がスタート
                BaseCamera.thread[i].start()
                #while self.get_frame(i) is None:
                #    time.sleep(0)
            else:
                if BaseCamera.thread[i] is None:
                    print("In constracta, starts thread: "+str(i))
                    BaseCamera.thread[i] = threading.Thread(target=self._thread, args = (i,)) # _thread()がスタート
                    BaseCamera.thread[i].start()
                #while self.get_frame(i) is None:

    def get_frame(self, num):
        print("using get_frame method in BaseCamera class")
        #if BaseCamera.frame[num] is None:
        #    print("Frame is None")
        #else:
        #    print("Frame is existed")
        #print("Get frame method:"+str(num)+"thread sum: "+ str(len(BaseCamera.thread)))
        BaseCamera.last_access[num] = time.time()
        BaseCamera.event[num].wait()
        BaseCamera.event[num].clear()
        return BaseCamera.frame[num]

    @staticmethod
    def frames(num):
        print("using frames method in BaseCamera class")
        raise RuntimeError('Must be implemented by subclasses.(frames{i})'.format(i=num))


    @classmethod
    def _thread(cls, num):
        # frames()が繰り返される
        # print("using _thread method in BaseCamera class")
        # print('Starting camera thread{i}.'.format(i=num))
        frame_iterator = cls.frames(num)
        print("---frame_iterator set okay!---")
        i=0
        for frame in frame_iterator:
            print(f'count:{i}, in frame_iterator')
            BaseCamera.frame[num] = frame
            BaseCamera.event[num].set()  # send signal to clients
            time.sleep(0)
            # time.sleep(0.5)
            i+=1
            # if there hasn't been any clients asking for frames in 100 seconds
            if time.time() - BaseCamera.last_access[num] > 86400:
                frame_iterator.close()
                print('Stopping camera thread due to inactivity.(frames{i})'.format(i=num))
                break
        print("Basecamera thread "+str(num)+" is set None and New thread")
        BaseCamera.thread[num] = None
        #BaseCamera.thread[num] = threading.Thread(target=cls._thread, args = (num,))
        #BaseCamera.thread[num].start()
                #while self.get_frame(i) is None:
    
    """
    @classmethod
    def _thread(cls, num):
        with cls.lock:
        # frames()が繰り返される
        # print("using _thread method in BaseCamera class")
        # print('Starting camera thread{i}.'.format(i=num))
            frame_iterator = cls.frames(num)
            print("---frame_iterator set okay!---")
            i=0
            for frame in frame_iterator:
                print(f'count:{i}, in frame_iterator')
                BaseCamera.frame[num] = frame
                BaseCamera.event[num].set()  # send signal to clients
                time.sleep(0)
                # time.sleep(0.5)
                i+=1
                # if there hasn't been any clients asking for frames in 100 seconds
                if time.time() - BaseCamera.last_access[num] > 86400:
                    frame_iterator.close()
                    print('Stopping camera thread due to inactivity.(frames{i})'.format(i=num))
                    break
            print("Basecamera thread "+str(num)+" is set None and New thread")
            BaseCamera.thread[num] = None
            #BaseCamera.thread[num] = threading.Thread(target=cls._thread, args = (num,))
            #BaseCamera.thread[num].start()
                    #while self.get_frame(i) is None:
    """
