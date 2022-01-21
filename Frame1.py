#Boa:Frame:Frame1

import os
import sys
import time
import threading
import datetime
import json
import traceback
import io

import wx
from wx.adv import TaskBarIcon as wxTaskBarIcon
from wx.adv import EVT_TASKBAR_LEFT_DCLICK

import pyWinhook
import win32con
import win32api
import ctypes
import pyperclip
from playsound import playsound

import config


VERSION = '3.2.2'


wx.NO_3D = 0
HOT_KEYS = ['F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12']

conf = config.getconfig()


def GetMondrianStream():
    data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x06\x00\x00\x00szz\xf4\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00qIDATX\x85\xed\xd6;\n\x800\x10E\xd1{\xc5\x8d\xb9r\x97\x16\x0b\xad$\x8a\x82:\x16o\xda\x84pB2\x1f\x81Fa\x8c\x9c\x08\x04Z{\xcf\xa72\xbcv\xfa\xc5\x08 \x80r\x80\xfc\xa2\x0e\x1c\xe4\xba\xfaX\x1d\xd0\xde]S\x07\x02\xd8>\xe1wa-`\x9fQ\xe9\x86\x01\x04\x10\x00\\(Dk\x1b-\x04\xdc\x1d\x07\x14\x98;\x0bS\x7f\x7f\xf9\x13\x04\x10@\xf9X\xbe\x00\xc9 \x14K\xc1<={\x00\x00\x00\x00IEND\xaeB`\x82'
    stream = io.BytesIO(data)
    return stream


def GetMondrianBitmap():
    stream = GetMondrianStream()
    image = wx.ImageFromStream(stream)
    return wx.BitmapFromImage(image)


def GetMondrianIcon():
    icon = wx.EmptyIcon()
    icon.CopyFromBitmap(GetMondrianBitmap())
    return icon


def create(parent):
    return Frame1(parent)


def current_ts():
    return int(time.time() * 1000)
    

def play_start_sound():
    path = os.path.join(os.getcwd(), 'sounds', 'start.mp3')
    playsound(path)


def play_end_sound():
    path = os.path.join(os.getcwd(), 'sounds', 'end.mp3')
    playsound(path)


[wxID_FRAME1, wxID_FRAME1BTRECORD, wxID_FRAME1BTRUN, wxID_FRAME1BTPAUSE, wxID_FRAME1BUTTON1,
 wxID_FRAME1CHOICE_SCRIPT, wxID_FRAME1CHOICE_START, wxID_FRAME1CHOICE_STOP,
 wxID_FRAME1PANEL1, wxID_FRAME1STATICTEXT1, wxID_FRAME1STATICTEXT2,
 wxID_FRAME1STATICTEXT3, wxID_FRAME1STATICTEXT4, wxID_FRAME1STIMES,
 wxID_FRAME1TEXTCTRL1, wxID_FRAME1TEXTCTRL2, wxID_FRAME1TNUMRD,
 wxID_FRAME1TSTOP, wxID_FRAME1STATICTEXT5, wxID_FRAME1TEXTCTRL3,
] = [wx.NewId() for _init_ctrls in range(20)]


SW = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
SH = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)


