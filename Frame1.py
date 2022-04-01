# cython: language_level=3
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
import win32con, win32print
import win32api, win32gui
import ctypes
import pyperclip
from playsound import playsound
from playsound import PlaysoundException
import re

import i18n
import config


VERSION = '3.3'


wx.NO_3D = 0
HOT_KEYS = ['F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12']

conf = config.getconfig()
i18n.load_path.append('i18n')
i18n.set('locale', conf['language'])
ID_MAP = {'zh-cn':0, 'en':1}
RID_MAP = {0:'zh-cn', 1:'en'}

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
    

[wxID_FRAME1, wxID_FRAME1BTRECORD, wxID_FRAME1BTRUN, wxID_FRAME1BTPAUSE, wxID_FRAME1BUTTON1,
 wxID_FRAME1CHOICE_SCRIPT, wxID_FRAME1CHOICE_START, wxID_FRAME1CHOICE_STOP, wxID_FRAME1CHOICE_RECORD,
 wxID_FRAME1PANEL1, wxID_FRAME1STATICTEXT1, wxID_FRAME1STATICTEXT2,
 wxID_FRAME1STATICTEXT3, wxID_FRAME1STATICTEXT4, wxID_FRAME1STIMES,
 wxID_FRAME1TEXTCTRL1, wxID_FRAME1TEXTCTRL2, wxID_FRAME1TNUMRD,
 wxID_FRAME1TSTOP, wxID_FRAME1STATICTEXT5, wxID_FRAME1TEXTCTRL3,
 wxID_LANGUAGECHOICE
] = [wx.NewId() for _init_ctrls in range(22)]


# SW = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
# SH = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
hDC = win32gui.GetDC(0)
SW = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
SH = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)


