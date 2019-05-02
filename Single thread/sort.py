# -*- coding: utf-8 -*-

"""
author:Decadence
email:leizhang9527@163.com
单线程版本的语音识别
"""
import queue

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets, QtCore, QtGui
from Ui_file_use import Ui_MainWindow

import json, time, base64, wave
from pyaudio import PyAudio, paInt16
from urllib.request import urlopen, Request
from urllib.error import URLError
from urllib.parse import urlencode
from datetime import datetime

timer = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
filename = timer + ".wav"

import numpy as np

# filename = '16k.wav'



class DemoError(Exception):
    pass


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        time.sleep(2)

        self.CUID = '123456PYTHON'
        self.RATE = 16000  # 采样率固定值
        self.DEV_PID = 1537  # 1537 表示识别普通话，使用输入法模型。1536表示识别普通话，使用搜索模型。根据文档填写PID，选择语言及识别模型
        self.ASR_URL = 'http://vop.baidu.com/server_api'
        self.SCOPE = 'audio_voice_assistant_get'  # 有此scope表示有asr能力
        self.TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'
        self.chunk = 1024
        self.NUM_SAMPLES = 2000  # 采样点
        self.channels = 1  # 一个声道
        self.sampwidth = 2  # 两个字节十六位

        self.API_KEY = 'GkegucnW3b559fCPZ8eQOkjK'
        self.SECRET_KEY = 'mhinZuFI05jx2K3dFv8yYWnsPxU93tTT'

        self.TIME = 30  # 条件变量，可以设置定义录音的时间
        self.Level = 600
        self.mute_count_limit = 50
        self.mute_begin = 0
        self.mute_end = 1
        self.not_mute = 0
        self.voice_queue = queue.Queue(1024)
        self.wav_queue = queue.Queue(1024)
        self.file_name_index = 1
        self.thread_flag = 0
        self.start_flag = 1

        # 需要识别的文件
        # AUDIO_FILE = filename  # 只支持 pcm/wav/amr
        # 文件格式
        self.FORMAT = filename[-3:]  # 文件后缀只支持 pcm/wav/amr

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
                             rate = self.RATE, input=True,
                             frames_per_buffer = self.NUM_SAMPLES)
            save_buffer = []
            count = 0
            print('开始录音')
            while count < self.TIME * 20:
                string_audio_data = stream.read(self.NUM_SAMPLES)
                audio_data = np.fromstring(string_audio_data, dtype = np.short)
                large_sample_count = np.sum(audio_data > self.LEVEL)
                print(large_sample_count)
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
                print('...')

                save_buffer = save_buffer[:]
                if save_buffer:
                    if self.file_name_index < 11:
                        pass
                    else:
                        self.file_name_index = 1
                    filename = str(self.file_name_index) + '.wav'
                    self.save_wave_file(filename=filename, data=save_buffer)
                    self.writeQ(queue=self.wav_queue, data=filename)
                    self.file_name_index += 1
                    print(filename + "已经保存")
                else:
                    print("文件未保存")
                # self.save_wave_file(filename, my_buf)
                save_buffer = []
                stream.close()

    # 放音模块
    def read_file(self):
        wf = wave.open(filename, 'rb')
        p = PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(), rate=wf.getframerate(), output=True, )
        print('开始放音')
        while True:
            data = wf.readframes(self.chunk)
            if data == b'': break
            stream.write(data)
            print('...')
        wf.close()
        stream.close()
        p.terminate()

    # 识别模块
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
            print('token http response http code : ' + str(err.code))
            result_str = err.read()
        result_str = result_str.decode()

        print(result_str)
        result = json.loads(result_str)
        print(result)

        if ('access_token' in result.keys() and 'scope' in result.keys()):
            print(self.SCOPE)
            if self.SCOPE and (not self.SCOPE in result['scope'].split(' ')):  # SCOPE = False 忽略检查
                raise DemoError('scope is not correct')
            print('token获取成功: %s  token过期时间: %s' % (result['access_token'], result['expires_in']))
            return result['access_token']
        else:
            raise DemoError(
                'API_KEY或者SECRET_KEY不正确，请重新设置')

    def speech_recognition(self):
        while self.start_flag == 1:
            token = self.fetch_token()
            speech_data = []
            with open(filename, 'rb') as speech_file:
                speech_data = speech_file.read()

            length = len(speech_data)
            if length == 0:
                raise DemoError('file %s length read 0 bytes' % self.AUDIO_FILE)
            speech = base64.b64encode(speech_data)
            speech = str(speech, 'utf-8')
            params = {'dev_pid': self.DEV_PID,
                      'format': self.FORMAT,
                      'rate': self.RATE,
                      'token': token,
                      'cuid': self.CUID,
                      'channel': 1,
                      'speech': speech,
                      'len': length
                      }
            post_data = json.dumps(params, sort_keys=False)
            # print post_data
            req = Request(self.ASR_URL, post_data.encode('utf-8'))
            req.add_header('Content-Type', 'application/json')
            timer = time.perf_counter
            try:
                begin = timer()
                f = urlopen(req)
                result_str = f.read()
                print("请求时间成本  %f" % (timer() - begin))
            except URLError as err:
                print('ASR HTTP响应HTTP代码 : ' + str(err.code))
                result_str = err.read()

            result_str = str(result_str, 'utf-8')
            print(result_str)
            # print(type(result_str))
            my_temp = json.loads(result_str)
            # err = my_temp['err_no']
            # print(my_temp['err_no'])
            if my_temp['err_no']:
                if my_temp['err_no'] == 3300:
                    text = '输入参数不正确'
                    print(text)
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3301:
                    text = '音频质量过差'
                    print(text)
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3302:
                    text = '鉴权失败'
                    print(text)
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3303:
                    text = '语音服务器后端问题'
                    print(text)
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3304:
                    text = '用户的请求QPS超限'
                    print(text)
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3305:
                    text = '用户的日pv（日请求量）超限'
                    print(text)
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3307:
                    text = '语音服务器后端识别出错问题'
                    print(text)
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3308:
                    text = '音频过长'
                    print(text)
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3309:
                    text = '音频数据问题'
                    print(text)
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3310:
                    text = '输入的音频文件过大'
                    print(text)
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3311:
                    text = '采样率rate参数不在选项里'
                    print(text)
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3312:
                    text = '音频格式format参数不在选项里'
                    print(text)
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3313:
                    text = '语音服务器解析超时'
                    print(text)
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3314:
                    text = '音频长度过短'
                    print(text)
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3315:
                    text = '语音服务器处理超时'
                    print(text)
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
                elif my_temp['err_no'] == 3316:
                    text = '音频转为pcm失败'
                    print(text)
                    self.textEdit.append("语音识别出现错误，错误码是： %f,原因是：" % my_temp['err_no'] + text)
            else:
                word = my_temp['result']
                print(word[0])
                with open("result.txt", "w") as of:
                    of.write(result_str)
                    self.textEdit.append(word[0])
                    self.textEdit.append("本次语音识别花费时间%f" % (timer() - begin))
            time.sleep(0.1)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        self.my_record()
        print('录音完成')

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        self.read_file()
        print('放音完成')

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        """
        Slot documentation goes here.
        """
        self.speech_recognition()
        print('识别完成')


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # 加入启动画面
    # splash = QtWidgets.QSplashScreen(QtGui.QPixmap(":/ico/source/icon/1.ico"))
    # splash.show()
    # splash.showMessage("努力加载中(:", QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
    # time.sleep(0.1)
    # splash.showMessage("加载中... 0%", QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
    # time.sleep(0.1)
    # splash.showMessage("加载中... 100%", QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
    # time.sleep(0.2)
    # app.processEvents()
    ui = MainWindow()
    #    ui.setWindowTitle("语音识别")
    #    ui.setStyleSheet("#MainWindow{border-image:url(./pic/source/pic/8.png);}")
    ui.show()
    # splash.finish(ui)
    sys.exit(app.exec_())