class Frame1(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(SW / 2 - 183, SH / 2 - 115.5), size=wx.Size(366, 231),
              style=wx.STAY_ON_TOP | wx.DEFAULT_FRAME_STYLE,
              title='KeymouseGo v%s' % VERSION)
        self.SetClientSize(wx.Size(361, 235))

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1', parent=self,
              pos=wx.Point(0, 0), size=wx.Size(350, 205),
              style=wx.NO_3D | wx.CAPTION)

        self.btrecord = wx.Button(id=wxID_FRAME1BTRECORD, label='录制',
              name='btrecord', parent=self.panel1, pos=wx.Point(213, 12),
              size=wx.Size(56, 32), style=0)
        self.btrecord.Bind(wx.EVT_BUTTON, self.OnBtrecordButton,
              id=wxID_FRAME1BTRECORD)

        self.btrun = wx.Button(id=wxID_FRAME1BTRUN, label='启动',
              name='btrun', parent=self.panel1, pos=wx.Point(285, 12),
              size=wx.Size(56, 32), style=0)
        self.btrun.Bind(wx.EVT_BUTTON, self.OnBtrunButton, id=wxID_FRAME1BTRUN)

        # 暂停/继续 功能不适合用按钮的形式来做，所以暂时隐去
        # self.btpause = wx.Button(id=wxID_FRAME1BTPAUSE, label='暂停',
        #       name='btpause', parent=self.panel1, pos=wx.Point(274, 141),
        #       size=wx.Size(56, 32), style=0)
        # self.btpause.Bind(wx.EVT_BUTTON, self.OnBtpauseButton, id=wxID_FRAME1BTPAUSE)

        self.tnumrd = wx.StaticText(id=wxID_FRAME1TNUMRD, label='ready..',
              name='tnumrd', parent=self.panel1, pos=wx.Point(17, 205),
              size=wx.Size(100, 36), style=0)

        self.button1 = wx.Button(id=wxID_FRAME1BUTTON1, label='test',
              name='button1', parent=self.panel1, pos=wx.Point(128, 296),
              size=wx.Size(75, 24), style=0)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_FRAME1BUTTON1)

        self.tstop = wx.StaticText(id=wxID_FRAME1TSTOP,
              label='If you want to stop it, Press F12', name='tstop',
              parent=self.panel1, pos=wx.Point(25, 332), size=wx.Size(183, 18),
              style=0)
        self.tstop.Show(False)

        self.stimes = wx.SpinCtrl(id=wxID_FRAME1STIMES, initial=0, max=1000,
              min=0, name='stimes', parent=self.panel1, pos=wx.Point(217, 101),
              size=wx.Size(45, 18), style=wx.SP_ARROW_KEYS)
        self.stimes.SetValue(int(conf[2][1]))

        self.label_run_times = wx.StaticText(id=wxID_FRAME1STATICTEXT2,
              label='执行次数(0为无限循环)',
              name='label_run_times', parent=self.panel1, pos=wx.Point(214, 61),
              size=wx.Size(136, 26), style=0)

        self.textCtrl1 = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL1, name='textCtrl1',
              parent=self.panel1, pos=wx.Point(24, 296), size=wx.Size(40, 22),
              style=0, value='119')

        self.textCtrl2 = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL2, name='textCtrl2',
              parent=self.panel1, pos=wx.Point(80, 296), size=wx.Size(36, 22),
              style=0, value='123')

        self.label_script = wx.StaticText(id=wxID_FRAME1STATICTEXT3,
              label='脚本', name='label_script', parent=self.panel1,
              pos=wx.Point(17, 20), size=wx.Size(40, 32), style=0)

        self.choice_script = wx.Choice(choices=[], id=wxID_FRAME1CHOICE_SCRIPT,
              name='choice_script', parent=self.panel1, pos=wx.Point(90, 15),
              size=wx.Size(108, 25), style=0)

        self.label_start_key = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label='启动/暂停热键', name='label_start_key',
              parent=self.panel1, pos=wx.Point(16, 55), size=wx.Size(56, 36),
              style=0)

        self.label_stop_key = wx.StaticText(id=wxID_FRAME1STATICTEXT4,
              label='终止热键', name='label_stop_key',
              parent=self.panel1, pos=wx.Point(16, 102), size=wx.Size(56, 32),
              style=0)

        self.choice_start = wx.Choice(choices=[], id=wxID_FRAME1CHOICE_START,
              name='choice_start', parent=self.panel1, pos=wx.Point(90, 58),
              size=wx.Size(108, 25), style=0)
        self.choice_start.SetLabel('')
        self.choice_start.SetLabelText('')
        self.choice_start.Bind(wx.EVT_CHOICE, self.OnChoice_startChoice,
              id=wxID_FRAME1CHOICE_START)

        self.choice_stop = wx.Choice(choices=[], id=wxID_FRAME1CHOICE_STOP,
              name='choice_stop', parent=self.panel1, pos=wx.Point(90, 98),
              size=wx.Size(108, 25), style=0)
        self.choice_stop.Bind(wx.EVT_CHOICE, self.OnChoice_stopChoice,
              id=wxID_FRAME1CHOICE_STOP)

        self.label_mouse_interval = wx.StaticText(
              label='鼠标精度', name='label_mouse_interval',
              parent=self.panel1, pos=wx.Point(16, 141), size=wx.Size(56, 32),
              style=0)

        self.mouse_move_interval_ms = wx.SpinCtrl(initial=int(conf[3][1]), max=999999,
              min=0, name='mouse_move_interval_ms', parent=self.panel1, pos=wx.Point(90, 141),
              size=wx.Size(68, 18), style=wx.SP_ARROW_KEYS)

        self.label_mouse_interval_tips = wx.StaticText(
              label='数值越小鼠标轨迹越精准，为 0 则不记录', name='label_mouse_interval_tips',
              parent=self.panel1, pos=wx.Point(171, 140), size=wx.Size(150, 50),
              style=0)

        self.label_execute_speed = wx.StaticText(
              label='执行速度(%)', name='label_execute_speed',
              parent=self.panel1, pos=wx.Point(16, 176), size=wx.Size(70, 32),
              style=0)

        self.execute_speed = wx.SpinCtrl(initial=int(conf[4][1]), max=500,
              min=20, name='execute_speed', parent=self.panel1,
              pos=wx.Point(90, 176),
              size=wx.Size(68, 18), style=wx.SP_ARROW_KEYS)

        self.label_execute_speed_tips = wx.StaticText(
            label='范围(20%-500%)', name='label_execute_speed_tips',
            parent=self.panel1, pos=wx.Point(171, 176), size=wx.Size(150, 50),
            style=0)
        # ===== if use SetProcessDpiAwareness, comment below =====
        # self.label_scale = wx.StaticText(id=wxID_FRAME1STATICTEXT5,
        #       label='屏幕缩放', name='staticText5',
        #       parent=self.panel1, pos=wx.Point(16, 141), size=wx.Size(56, 32),
        #       style=0)
        # self.text_scale = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL3, name='textCtrl3',
        #       parent=self.panel1, pos=wx.Point(79, 138), size=wx.Size(108, 22),
        #       style=0, value='100%')
        # =========================================================

    def __init__(self, parent):

        self._init_ctrls(parent)

        self.SetIcon(GetMondrianIcon())
        self.taskBarIcon = TaskBarIcon(self)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_ICONIZE, self.OnIconfiy)

        if not os.path.exists('scripts'):
            os.mkdir('scripts')
        self.scripts = os.listdir('scripts')[::-1]

        self.scripts = list(filter(lambda s: s.endswith('.txt'), self.scripts))
        self.choice_script.SetItems(self.scripts)
        if self.scripts:
            self.choice_script.SetSelection(0)

        self.choice_start.SetItems(HOT_KEYS)
        self.choice_start.SetSelection(int(conf[0][1]))

        self.choice_stop.SetItems(HOT_KEYS)
        self.choice_stop.SetSelection(int(conf[1][1]))

        self.running = False
        self.recording = False
        self.record = []
        self.ttt = current_ts()

        # for pause-resume feature
        self.paused = False
        self.pause_event = threading.Event()

        self.hm = pyWinhook.HookManager()

        def on_mouse_event(event):

            # print('MessageName:',event.MessageName)  #事件名称
            # print('Message:',event.Message)          #windows消息常量 
            # print('Time:',event.Time)                #事件发生的时间戳        
            # print('Window:',event.Window)            #窗口句柄         
            # print('WindowName:',event.WindowName)    #窗口标题
            # print('Position:',event.Position)        #事件发生时相对于整个屏幕的坐标
            # print('Wheel:',event.Wheel)              #鼠标滚轮
            # print('Injected:',event.Injected)        #判断这个事件是否由程序方式生成，而不是正常的人为触发。
            # print('---')

            if not self.recording or self.running:
                return True

            message = event.MessageName
            if message == 'mouse wheel':
                message += ' up' if event.Wheel == 1 else ' down'
            all_messages = ('mouse left down', 'mouse left up', 'mouse right down', 'mouse right up', 'mouse move',
                            'mouse middle down', 'mouse middle up', 'mouse wheel up', 'mouse wheel down')
            if message not in all_messages:
                return True

            pos = win32api.GetCursorPos()

            delay = current_ts() - self.ttt

            # 录制鼠标轨迹的精度，数值越小越精准，但同时可能产生大量的冗余
            mouse_move_interval_ms = self.mouse_move_interval_ms.Value or 999999

            if message == 'mouse move' and delay < mouse_move_interval_ms:
                return True

            self.ttt = current_ts()
            if not self.record:
                delay = 0

            x, y = pos
            tx = x / SW
            ty = y / SH
            tpos = (tx, ty)

            print(delay, message, tpos)

            self.record.append([delay, 'EM', message, tpos])
            text = self.tnumrd.GetLabel()
            action_count = text.replace(' actions recorded', '')
            text = '%d actions recorded' % (int(action_count) + 1)
            self.tnumrd.SetLabel(text)
            return True

        def on_keyboard_event(event):

            # print('MessageName:',event.MessageName)          #同上，共同属性不再赘述
            # print('Message:',event.Message)
            # print('Time:',event.Time)
            # print('Window:',event.Window)
            # print('WindowName:',event.WindowName)
            # print('Ascii:', event.Ascii, chr(event.Ascii))   #按键的ASCII码
            # print('Key:', event.Key)                         #按键的名称
            # print('KeyID:', event.KeyID)                     #按键的虚拟键值
            # print('ScanCode:', event.ScanCode)               #按键扫描码
            # print('Extended:', event.Extended)               #判断是否为增强键盘的扩展键
            # print('Injected:', event.Injected)
            # print('Alt', event.Alt)                          #是某同时按下Alt
            # print('Transition', event.Transition)            #判断转换状态
            # print('---')

            message = event.MessageName
            message = message.replace(' sys ', ' ')

            if message == 'key up' and not self.recording:
                # listen for start/stop script
                key_name = event.Key.lower()
                # start_name = 'f6'  # as default
                # stop_name = 'f9'  # as default

                start_index = self.choice_start.GetSelection()
                stop_index = self.choice_stop.GetSelection()
                # Predict potential conflict
                if start_index == stop_index:
                    stop_index = (stop_index + 1) % len(HOT_KEYS)
                    self.choice_stop.SetSelection(stop_index)
                start_name = HOT_KEYS[start_index].lower()
                stop_name = HOT_KEYS[stop_index].lower()

                if key_name == start_name and not self.running:
                    print('script start')
                    t = RunScriptClass(self, self.pause_event)
                    t.start()
                    print(key_name, 'host start')
                elif key_name == start_name and self.running:
                    if self.paused:
                        print('script resume')
                        self.paused = False
                        self.pause_event.set()
                        print(key_name, 'host resume')
                    else:
                        print('script pause')
                        self.paused = True
                        self.pause_event.clear()
                        print(key_name, 'host pause')
                elif key_name == stop_name and self.running:
                    print('script stop')
                    self.tnumrd.SetLabel('broken')
                    print(key_name, 'host stop')

            if not self.recording or self.running:
                return True

            all_messages = ('key down', 'key up')
            if message not in all_messages:
                return True

            key_info = (event.KeyID, event.Key, event.Extended)

            delay = current_ts() - self.ttt
            self.ttt = current_ts()
            if not self.record:
                delay = 0

            print(delay, message, key_info)

            self.record.append([delay, 'EK', message, key_info])
            text = self.tnumrd.GetLabel()
            action_count = text.replace(' actions recorded', '')
            text = '%d actions recorded' % (int(action_count) + 1)
            self.tnumrd.SetLabel(text)
            return True

        self.hm.MouseAll = on_mouse_event
        self.hm.KeyAll = on_keyboard_event
        self.hm.HookMouse()
        self.hm.HookKeyboard()

    def get_script_path(self):
        i = self.choice_script.GetSelection()
        if i < 0:
            return ''
        script = self.scripts[i]
        path = os.path.join(os.getcwd(), 'scripts', script)
        print(path)
        return path

    def new_script_path(self):
        now = datetime.datetime.now()
        script = '%s.txt' % now.strftime('%m%d_%H%M')
        if script in self.scripts:
            script = '%s.txt' % now.strftime('%m%d_%H%M%S')
        self.scripts.insert(0, script)
        self.choice_script.SetItems(self.scripts)
        self.choice_script.SetSelection(0)
        return self.get_script_path()

    def OnHide(self, event):
        self.Hide()
        event.Skip()

    def OnIconfiy(self, event):
        self.Hide()
        event.Skip()

    def OnClose(self, event):
        config.saveconfig(newStartIndex=self.choice_start.GetSelection(),
                          newStopIndex=self.choice_stop.GetSelection(),
                          newTimes=self.stimes.GetValue(),
                          newPrecsion=self.mouse_move_interval_ms.GetValue(),
                          newSpeed=self.execute_speed.GetValue())
        self.taskBarIcon.Destroy()
        self.Destroy()
        event.Skip()

    def OnButton1Button(self, event):
        event.Skip()

    def OnBtrecordButton(self, event):

        if self.recording:
            print('record stop')
            self.recording = False
            self.record = self.record[:-2]
            output = json.dumps(self.record, indent=1)
            output = output.replace('\r\n', '\n').replace('\r', '\n')
            output = output.replace('\n   ', '').replace('\n  ', '')
            output = output.replace('\n ]', ']')
            open(self.new_script_path(), 'w').write(output)
            self.btrecord.SetLabel('录制')
            self.tnumrd.SetLabel('finished')
            self.record = []
        else:
            print('record start')
            self.recording = True
            self.ttt = current_ts()
            status = self.tnumrd.GetLabel()
            if 'running' in status or 'recorded' in status:
                return
            self.btrecord.SetLabel('结束') # 结束
            self.tnumrd.SetLabel('0 actions recorded')
            self.choice_script.SetSelection(-1)
            self.record = []

        event.Skip()

    def OnBtrunButton(self, event):
        print('script start by btn')
        t = RunScriptClass(self, self.pause_event)
        t.start()
        event.Skip()

    def OnBtpauseButton(self, event):
        print('script pause button pressed')
        if self.paused:
            print('script is resumed')
            self.pause_event.set()
            self.paused = False
            self.btpause.SetLabel('暂停')
        else:
            print('script is paused')
            self.pause_event.clear()
            self.paused = True
            self.btpause.SetLabel('继续')
        event.Skip()

    def OnChoice_startChoice(self, event):
        event.Skip()

    def OnChoice_stopChoice(self, event):
        event.Skip()


