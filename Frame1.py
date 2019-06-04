#Boa:Frame:Frame1

import os
import sys
import wx
import time
import threading
import datetime
import json
import traceback

from pynput import mouse
from pynput import keyboard
from pynput.mouse import Button
from pynput.keyboard import Key, KeyCode

PY2 = PY3 = False
try:
    import StringIO
    from wx import TaskBarIcon as wxTaskBarIcon
    from wx import EVT_TASKBAR_LEFT_DCLICK
    PY2 = True
except:
    import io
    from wx.adv import TaskBarIcon as wxTaskBarIcon
    from wx.adv import EVT_TASKBAR_LEFT_DCLICK
    PY3 = True


wx.NO_3D = 0


KEYS = ['F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12']


def GetMondrianStream():
    if PY2:
        data = '\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x06\x00\x00\x00szz\xf4\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00qIDATX\x85\xed\xd6;\n\x800\x10E\xd1{\xc5\x8d\xb9r\x97\x16\x0b\xad$\x8a\x82:\x16o\xda\x84pB2\x1f\x81Fa\x8c\x9c\x08\x04Z{\xcf\xa72\xbcv\xfa\xc5\x08 \x80r\x80\xfc\xa2\x0e\x1c\xe4\xba\xfaX\x1d\xd0\xde]S\x07\x02\xd8>\xe1wa-`\x9fQ\xe9\x86\x01\x04\x10\x00\\(Dk\x1b-\x04\xdc\x1d\x07\x14\x98;\x0bS\x7f\x7f\xf9\x13\x04\x10@\xf9X\xbe\x00\xc9 \x14K\xc1<={\x00\x00\x00\x00IEND\xaeB`\x82'
        stream = StringIO.StringIO(data)
    else:
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


[wxID_FRAME1, wxID_FRAME1BTRECORD, wxID_FRAME1BTRUN, wxID_FRAME1BUTTON1, 
 wxID_FRAME1CHOICE_SCRIPT, wxID_FRAME1CHOICE_START, wxID_FRAME1CHOICE_STOP, 
 wxID_FRAME1PANEL1, wxID_FRAME1STATICTEXT1, wxID_FRAME1STATICTEXT2, 
 wxID_FRAME1STATICTEXT3, wxID_FRAME1STATICTEXT4, wxID_FRAME1STIMES, 
 wxID_FRAME1TEXTCTRL1, wxID_FRAME1TEXTCTRL2, wxID_FRAME1TNUMRD, 
 wxID_FRAME1TSTOP, wxID_FRAME1STATICTEXT5, wxID_FRAME1TEXTCTRL3,
] = [wx.NewId() for _init_ctrls in range(19)]