class Frame1(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(SW / 2 - 183, SH / 2 - 115.5), size=wx.Size(366, 271),
              style=wx.STAY_ON_TOP | wx.DEFAULT_FRAME_STYLE,
              title='KeymouseGo v%s' % VERSION)
        self.SetClientSize(self.FromDIP(wx.Size(361, 270)))

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1', parent=self,
              pos=self.FromDIP(wx.Point(0, 0)), size=self.FromDIP(wx.Size(350, 245)),
              style=wx.NO_3D | wx.CAPTION)

        self.btrecord = wx.Button(id=wxID_FRAME1BTRECORD, label=i18n.t('lang.record'),
              name='btrecord', parent=self.panel1, pos=self.FromDIP(wx.Point(213, 12)),
              size=self.FromDIP(wx.Size(56, 32)), style=0)
        self.btrecord.Bind(wx.EVT_BUTTON, self.OnBtrecordButton,
              id=wxID_FRAME1BTRECORD)

        self.btrun = wx.Button(id=wxID_FRAME1BTRUN, label=i18n.t('lang.launch'),
              name='btrun', parent=self.panel1, pos=self.FromDIP(wx.Point(285, 12)),
              size=self.FromDIP(wx.Size(56, 32)), style=0)
        self.btrun.Bind(wx.EVT_BUTTON, self.OnBtrunButton, id=wxID_FRAME1BTRUN)

        # 暂停/继续 功能不适合用按钮的形式来做，所以暂时隐去
        # self.btpause = wx.Button(id=wxID_FRAME1BTPAUSE, label='暂停',
        #       name='btpause', parent=self.panel1, pos=self.FromDIP(wx.Point(274, 141)),
        #       size=self.FromDIP(wx.Size(56, 32)), style=0)
        # self.btpause.Bind(wx.EVT_BUTTON, self.OnBtpauseButton, id=wxID_FRAME1BTPAUSE)

        # 暂停录制
        self.btpauserecord = wx.Button(id=wxID_FRAME1BTPAUSE, label=i18n.t('lang.pauserecord'),
               name='btpauserecording', parent=self.panel1, pos=self.FromDIP(wx.Point(213, 135)),
               size=self.FromDIP(wx.Size(86, 32)), style=0)
        self.btpauserecord.Bind(wx.EVT_BUTTON, self.OnPauseRecordButton, id=wxID_FRAME1BTPAUSE)
        self.btpauserecord.Enable(False)

        self.tnumrd = wx.StaticText(id=wxID_FRAME1TNUMRD, label='ready..',
              name='tnumrd', parent=self.panel1, pos=self.FromDIP(wx.Point(17, 245)),
              size=self.FromDIP(wx.Size(100, 36)), style=0)

        self.button1 = wx.Button(id=wxID_FRAME1BUTTON1, label='test',
              name='button1', parent=self.panel1, pos=self.FromDIP(wx.Point(128, 296)),
              size=self.FromDIP(wx.Size(75, 24)), style=0)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_FRAME1BUTTON1)

        self.tstop = wx.StaticText(id=wxID_FRAME1TSTOP,
              label='If you want to stop it, Press F12', name='tstop',
              parent=self.panel1, pos=self.FromDIP(wx.Point(25, 332)), size=self.FromDIP(wx.Size(183, 18)),
              style=0)
        self.tstop.Show(False)

        self.stimes = wx.SpinCtrl(id=wxID_FRAME1STIMES, initial=0, max=1000,
              min=0, name='stimes', parent=self.panel1, pos=self.FromDIP(wx.Point(217, 101)),
              size=self.FromDIP(wx.Size(45, 18)), style=wx.SP_ARROW_KEYS)
        self.stimes.SetValue(int(conf['looptimes']))

        self.label_run_times = wx.StaticText(id=wxID_FRAME1STATICTEXT2,
              label=i18n.t('lang.tip'),
              name='label_run_times', parent=self.panel1, pos=self.FromDIP(wx.Point(214, 57)),
              size=self.FromDIP(wx.Size(146, 36)), style=0)

        self.textCtrl1 = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL1, name='textCtrl1',
              parent=self.panel1, pos=self.FromDIP(wx.Point(24, 296)), size=self.FromDIP(wx.Size(40, 22)),
              style=0, value='119')

        self.textCtrl2 = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL2, name='textCtrl2',
              parent=self.panel1, pos=self.FromDIP(wx.Point(80, 296)), size=self.FromDIP(wx.Size(36, 22)),
              style=0, value='123')

        self.label_script = wx.StaticText(id=wxID_FRAME1STATICTEXT3,
              label=i18n.t('lang.script'), name='label_script', parent=self.panel1,
              pos=self.FromDIP(wx.Point(17, 20)), size=self.FromDIP(wx.Size(40, 32)), style=0)

        self.choice_script = wx.Choice(choices=[], id=wxID_FRAME1CHOICE_SCRIPT,
              name='choice_script', parent=self.panel1, pos=self.FromDIP(wx.Point(100, 15)),
              size=self.FromDIP(wx.Size(108, 25)), style=0)

        self.label_start_key = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label=i18n.t('lang.launchhotkey'), name='label_start_key',
              parent=self.panel1, pos=self.FromDIP(wx.Point(16, 61)), size=self.FromDIP(wx.Size(80, 36)),
              style=0)

        self.label_stop_key = wx.StaticText(id=wxID_FRAME1STATICTEXT4,
              label=i18n.t('lang.terminatehotkey'), name='label_stop_key',
              parent=self.panel1, pos=self.FromDIP(wx.Point(16, 102)), size=self.FromDIP(wx.Size(76, 32)),
              style=0)

        self.label_record_key = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label=i18n.t('lang.recordhotkey'), name='label_record_key',
              parent=self.panel1, pos=self.FromDIP(wx.Point(16, 141)),
              size=self.FromDIP(wx.Size(80, 36)),
              style=0)

        self.choice_start = wx.Choice(choices=[], id=wxID_FRAME1CHOICE_START,
              name='choice_start', parent=self.panel1, pos=self.FromDIP(wx.Point(100, 58)),
              size=self.FromDIP(wx.Size(108, 25)), style=0)
        self.choice_start.SetLabel('')
        self.choice_start.SetLabelText('')
        self.choice_start.Bind(wx.EVT_CHOICE, self.OnChoice_startChoice,
              id=wxID_FRAME1CHOICE_START)

        self.choice_stop = wx.Choice(choices=[], id=wxID_FRAME1CHOICE_STOP,
              name='choice_stop', parent=self.panel1, pos=self.FromDIP(wx.Point(100, 98)),
              size=self.FromDIP(wx.Size(108, 25)), style=0)
        self.choice_stop.Bind(wx.EVT_CHOICE, self.OnChoice_stopChoice,
              id=wxID_FRAME1CHOICE_STOP)

        self.choice_record = wx.Choice(choices=[], id=wxID_FRAME1CHOICE_RECORD,
              name='choice_record', parent=self.panel1, pos=self.FromDIP(wx.Point(100, 138)),
              size=self.FromDIP(wx.Size(108, 25)), style=0)
        self.choice_record.Bind(wx.EVT_CHOICE, self.OnChoice_recordChoice,
              id=wxID_FRAME1CHOICE_RECORD)

        self.label_mouse_interval = wx.StaticText(
              label=i18n.t('lang.precision'), name='label_mouse_interval',
              parent=self.panel1, pos=self.FromDIP(wx.Point(16, 181)), size=self.FromDIP(wx.Size(56, 32)),
              style=0)

        self.mouse_move_interval_ms = wx.SpinCtrl(initial=int(conf['precision']), max=999999,
              min=0, name='mouse_move_interval_ms', parent=self.panel1, pos=self.FromDIP(wx.Point(100, 181)),
              size=self.FromDIP(wx.Size(68, 18)), style=wx.SP_ARROW_KEYS)

        self.label_mouse_interval_tips = wx.StaticText(
              label=i18n.t('lang.tip2'), name='label_mouse_interval_tips',
              parent=self.panel1, pos=self.FromDIP(wx.Point(171, 180)), size=self.FromDIP(wx.Size(170, 60)),
              style=0)

        self.label_execute_speed = wx.StaticText(
              label=i18n.t('lang.speed'), name='label_execute_speed',
              parent=self.panel1, pos=self.FromDIP(wx.Point(16, 216)), size=self.FromDIP(wx.Size(70, 32)),
              style=0)

        self.execute_speed = wx.SpinCtrl(initial=int(conf['executespeed']), max=500,
              min=20, name='execute_speed', parent=self.panel1,
              pos=self.FromDIP(wx.Point(100, 216)),
              size=self.FromDIP(wx.Size(68, 18)), style=wx.SP_ARROW_KEYS)

        self.label_execute_speed_tips = wx.StaticText(
            label=i18n.t('lang.range'), name='label_execute_speed_tips',
            parent=self.panel1, pos=self.FromDIP(wx.Point(171, 216)), size=self.FromDIP(wx.Size(120, 20)),
            style=0)

        self.label_language = wx.StaticText(
            label=i18n.t('lang.language'), style=wx.ALIGN_RIGHT,
            parent=self.panel1, pos=self.FromDIP(wx.Point(120, 245)), size=self.FromDIP(wx.Size(150, 50)),
            )

        self.choice_language = wx.Choice(choices=['简体中文', 'English'], id=wxID_LANGUAGECHOICE,
            parent=self.panel1, pos=self.FromDIP(wx.Point(281, 240)),
            size=self.FromDIP(wx.Size(70, 25)), style=0)
        self.choice_language.SetSelection(ID_MAP[conf['language']])

        # ===== if use SetProcessDpiAwareness, comment below =====
        # self.label_scale = wx.StaticText(id=wxID_FRAME1STATICTEXT5,
        #       label='屏幕缩放', name='staticText5',
        #       parent=self.panel1, pos=self.FromDIP(wx.Point(16, 141)), size=self.FromDIP(wx.Size(56, 32)),
        #       style=0)
        # self.text_scale = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL3, name='textCtrl3',
        #       parent=self.panel1, pos=self.FromDIP(wx.Point(79, 138)), size=self.FromDIP(wx.Size(108, 22)),
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
        self.choice_start.SetSelection(int(conf['starthotkeyindex']))

        self.choice_stop.SetItems(HOT_KEYS)
        self.choice_stop.SetSelection(int(conf['stophotkeyindex']))

        self.choice_record.SetItems(HOT_KEYS)
        self.choice_record.SetSelection(int(conf['recordhotkeyindex']))

        self.running = False
        self.recording = False
        self.record = []
        self.ttt = current_ts()

        # for pause-resume feature
        self.paused = False
        self.pause_event = threading.Event()

        # Pause-Resume Record
        self.pauserecord = False

        self.actioncount = 0

        # For better thread control
        self.runthread = None
        self.isbrokenorfinish = True

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

            if not self.recording or self.running or self.pauserecord:
                return True

            message = event.MessageName
            if message == 'mouse wheel':
                message += ' up' if event.Wheel == 1 else ' down'
            elif message in config.swapmousemap and config.swapmousebuttons:
                message = config.swapmousemap[message]
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

            # self.record.append([delay, 'EM', message, tpos])
            self.record.append([delay, 'EM', message, ['{0}%'.format(tx), '{0}%'.format(ty)]])
            self.actioncount = self.actioncount + 1
            text = '%d actions recorded' % self.actioncount

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

            if message == 'key up':
                # listen for start/stop script
                key_name = event.Key.lower()
                # start_name = 'f6'  # as default
                # stop_name = 'f9'  # as default

                start_index = self.choice_start.GetSelection()
                stop_index = self.choice_stop.GetSelection()
                record_index = self.choice_record.GetSelection()

                # Predict potential conflict
                if start_index == stop_index:
                    stop_index = (stop_index + 1) % len(HOT_KEYS)
                    self.choice_stop.SetSelection(stop_index)
                if start_index == record_index:
                    record_index = (record_index + 1) % len(HOT_KEYS)
                    if record_index == stop_index:
                        record_index = (record_index + 1) % len(HOT_KEYS)
                    self.choice_record.SetSelection(record_index)
                start_name = HOT_KEYS[start_index].lower()
                stop_name = HOT_KEYS[stop_index].lower()
                record_name = HOT_KEYS[record_index].lower()

                if key_name == start_name and not self.running and not self.recording:
                    print('script start')
                    # t = RunScriptClass(self, self.pause_event)
                    # t.start()
                    self.runthread = RunScriptClass(self, self.pause_event)
                    self.runthread.start()
                    self.isbrokenorfinish = False
                    print(key_name, 'host start')
                elif key_name == start_name and self.running and not self.recording:
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
                elif key_name == stop_name and self.running and not self.recording:
                    print('script stop')
                    self.tnumrd.SetLabel('broken')
                    self.isbrokenorfinish = True
                    if self.paused:
                        self.paused = False
                        self.pause_event.set()
                    print(key_name, 'host stop')
                elif key_name == stop_name and self.recording:
                    self.recordMethod()
                    print(key_name, 'host stop record')
                elif key_name == record_name:
                    if not self.recording:
                        self.recordMethod()
                        print(key_name, 'host start record')
                    else:
                        self.pauseRecordMethod()
                        print(key_name, 'host pause record')

            if not self.recording or self.running or self.pauserecord:
                return True

            all_messages = ('key down', 'key up')
            if message not in all_messages:
                return True

            # 不录制热键
            hot_keys = [HOT_KEYS[self.choice_start.GetSelection()],
                        HOT_KEYS[self.choice_stop.GetSelection()],
                        HOT_KEYS[self.choice_record.GetSelection()]]
            if event.Key in hot_keys:
                return True

            key_info = (event.KeyID, event.Key, event.Extended)

            delay = current_ts() - self.ttt
            self.ttt = current_ts()
            if not self.record:
                delay = 0

            print(delay, message, key_info)

            self.record.append([delay, 'EK', message, key_info])
            self.actioncount = self.actioncount + 1
            text = '%d actions recorded' % self.actioncount
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
        config.saveconfig({
            'starthotkeyindex':self.choice_start.GetSelection(),
            'stophotkeyindex':self.choice_stop.GetSelection(),
            'recordhotkeyindex': self.choice_record.GetSelection(),
            'looptimes':self.stimes.GetValue(),
            'precision':self.mouse_move_interval_ms.GetValue(),
            'executespeed':self.execute_speed.GetValue(),
            'language':RID_MAP[self.choice_language.GetSelection()]
            })
        self.taskBarIcon.Destroy()
        self.Destroy()
        event.Skip()

    def OnButton1Button(self, event):
        event.Skip()

    def pauseRecordMethod(self):
        if self.pauserecord:
            print('record resume')
            self.pauserecord = False
            self.btpauserecord.SetLabel(i18n.t('lang.pauserecord'))
        else:
            print('record pause')
            self.pauserecord = True
            self.btpauserecord.SetLabel(i18n.t('lang.continuerecord'))
            self.tnumrd.SetLabel('record paused')

    def OnPauseRecordButton(self, event):
        self.pauseRecordMethod()
        event.Skip()

    def recordMethod(self):
        if self.recording:
            print('record stop')
            self.recording = False
            self.record = self.record[:-2]
            output = json.dumps(self.record, indent=1)
            output = output.replace('\r\n', '\n').replace('\r', '\n')
            output = output.replace('\n   ', '').replace('\n  ', '')
            output = output.replace('\n ]', ']')
            open(self.new_script_path(), 'w').write(output)
            self.btrecord.SetLabel(i18n.t('lang.record'))
            self.tnumrd.SetLabel('finished')
            self.record = []
            self.btpauserecord.Enable(False)
            self.btrun.Enable(True)
            self.actioncount = 0
            self.pauserecord = False
            self.btpauserecord.SetLabel(i18n.t('lang.pauserecord'))
        else:
            print('record start')
            self.recording = True
            self.ttt = current_ts()
            status = self.tnumrd.GetLabel()
            if 'running' in status or 'recorded' in status:
                return
            self.btrecord.SetLabel(i18n.t('lang.finish'))  # 结束
            self.tnumrd.SetLabel('0 actions recorded')
            self.choice_script.SetSelection(-1)
            self.record = []
            self.btpauserecord.Enable(True)
            self.btrun.Enable(False)

    def OnBtrecordButton(self, event):
        self.recordMethod()
        event.Skip()

    def OnBtrunButton(self, event):
        print('script start by btn')
        # t = RunScriptClass(self, self.pause_event)
        # t.start()
        self.runthread = RunScriptClass(self, self.pause_event)
        self.runthread.start()
        self.isbrokenorfinish = False
        event.Skip()

    def OnBtpauseButton(self, event):
        print('script pause button pressed')
        if self.paused:
            print('script is resumed')
            self.pause_event.set()
            self.paused = False
            self.btpause.SetLabel(i18n.t('lang.pause'))
        else:
            print('script is paused')
            self.pause_event.clear()
            self.paused = True
            self.btpause.SetLabel(i18n.t('lang.continue'))
        event.Skip()

    def OnChoice_startChoice(self, event):
        event.Skip()

    def OnChoice_stopChoice(self, event):
        event.Skip()

    def OnChoice_recordChoice(self, event):
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

        self.frame.btrun.Enable(False)
        self.frame.btrecord.Enable(False)

        try:
            self.run_times = self.frame.stimes.Value
            self.running_text = '%s running..' % script_path.split('/')[-1].split('\\')[-1]
            self.frame.tnumrd.SetLabel(self.running_text)
            self.frame.tstop.Shown = True
            self.run_speed = self.frame.execute_speed.Value

            self.j = 0
            while self.j < self.run_times or self.run_times == 0:
                self.j += 1
                current_status = self.frame.tnumrd.GetLabel()
                if  current_status in ['broken', 'finished']:
                    self.frame.running = False
                    break
                RunScriptClass.run_script_once(script_path, self.j, thd=self)

            self.frame.tnumrd.SetLabel('finished')
            self.frame.tstop.Shown = False
            self.frame.running = False
            PlayPromptTone.play_end_sound()
            print('script run finish!')

        except Exception as e:
            print('run error', e)
            traceback.print_exc()
            self.frame.tnumrd.SetLabel('failed')
            self.frame.tstop.Shown = False
            self.frame.running = False
        finally:
            self.frame.btrun.Enable(True)
            self.frame.btrecord.Enable(True)

    @classmethod
    def run_script_once(cls, script_path, step, thd=None):

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

            if 1 == step and 0 == i:
                play = PlayPromptTone(1, delay)
                play.start()

            time.sleep(delay / 1000.0)

            if thd:
                # current_status = thd.frame.tnumrd.GetLabel()
                # if current_status in ['broken', 'finished']:
                #     break
                if thd.frame.isbrokenorfinish:
                    break
                thd.event.wait()
                text = '%s  [%d/%d %d/%d] %d%%' % (thd.running_text, i+1, steps, thd.j, thd.run_times, thd.run_speed)
                thd.frame.tnumrd.SetLabel(text)

            if event_type == 'EM':
                x, y = action
                # 兼容旧版的绝对坐标
                if not isinstance(x, int) and not isinstance(y, int):
                    x = float(re.match('([0-1].[0-9]+)%', x).group(1))
                    y = float(re.match('([0-1].[0-9]+)%', y).group(1))

                if action == [-1, -1]:
                    # 约定 [-1, -1] 表示鼠标保持原位置不动
                    pass
                else:
                    # 挪动鼠标 普通做法
                    # ctypes.windll.user32.SetCursorPos(x, y)
                    # or
                    # win32api.SetCursorPos([x, y])

                    # 更好的兼容 win10 屏幕缩放问题
                    if isinstance(x, int) and isinstance(y, int):
                        nx = int(x * 65535 / SW)
                        ny = int(y * 65535 / SH)
                    else:
                        nx = int(x * 65535)
                        ny = int(y * 65535)
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
                    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, win32con.WHEEL_DELTA, 0)
                elif message == 'mouse wheel down':
                    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -win32con.WHEEL_DELTA, 0)
                elif message == 'mouse move':
                    pass
                else:
                    print('unknow mouse event:', message)

            elif event_type == 'EK':
                key_code, key_name, extended = action

                # shift ctrl alt
                # if key_code >= 160 and key_code <= 165:
                #     key_code = int(key_code/2) - 64

                # 不执行热键
                hot_keys = [HOT_KEYS[thd.frame.choice_start.GetSelection()], HOT_KEYS[thd.frame.choice_stop.GetSelection()]]
                if key_name in hot_keys:
                    continue

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


class PlayPromptTone(threading.Thread):

    def __init__(self, op, delay):
        self._delay = delay
        self._op = op
        super().__init__()

    def run(self):
        if 1 == self._op:
            if self._delay >= 1000:
                time.sleep((self._delay - 500.0) / 1000.0)
            self._play_start_sound()

    def _play_start_sound(self):
        try:
            path = os.path.join(os.getcwd(), 'sounds', 'start.mp3')
            playsound(path)
        except PlaysoundException as e:
            print(e)

    @classmethod
    def play_end_sound(cls):
        try:
            path = os.path.join(os.getcwd(), 'sounds', 'end.mp3')
            playsound(path)
        except PlaysoundException as e:
            print(e)
