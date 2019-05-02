# -*- coding: utf-8 -*-

"""
多线程版本的语音识别系统
Author:Decadence
Email:leizhang9527@163.com
"""

import Queue
import base64
import json
import threading
import time
import wave
import sys
from time import ctime

from urllib2 import urlopen
from urllib2 import Request
from urllib2 import URLError
from urllib import urlencode


import numpy as np

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature
from PyQt4.QtGui import QMainWindow


from main import Ui_MainWindow
from pyaudio import PyAudio,paInt16


class DemoError(Exception):
    pass


class MyThread (threading.Thread):
    def __init__(self,func, args, name = ''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def getResult(self):
        return self.res

    def run(self):
        print self.name + "开始线程：" + ctime()
        self.res = apply(self.func)
        print self.name + "退出线程：" + ctime()

class MainWindow(QMainWindow, Ui_MainWindow,threading.Thread):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        reload(sys)
        sys.setdefaultencoding('utf8')
        threading.Thread.__init__(self)
        self.name = self.voise_tts.__name__
        self.setupUi(self)

        self.CUID = '123456PYTHON'
        self.RATE = 16000  # 采样率固定值
        self.DEV_PID = 1537  # 1537 表示识别普通话，使用输入法模型。1536表示识别普通话，使用搜索模型。
        self.ASR_URL = 'http://vop.baidu.com/server_api'
        self.SCOPE = 'audio_voice_assistant_get'  # 有此scope表示有asr能力
        self.TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'
        self.chunk = 1024
        self.NUM_SAMPLES = 2000  # 采样点
        self.channels = 1  # 一个声道
        self.sampwidth = 2  # 两个字节十六位

        self.API_KEY = 'GkegucnW3b559fCPZ8eQOkjK'
        self.SECRET_KEY = 'mhinZuFI05jx2K3dFv8yYWnsPxU93tTT'

        self.TIME = 5  # 条件变量，可以设置定义录音的时间
        self.Level = 600
        self.mute_count_limit = 50
        self.mute_begin = 0
        self.mute_end = 1
        self.not_mute = 0
        self.voice_queue = Queue.Queue(1024)
        self.wav_queue = Queue.Queue(1024)
        self.file_name_index = 1
        self.thread_flag = 0
        self.start_flag = 1


    def getResult(self):
        return self.res

    def run(self):
        t = threading.currentThread()  # 获取当前子线程对象
        print self.name + "开始线程：" + ctime()
        self.res = apply(self.voise_tts)
        print self.name + "退出线程：" + ctime()

    def writeQ(self, queue, data):
        queue.put(data, 1)

    def readQ(self, queue):
        val = queue.get(1)
        return val

    def save_wave_file(self, filename, data):
        wf = wave.open(filename, 'wb')  # 二进制写入模式
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.sampwidth)  # 两个字节16位
        wf.setframerate(self.RATE)  # 帧速率
        wf.writeframes(b"".join(data))  # 把数据加进去，就会存到硬盘上去wf.writeframes(b"".join(data))
        wf.close()

    # 录音模块
    def record_wave(self):
        while self.start_flag == 1:
            pa = PyAudio()
            stream = pa.open(format = paInt16, channels = 1,
                             rate = self.RATE, input = True,
                             frames_per_buffer = self.NUM_SAMPLES)
            save_buffer = []
            count = 0
            print '当前正在录音(同时录制系统内部和麦克风的声音)……'
            while count < self.TIME * 30:
                string_audio_data = stream.read(self.NUM_SAMPLES)
                audio_data = np.fromstring(string_audio_data, dtype = np.short)
                large_sample_count = np.sum(audio_data > self.Level)
                print large_sample_count
                if large_sample_count < self.mute_count_limit:  # 静音
                    self.mute_begin = 1
                else:
                    save_buffer.append(string_audio_data)
                    self.mute_begin = 0
                    self.mute_end = 1
                count += 1
                if (self.mute_end - self.mute_begin) > 9:  # 留白时间过长
                    self.mute_begin = 0
                    self.mute_end = 1
                    break
                if self.mute_begin:
                    self.mute_end += 1
                print '...'

            save_buffer = save_buffer[:]
            if save_buffer:
                if self.file_name_index < 11:
                    pass
                else:
                    self.file_name_index = 1
                filename = str(self.file_name_index) + '.wav'
                self.save_wave_file(filename = filename, data = save_buffer)
                self.writeQ(queue = self.wav_queue, data = filename)
                self.file_name_index += 1
                print filename + "已经保存"
            else:
                print "文件未保存"
            # self.save_wave_file(filename, my_buf)
            save_buffer = []
            stream.close()

    # 获取token
    def fetch_token(self):
        params = {'grant_type': 'client_credentials',
                  'client_id': self.API_KEY,
                  'client_secret': self.SECRET_KEY}
        post_data = urlencode(params)
        post_data = post_data.encode('utf-8')
        req = Request(self.TOKEN_URL, post_data)
        try:
            f = urlopen(req)
            result_str = f.read()
        except URLError as err:
            print 'token http response http code : ' + str(err.code)
            result_str = err.read()
        result_str = result_str.decode()

        print result_str
        result = json.loads(result_str)
        print result

        if ('access_token' in result.keys() and 'scope' in result.keys()):
            print self.SCOPE
            if self.SCOPE and (not self.SCOPE in result['scope'].split(' ')):  # SCOPE = False 忽略检查
                raise DemoError('scope is not correct')
            print 'SUCCESS WITH TOKEN: %s  EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in'])
            return result['access_token']
        else:
            raise DemoError(
                'API_KEY或者SECRET_KEY不正确，请重新设置')

    # 识别模块
    def speech_recognition(self):
        # qRegisterMetaType < s_MSGBoxInfo > ("QTextCursor");
        while True:
            if self.wav_queue.qsize():
                filename = self.readQ(queue = self.wav_queue)
            else:
                continue
            token = self.fetch_token()
            speech_data = []
            with open(filename, 'rb') as speech_file:
                speech_data = speech_file.read()

            length = len(speech_data)
            if length == 0:
                raise DemoError('file %s length read 0 bytes' % filename)
            speech = base64.b64encode(speech_data)
            # speech = str(speech, 'utf-8')
            # speech = str(speech,'')
            params = {'dev_pid': self.DEV_PID,
                      'format': filename[-3:] ,
                      'rate': self.RATE,
                      'token': token,
                      'cuid': self.CUID,
                      'channel': 1,
                      'speech': speech,
                      'len': length
                      }
            post_data = json.dumps(params, sort_keys=False)
            print post_data
            req = Request(self.ASR_URL, post_data.encode('utf-8'))
            req.add_header('Content-Type', 'application/json')
            timer = time.clock
            try:
                begin = timer()
                f = urlopen(req)
                result_str = f.read()
                print "Request time cost %f" % (timer() - begin)
            except URLError as err:
                print 'asr http response http code :' + str(err.code)
                result_str = err.read()

            # resultstr = str(result_str)
            # result_str = resultstr.decode( 'utf-8')
            # print result_str
            # print type(result_str)
            my_temp = json.loads(result_str)
            err = my_temp['err_no']
            print my_temp['err_no']
            if my_temp['err_no']:
                if my_temp['err_no'] == 3300:
                    text = '输入参数不正确'
                    text1 = str(text)
                    text = text1.decode('utf-8')
                    print text
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3301:
                    text = '音频质量过差'
                    text1 = str(text)
                    text = text1.decode('utf-8')
                    print text
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3302:
                    text = '鉴权失败'
                    text1 = str(text)
                    text = text1.decode('utf-8')
                    print text
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3303:
                    text = '语音服务器后端问题'
                    text1 = str(text)
                    text = text1.decode('utf-8')
                    print text
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3304:
                    text = '用户的请求QPS超限'
                    text1 = str(text)
                    text = text1.decode('utf-8')
                    print text
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3305:
                    text = '用户的日pv（日请求量）超限'
                    text1 = str(text)
                    text = text1.decode('utf-8')
                    print text
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3307:
                    text = '语音服务器后端识别出错问题'
                    text1 = str(text)
                    text = text1.decode('utf-8')
                    print text
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3308:
                    text = '音频过长'
                    text1 = str(text)
                    text = text1.decode('utf-8')
                    print text
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3309:
                    text = '音频数据问题'
                    text1 = str(text)
                    text = text1.decode('utf-8')
                    print text
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3310:
                    text = '输入的音频文件过大'
                    text1 = str(text)
                    text = text1.decode('utf-8')
                    print text
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3311:
                    text = '采样率rate参数不在选项里'
                    text1 = str(text)
                    text = text1.decode('utf-8')
                    print text
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3312:
                    text = '音频格式format参数不在选项里'
                    text1 = str(text)
                    text = text1.decode('utf-8')
                    print text
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3313:
                    text = '语音服务器解析超时'
                    text1 = str(text)
                    text = text1.decode('utf-8')
                    print text
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3314:
                    text = '音频长度过短'
                    text1 = str(text)
                    text = text1.decode('utf-8')
                    print text
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3315:
                    text = '语音服务器处理超时'
                    text1 = str(text)
                    text = text1.decode('utf-8')
                    print text
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3316:
                    text = '音频转为pcm失败'
                    text1 = str(text)
                    text = text1.decode('utf-8')
                    print text
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
            else:
                word = my_temp['result']
                print word[0]
                with open("result.txt", "a") as of:
                    if of is None:
                        of.write(word[0])
                    else:
                        of.write('\n')
                        of.write(word[0])
                    self.textEdit.append(word[0])
            time.sleep(0.1)

    def voise_tts(self):
        self.speech_recognition()

    @pyqtSignature("",)
    def on_pushButton_clicked(self):
        if self.thread_flag == 0:
            self.start_flag = 1
            record = MyThread(self.record_wave,(self,),self.record_wave.__name__)
            record.setDaemon(True)
            record.start()
            self.thread_flag =1
        print '开始识别'

    @pyqtSignature("",)
    def on_pushButton_2_clicked(self):
        if self.thread_flag == 1:
            self.start_flag = 0
            self.thread_flag = 0
        print'停止识别'

    @pyqtSignature("", )
    def on_pushButton_3_clicked(self):
        self.textEdit.clear()
        print'清空内容'



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = MainWindow()
    ui.setDaemon(True)
    ui.start()
    ui.show()
    sys.exit(app.exec_())