class Frame1(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(506, 283), size=wx.Size(366, 201),
              style=wx.STAY_ON_TOP | wx.DEFAULT_FRAME_STYLE,
              title='Keymouse Go')
        self.SetClientSize(wx.Size(350, 205))

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1', parent=self,
              pos=wx.Point(0, 0), size=wx.Size(350, 205),
              style=wx.NO_3D | wx.CAPTION)

        self.btrecord = wx.Button(id=wxID_FRAME1BTRECORD, label=u'\u5f55\u5236',
              name='btrecord', parent=self.panel1, pos=wx.Point(202, 12),
              size=wx.Size(56, 32), style=0)
        self.btrecord.Bind(wx.EVT_BUTTON, self.OnBtrecordButton,
              id=wxID_FRAME1BTRECORD)

        self.btrun = wx.Button(id=wxID_FRAME1BTRUN, label=u'\u542f\u52a8',
              name='btrun', parent=self.panel1, pos=wx.Point(274, 12),
              size=wx.Size(56, 32), style=0)
        self.btrun.Bind(wx.EVT_BUTTON, self.OnBtrunButton, id=wxID_FRAME1BTRUN)

        self.tnumrd = wx.StaticText(id=wxID_FRAME1TNUMRD, label=u'ready..',
              name='tnumrd', parent=self.panel1, pos=wx.Point(17, 175),
              size=wx.Size(100, 36), style=0)

        self.button1 = wx.Button(id=wxID_FRAME1BUTTON1, label=u'test',
              name='button1', parent=self.panel1, pos=wx.Point(128, 296),
              size=wx.Size(75, 24), style=0)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_FRAME1BUTTON1)

        self.tstop = wx.StaticText(id=wxID_FRAME1TSTOP,
              label=u'If you want to stop it, Press F12', name='tstop',
              parent=self.panel1, pos=wx.Point(25, 332), size=wx.Size(183, 18),
              style=0)
        self.tstop.Show(False)

        self.stimes = wx.SpinCtrl(id=wxID_FRAME1STIMES, initial=0, max=1000,
              min=0, name='stimes', parent=self.panel1, pos=wx.Point(206, 101),
              size=wx.Size(45, 18), style=wx.SP_ARROW_KEYS)
        self.stimes.SetValue(1)

        self.label_run_times = wx.StaticText(id=wxID_FRAME1STATICTEXT2,
              label=u'\u6267\u884c\u6b21\u6570(0\u4e3a\u65e0\u9650\u5faa\u73af)',
              name='label_run_times', parent=self.panel1, pos=wx.Point(203, 61),
              size=wx.Size(136, 26), style=0)

        self.textCtrl1 = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL1, name='textCtrl1',
              parent=self.panel1, pos=wx.Point(24, 296), size=wx.Size(40, 22),
              style=0, value='119')

        self.textCtrl2 = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL2, name='textCtrl2',
              parent=self.panel1, pos=wx.Point(80, 296), size=wx.Size(36, 22),
              style=0, value='123')

        self.label_script = wx.StaticText(id=wxID_FRAME1STATICTEXT3,
              label=u'\u811a\u672c', name='label_script', parent=self.panel1,
              pos=wx.Point(17, 20), size=wx.Size(40, 32), style=0)

        self.choice_script = wx.Choice(choices=[], id=wxID_FRAME1CHOICE_SCRIPT,
              name=u'choice_script', parent=self.panel1, pos=wx.Point(79, 15),
              size=wx.Size(108, 25), style=0)

        self.label_start_key = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label=u'\u542f\u52a8\u70ed\u952e', name='label_start_key',
              parent=self.panel1, pos=wx.Point(16, 63), size=wx.Size(56, 24),
              style=0)

        self.label_stop_key = wx.StaticText(id=wxID_FRAME1STATICTEXT4,
              label=u'\u7ec8\u6b62\u70ed\u952e', name='label_stop_key',
              parent=self.panel1, pos=wx.Point(16, 102), size=wx.Size(56, 32),
              style=0)

        self.label_scale = wx.StaticText(id=wxID_FRAME1STATICTEXT5,
              label=u'\u5c4f\u5e55\u7f29\u653e', name='staticText5',
              parent=self.panel1, pos=wx.Point(16, 141), size=wx.Size(56, 32),
              style=0)

        self.choice_start = wx.Choice(choices=[], id=wxID_FRAME1CHOICE_START,
              name=u'choice_start', parent=self.panel1, pos=wx.Point(79, 58),
              size=wx.Size(108, 25), style=0)
        self.choice_start.SetLabel(u'')
        self.choice_start.SetLabelText(u'')
        self.choice_start.Bind(wx.EVT_CHOICE, self.OnChoice_startChoice,
              id=wxID_FRAME1CHOICE_START)

        self.choice_stop = wx.Choice(choices=[], id=wxID_FRAME1CHOICE_STOP,
              name=u'choice_stop', parent=self.panel1, pos=wx.Point(79, 98),
              size=wx.Size(108, 25), style=0)
        self.choice_stop.Bind(wx.EVT_CHOICE, self.OnChoice_stopChoice,
              id=wxID_FRAME1CHOICE_STOP)

        self.text_scale = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL3, name='textCtrl3',
              parent=self.panel1, pos=wx.Point(79, 138), size=wx.Size(108, 22),
              style=0, value='100%')

    def __init__(self, parent):

        self._init_ctrls(parent)
        
        self.SetIcon(GetMondrianIcon())
        self.taskBarIcon = TaskBarIcon(self) 
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_ICONIZE, self.OnIconfiy)
        
        if not os.path.exists('scripts'):
            os.mkdir('scripts')
        self.scripts = os.listdir('scripts')[::-1]
        
        self.choice_script.SetItems(self.scripts)
        self.scripts = list(filter(lambda s: s.endswith('.txt'), self.scripts))
        if self.scripts:
            self.choice_script.SetSelection(0)
                
        self.choice_start.SetItems(KEYS)
        self.choice_start.SetSelection(3)
        
        self.choice_stop.SetItems(KEYS)
        self.choice_stop.SetSelection(6)

        self.running = False
        self.recording = False
        self.record = []
        self.ttt = self.now_ts

        # =========== create mouse listener for record ===========
        def on_move(x, y):
            if not self.recording or self.running:
                return True

        def on_scroll(x, y, dx, dy):
            if not self.recording or self.running:
                return True

        def on_click(x, y, button, pressed):

            if not self.recording or self.running:
                return True

            try:
                scale = self.text_scale.GetValue()
                scale = scale.replace('%', '').replace('-', '').strip()
                scale = float(scale)
                scale = scale / 100.0
            except:
                scale = 1

            x = int(x / scale)
            y = int(y / scale)

            print('mouse click:', x, y, button.name, pressed)
            delay = self.now_ts - self.ttt
            self.ttt = self.now_ts
            pos = (x, y)
            if button.name == 'left':
                message = 'mouse left '
            elif button.name == 'right':
                message = 'mouse right '
            else:
                return True
            if pressed:
                message += 'down'
            else:
                message += 'up'
            self.record.append(['EM', message, pos, delay])
            text = self.tnumrd.GetLabel()
            text = text.replace(' actions recorded','')
            text = str(eval(text)+1)
            text = text + ' actions recorded'
            self.tnumrd.SetLabel(text)
            return True

        self.mouse_listener = mouse.Listener(
            on_move=on_move,
            on_scroll=on_scroll,
            on_click=on_click
        )
        self.mouse_listener.start()

        # =========== create keyboard listener for record ===========
        def key_event(key, is_press):
            if not self.recording or self.running:
                return True

            if is_press:
                print('keyboard press:', key)
                message = 'key down'
            else:
                print('keyboard release:', key)
                message = 'key up'

            if isinstance(key, Key):
                print('Key:', key.name, key.value.vk)
                name = key.name
            elif isinstance(key, KeyCode):
                print('KeyCode:', key.char, key.vk)
                name = key.char
            else:
                assert False

            delay = self.now_ts - self.ttt
            self.ttt = self.now_ts

            self.record.append(['EK', message, name, delay])

            text = self.tnumrd.GetLabel()
            text = text.replace(' actions recorded', '')
            text = str(eval(text) + 1)
            text = text + ' actions recorded'
            self.tnumrd.SetLabel(text)
            return True

        def on_press(key):
            if not self.recording:
                # listen for start/stop script
                start_name = 'f6'
                stop_name = 'f9'
                start_index = self.choice_start.GetSelection()
                start_name = KEYS[start_index].lower()
                stop_index = self.choice_stop.GetSelection()
                stop_name = KEYS[stop_index].lower()

                print(start_name, stop_name, key)

                if not isinstance(key, Key):
                    return True

                if key.name == start_name and not self.running:
                    print('script start')
                    t = RunScriptClass(self)
                    t.start()
                elif key.name == stop_name and self.running:
                    print('script stop')
                    self.tnumrd.SetLabel('broken')

            return key_event(key, True)

        def on_release(key):
            return key_event(key, False)

        self.keyboard_listener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release)
        self.keyboard_listener.start()

    @property
    def now_ts(self):
        return int(time.time() * 1000)

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
        try:
            self.mouse_listener.stop()
            self.keyboard_listener.stop()
        except:
            pass
        self.taskBarIcon.Destroy()
        self.Destroy()
        event.Skip()

    def OnButton1Button(self, event):
        event.Skip()

    def OnBtrecordButton(self, event):

        if self.recording:
            print('record stop')
            self.recording = False
            del self.record[-2]
            del self.record[-1]
            output = json.dumps(self.record, indent=1)
            output = output.replace('\r\n', '\n').replace('\r', '\n')
            output = output.replace('\n   ', '').replace('\n  ', '')
            output = output.replace('\n ]', ']')
            open(self.new_script_path(), 'w').write(output)
            self.btrecord.SetLabel(u'\u5f55\u5236')
            self.tnumrd.SetLabel('finished')
            self.record = []
        else:
            print('record start')
            self.recording = True
            self.ttt = self.now_ts
            status = self.tnumrd.GetLabel()
            if 'running' in status or 'recorded' in status:
                return
            self.btrecord.SetLabel(u'\u7ed3\u675f')
            self.tnumrd.SetLabel('0 actions recorded')
            self.choice_script.SetSelection(-1)
            self.record = []
        
        event.Skip()

    def OnBtrunButton(self, event):
        print('script start by btn')
        t = RunScriptClass(self)
        t.start()
        event.Skip()

    def OnChoice_startChoice(self, event):
        event.Skip()

    def OnChoice_stopChoice(self, event):
        event.Skip()