class RunScriptClass(threading.Thread):

    def __init__(self, frame: Frame1, event: threading.Event):
        self.frame = frame
        self.event = event
        self.event.set()
        super(RunScriptClass, self).__init__()

    def run(self):

        status = self.frame.tnumrd.GetLabel()
        if self.frame.running or self.frame.recording:
            return

        if 'running' in status or 'recorded' in status:
            return

        script_path = self.frame.get_script_path()
        if not script_path:
            self.frame.tnumrd.SetLabel('script not found, please self.record first!')
            return

        self.frame.running = True

        try:
            self.run_times = self.frame.stimes.Value
            self.running_text = '%s running..' % script_path.split('/')[-1].split('\\')[-1]
            self.frame.tnumrd.SetLabel(self.running_text)
            self.frame.tstop.Shown = True
            self.run_speed = self.frame.execute_speed.Value

            self.j = 0
            play_start_sound()
            while self.j < self.run_times or self.run_times == 0:
                self.j += 1
                current_status = self.frame.tnumrd.GetLabel()
                if  current_status in ['broken', 'finished']:
                    self.frame.running = False
                    break
                RunScriptClass.run_script_once(script_path, thd=self)

            self.frame.tnumrd.SetLabel('finished')
            self.frame.tstop.Shown = False
            self.frame.running = False
            play_end_sound()
            print('script run finish!')

        except Exception as e:
            print('run error', e)
            traceback.print_exc()
            self.frame.tnumrd.SetLabel('failed')
            self.frame.tstop.Shown = False
            self.frame.running = False


    @classmethod
    def run_script_once(cls, script_path, thd=None):

        content = ''

        lines = []

        try:
            lines = open(script_path, 'r', encoding='utf8').readlines()
        except Exception as e:
            print(e)
            try:
                lines = open(script_path, 'r', encoding='gbk').readlines()
            except Exception as e:
                print(e)

        for line in lines:
            # 去注释
            if '//' in line:
                index = line.find('//')
                line = line[:index]
            # 去空字符
            line = line.strip()
            content += line

        # 去最后一个元素的逗号（如有）
        content = content.replace('],\n]', ']\n]').replace('],]', ']]')

        print(content)
        s = json.loads(content)
        steps = len(s)

        for i in range(steps):

            print(s[i])

            delay = s[i][0] / (thd.run_speed/100)
            event_type = s[i][1].upper()
            message = s[i][2].lower()
            action = s[i][3]

            time.sleep(delay / 1000.0)

            if thd:
                current_status = thd.frame.tnumrd.GetLabel()
                if current_status in ['broken', 'finished']:
                    break
                thd.event.wait()
                text = '%s  [%d/%d %d/%d] %d%%' % (thd.running_text, i+1, steps, thd.j, thd.run_times, thd.run_speed)
                thd.frame.tnumrd.SetLabel(text)

            if event_type == 'EM':
                x, y = action

                if action == [-1, -1]:
                    # 约定 [-1, -1] 表示鼠标保持原位置不动
                    pass
                else:
                    # 挪动鼠标 普通做法
                    # ctypes.windll.user32.SetCursorPos(x, y)
                    # or
                    # win32api.SetCursorPos([x, y])

                    # 更好的兼容 win10 屏幕缩放问题
                    nx = int((x * SW) * 65535 / SW)
                    ny = int((y * SH) * 65535 / SH)
                    win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_MOVE, nx, ny, 0, 0)

                if message == 'mouse left down':
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                elif message == 'mouse left up':
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                elif message == 'mouse right down':
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                elif message == 'mouse right up':
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                elif message == 'mouse middle down':
                    win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)
                elif message == 'mouse middle up':
                    win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)
                elif message == 'mouse wheel up':
                    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, 120, 0)
                elif message == 'mouse wheel down':
                    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -120, 0)
                elif message == 'mouse move':
                    pass
                else:
                    print('unknow mouse event:', message)

            elif event_type == 'EK':
                key_code, key_name, extended = action

                # shift ctrl alt
                # if key_code >= 160 and key_code <= 165:
                #     key_code = int(key_code/2) - 64

                base = 0
                if extended:
                    base = win32con.KEYEVENTF_EXTENDEDKEY

                if message == 'key down':
                    win32api.keybd_event(key_code, 0, base, 0)
                elif message == 'key up':
                    win32api.keybd_event(key_code, 0, base | win32con.KEYEVENTF_KEYUP, 0)
                else:
                    print('unknow keyboard event:', message)

            elif event_type == 'EX':

                if message == 'input':
                    text = action
                    pyperclip.copy(text)
                    # Ctrl+V
                    win32api.keybd_event(162, 0, 0, 0)  # ctrl
                    win32api.keybd_event(86, 0, 0, 0)  # v
                    win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)
                    win32api.keybd_event(162, 0, win32con.KEYEVENTF_KEYUP, 0)
                else:
                    print('unknow extra event:', message)


class TaskBarIcon(wxTaskBarIcon):
    ID_About = wx.NewId()
    ID_Closeshow = wx.NewId()

    def __init__(self, frame):
        wxTaskBarIcon.__init__(self)
        self.frame = frame
        self.SetIcon(GetMondrianIcon())
        self.Bind(EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarLeftDClick)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=self.ID_About)
        self.Bind(wx.EVT_MENU, self.OnCloseshow, id=self.ID_Closeshow)

    def OnTaskBarLeftDClick(self, event):
        if self.frame.IsIconized():
            self.frame.Iconize(False)
        if not self.frame.IsShown():
            self.frame.Show(True)
        self.frame.Raise()

    def OnAbout(self, event):
        wx.MessageBox('https://github.com/taojy123/KeymouseGo', 'KeymouseGo v%s' % VERSION)
        event.Skip()

    def OnCloseshow(self, event):
        self.frame.Close(True)
        event.Skip()

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(self.ID_About, 'About')
        menu.Append(self.ID_Closeshow, 'Exit')
        return menu