class RunScriptClass(threading.Thread):

    def __init__(self, frame):
        self.frame = frame
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
            s = open(script_path, 'r').read()
            s = json.loads(s)
            steps = len(s)
            run_times = self.frame.stimes.Value

            text = '%s running..' % script_path.split('/')[-1].split('\\')[-1]
            self.frame.tnumrd.SetLabel(text)
            self.frame.tstop.Shown = True

            mouse_ctl = mouse.Controller()
            keyboard_ctl = keyboard.Controller()

            j = 0
            while j < run_times or run_times == 0:
                j += 1

                if self.frame.tnumrd.GetLabel() == 'broken' or self.frame.tnumrd.GetLabel() == 'finished':
                    self.frame.running = False
                    break
                
                for i in range(0, steps):

                    print(s[i])

                    event_type = s[i][0]
                    message = s[i][1]
                    delay = s[i][3]
                    
                    time.sleep(delay / 1000.0)
                    
                    if self.frame.tnumrd.GetLabel() == 'broken' or self.frame.tnumrd.GetLabel() == 'finished':
                        break
                    
                    if event_type == 'EM':
                        x, y = s[i][2]
                        mouse_ctl.position = (x, y)
                        if message == 'mouse left down':
                            mouse_ctl.press(Button.left)
                        elif message == 'mouse left up':
                            mouse_ctl.release(Button.left)
                        elif message == 'mouse right down':
                            mouse_ctl.press(Button.right)
                        elif message == 'mouse right up':
                            mouse_ctl.release(Button.right)

                    elif event_type == 'EK':
                        key_name = s[i][2]

                        if len(key_name) == 1:
                            key = key_name
                        else:
                            key = getattr(Key, key_name)

                        if message == 'key down':
                            keyboard_ctl.press(key)
                        elif message == 'key up':
                            keyboard_ctl.release(key)

            self.frame.tnumrd.SetLabel('finished')
            self.frame.tstop.Shown = False
            self.frame.running = False
            print('script run finish!')
            
        except Exception as e:
            print('run error', e)
            traceback.print_exc()
            self.frame.tnumrd.SetLabel('failed')
            self.frame.tstop.Shown = False
            self.frame.running = False


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
        wx.MessageBox('https://github.com/taojy123/KeymouseGo', 'KeymouseGo')
        event.Skip()

    def OnCloseshow(self, event):
        self.frame.Close(True)
        event.Skip()

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(self.ID_About, 'About')
        menu.Append(self.ID_Closeshow, 'Exit')
        return menu

