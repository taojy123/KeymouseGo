#Boa:Frame:Frame1

import os
import sys
import wx
import wx.lib.buttons
import wx.lib.analogclock
import wx.lib.throbber
import pyHook
import win32ui,win32con,pythoncom,win32gui,win32process,win32api
import ctypes
import time
import threading
import cStringIO
import datetime
import json
import traceback


global record
record = []
global hm
hm = pyHook.HookManager()
hm.keyboard_hook = False
hm.mouse_hook = False
global hm2
hm2 = pyHook.HookManager()


KEYS = ['F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12']


def GetMondrianData():
    return \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x06\x00\
\x00\x00szz\xf4\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00qID\
ATX\x85\xed\xd6;\n\x800\x10E\xd1{\xc5\x8d\xb9r\x97\x16\x0b\xad$\x8a\x82:\x16\
o\xda\x84pB2\x1f\x81Fa\x8c\x9c\x08\x04Z{\xcf\xa72\xbcv\xfa\xc5\x08 \x80r\x80\
\xfc\xa2\x0e\x1c\xe4\xba\xfaX\x1d\xd0\xde]S\x07\x02\xd8>\xe1wa-`\x9fQ\xe9\
\x86\x01\x04\x10\x00\\(Dk\x1b-\x04\xdc\x1d\x07\x14\x98;\x0bS\x7f\x7f\xf9\x13\
\x04\x10@\xf9X\xbe\x00\xc9 \x14K\xc1<={\x00\x00\x00\x00IEND\xaeB`\x82' 

def GetMondrianImage():
    stream = cStringIO.StringIO(GetMondrianData())
    return wx.ImageFromStream(stream)

def GetMondrianBitmap():
    return wx.BitmapFromImage(GetMondrianImage())

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
 wxID_FRAME1TSTOP, 
] = [wx.NewId() for _init_ctrls in range(17)]

class Frame1(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(506, 283), size=wx.Size(366, 201),
              style=wx.STAY_ON_TOP | wx.DEFAULT_FRAME_STYLE,
              title='Keymouse Go')
        self.SetClientSize(wx.Size(350, 163))

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1', parent=self,
              pos=wx.Point(0, 0), size=wx.Size(350, 163),
              style=wx.NO_3D | wx.CAPTION)

        self.btrecord = wx.Button(id=wxID_FRAME1BTRECORD, label=u'\u5f55\u5236',
              name='btrecord', parent=self.panel1, pos=wx.Point(202, 12),
              size=wx.Size(56, 32), style=0)
        self.btrecord.Bind(wx.EVT_BUTTON, self.OnBtrecordButton,
              id=wxID_FRAME1BTRECORD)

        self.btrun = wx.Button(id=wxID_FRAME1BTRUN, label=u'\u8fd0\u884c',
              name='btrun', parent=self.panel1, pos=wx.Point(274, 12),
              size=wx.Size(56, 32), style=0)
        self.btrun.Bind(wx.EVT_BUTTON, self.OnBtrunButton, id=wxID_FRAME1BTRUN)

        self.tnumrd = wx.StaticText(id=wxID_FRAME1TNUMRD, label=u'ready..',
              name='tnumrd', parent=self.panel1, pos=wx.Point(17, 135),
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
        self.tstop.SetToolTipString('tstop')
        self.tstop.Show(False)

        self.stimes = wx.SpinCtrl(id=wxID_FRAME1STIMES, initial=0, max=1000,
              min=0, name='stimes', parent=self.panel1, pos=wx.Point(206, 101),
              size=wx.Size(45, 18), style=wx.SP_ARROW_KEYS)
        self.stimes.SetValue(1)

        self.staticText2 = wx.StaticText(id=wxID_FRAME1STATICTEXT2,
              label=u'\u6267\u884c\u6b21\u6570(0\u4e3a\u65e0\u9650\u5faa\u73af)',
              name='staticText2', parent=self.panel1, pos=wx.Point(203, 61),
              size=wx.Size(136, 26), style=0)

        self.textCtrl1 = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL1, name='textCtrl1',
              parent=self.panel1, pos=wx.Point(24, 296), size=wx.Size(40, 22),
              style=0, value='119')

        self.textCtrl2 = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL2, name='textCtrl2',
              parent=self.panel1, pos=wx.Point(80, 296), size=wx.Size(36, 22),
              style=0, value='123')

        self.staticText3 = wx.StaticText(id=wxID_FRAME1STATICTEXT3,
              label=u'\u811a\u672c', name='staticText3', parent=self.panel1,
              pos=wx.Point(17, 20), size=wx.Size(40, 32), style=0)

        self.choice_script = wx.Choice(choices=[], id=wxID_FRAME1CHOICE_SCRIPT,
              name=u'choice_script', parent=self.panel1, pos=wx.Point(79, 15),
              size=wx.Size(108, 25), style=0)

        self.staticText1 = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label=u'\u542f\u52a8\u70ed\u952e', name='staticText1',
              parent=self.panel1, pos=wx.Point(16, 63), size=wx.Size(56, 24),
              style=0)

        self.staticText4 = wx.StaticText(id=wxID_FRAME1STATICTEXT4,
              label=u'\u7ec8\u6b62\u70ed\u952e', name='staticText4',
              parent=self.panel1, pos=wx.Point(16, 102), size=wx.Size(56, 32),
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

    def __init__(self, parent):
        global mself
        
        mself=self
        
        self._init_ctrls(parent)

        
        self.SetIcon(GetMondrianIcon())
        self.taskBarIcon = TaskBarIcon(self) 
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_ICONIZE, self.OnIconfiy)
        
        if not os.path.exists('scripts'):
            os.mkdir('scripts')
        self.scripts = os.listdir('scripts')[::-1]
        
        self.choice_script.SetItems(self.scripts)
        self.scripts = filter(lambda s: s.endswith('.txt'), self.scripts)
        if self.scripts:
            self.choice_script.SetSelection(0)
                
        self.choice_start.SetItems(KEYS)
        self.choice_start.SetSelection(5)
        
        self.choice_stop.SetItems(KEYS)
        self.choice_stop.SetSelection(9)

        def onKeyboardEvent2(event):

            start_code = 119 #F8
            stop_code = 123  #F12
            
            start_code = int(self.textCtrl1.GetValue())
            stop_code = int(self.textCtrl2.GetValue())

            # print(start_code, stop_code, event.KeyID)

            if event.KeyID == start_code:
                t = ThreadClass()
                t.start()
            elif event.KeyID == stop_code:
                mself.tnumrd.SetLabel('breaked')
                
            return True

        hm2.KeyUp = onKeyboardEvent2
        hm2.HookKeyboard()
        
    def get_script_path(self):
        i = self.choice_script.GetSelection()
        if i < 0:
            return ''
        script = self.scripts[i]
        path = os.path.join(os.getcwd(), 'scripts', script)
        print path
        return path
        
    def new_script_path(self):
        now = datetime.datetime.now()
        script = '%s.txt' % now.strftime('%m%d_%H%M')
        if script in self.scripts:
            script = script = '%s.txt' % now.strftime('%m%d_%H%M%S')
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
        self.taskBarIcon.Destroy()
        self.Destroy()
        event.Skip()
        

    def OnButton1Button(self, event):
        event.Skip()
        
        
    def OnBtrecordButton(self, event):
        global record
        global hm
        global hm2
        global ttt
        ttt = 0
        
        def onMouseEvent(event):
            global ttt
            if ttt == 0:
                ttt = event.Time
            if event.MessageName == 'mouse move':
                return True
            pos = win32gui.GetCursorPos()
            rhwnd = win32gui.WindowFromPoint(pos)
            pos = win32gui.ScreenToClient(rhwnd, pos)
            cname = win32gui.GetClassName(rhwnd)
            dcid = win32gui.GetDlgCtrlID(rhwnd)  
            # print event.Message, event.MessageName
            interval = event.Time - ttt
            record.append(['EM', event.MessageName, event.Position, interval])
            ttt = event.Time
            ts = self.tnumrd.GetLabel()
            ts = ts.replace(' actions recorded','')
            ts = str(eval(ts)+1)
            ts = ts + ' actions recorded'
            self.tnumrd.SetLabel(ts)
            return True

        def onKeyboardEvent(event):
            global ttt
            if ttt == 0:
                ttt = event.Time - 1000
            pos = win32gui.GetCursorPos()
            rhwnd = win32gui.WindowFromPoint(pos)
            cname = win32gui.GetClassName(rhwnd)
            dcid = win32gui.GetDlgCtrlID(rhwnd)
            # print event.Message, event.MessageName
            interval = event.Time - ttt
            record.append(['EK', event.MessageName, (event.KeyID, event.Key), interval])
            # event.Key is useless, just for remark
            ttt = event.Time
            ts = self.tnumrd.GetLabel()
            ts = ts.replace(' actions recorded','')
            ts = str(eval(ts)+1)
            ts = ts + ' actions recorded'
            self.tnumrd.SetLabel(ts)
            return True
        

        try:
            if hm.keyboard_hook and hm.mouse_hook:
                # stop and save record
                hm.UnhookMouse()
                hm.UnhookKeyboard()
                del record[-2]
                del record[-1]
                output = json.dumps(record, indent=1)
                output = output.replace('\r\n', '\n').replace('\r', '\n')
                output = output.replace('\n   ', '').replace('\n  ', '')
                output = output.replace('\n ]', ']')
                file(self.new_script_path(),'w').write(output)
                self.btrecord.SetLabel(u'\u5f55\u5236')
                self.tnumrd.SetLabel('finished')
                hm2.HookKeyboard()
            else:
                # start record  
                status = self.tnumrd.GetLabel()
                if 'runing' in status or 'recorded' in status:
                    return
                hm2.UnhookKeyboard()
                record=[]
                hm.MouseAll = onMouseEvent
                hm.KeyAll = onKeyboardEvent
                hm.HookMouse()
                hm.HookKeyboard()
                self.btrecord.SetLabel(u'\u7ed3\u675f')
                self.tnumrd.SetLabel('0 actions recorded')
                self.choice_script.SetSelection(-1)

        except:
            print 'record errors'
            traceback.print_exc()
        
        event.Skip()

    def OnBtrunButton(self, event):
                 
        t = ThreadClass()
        t.start()

        event.Skip()


    def OnSmodeScroll(self, event):
        # if self.smode.Value == 0:   #normal mode
        #     self.btrun.Enabled = True
        #     self.btrun.SetLabel('Run Script (F9)')
        # else:   #background mode
        #     self.btrun.Enabled = False
        #     self.btrun.SetLabel("Move to the title bar and Press F8 to runing")
        event.Skip()

    def OnChoice_startChoice(self, event):
        i = self.choice_start.GetSelection()
        j = self.choice_stop.GetSelection()
        if i == j:
            i = (i+1) % 10
            self.choice_start.SetSelection(i)
        self.textCtrl1.SetValue(str(i + 114))
        event.Skip()

    def OnChoice_stopChoice(self, event):
        i = self.choice_start.GetSelection()
        j = self.choice_stop.GetSelection()
        if i == j:
            j = (i+1) % 10
            self.choice_stop.SetSelection(j)
        self.textCtrl2.SetValue(str(j + 114))
        event.Skip()


class TaskBarIcon(wx.TaskBarIcon):
    ID_About = wx.NewId()
    ID_Closeshow=wx.NewId()
    
    def __init__(self, frame):
        wx.TaskBarIcon.__init__(self)
        self.frame = frame
        self.SetIcon(GetMondrianIcon())
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarLeftDClick)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=self.ID_About)
        self.Bind(wx.EVT_MENU, self.OnCloseshow, id=self.ID_Closeshow)

    def OnTaskBarLeftDClick(self, event):
        if self.frame.IsIconized():
           self.frame.Iconize(False)
        if not self.frame.IsShown():
           self.frame.Show(True)
        self.frame.Raise()

    def OnAbout(self,event):
        wx.MessageBox('KeymouseGo v1.1', 'KeymouseGo')
        event.Skip()

    def OnCloseshow(self,event):
        self.frame.Close(True)
        event.Skip()

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(self.ID_About, 'About')
        menu.Append(self.ID_Closeshow, 'Exit')
        return menu




class ThreadClass(threading.Thread):


    def run(self):

        status = mself.tnumrd.GetLabel()
        if 'runing' in status or 'recorded' in status:
            return

        script_path = mself.get_script_path()
        if not script_path:
            mself.tnumrd.SetLabel('script not found, please record first!')
            return

        try:
            rhwnd = win32gui.WindowFromPoint(win32gui.GetCursorPos())
            s = file(script_path, 'r').read()
            s = json.loads(s)
            l = len(s)
            mself.tnumrd.SetLabel('%s runing..' % script_path.split('\\')[-1])
            mself.tstop.Shown = True

            j=0
            while j < mself.stimes.Value or mself.stimes.Value == 0:
                if mself.tnumrd.GetLabel() == 'breaked' or mself.tnumrd.GetLabel() == 'finished':
                    break
                if mself.stimes.Value != 0:
                    j=j+1
                
                for i in range(0,l):
                    
                    time.sleep(s[i][3]/1000.0)
                    
                    if mself.tnumrd.GetLabel() == 'breaked' or mself.tnumrd.GetLabel() == 'finished':
                        break
                    
                    if s[i][0]=='EM':
                        # if mself.smode.Value == 0:  #normal mode

                        ctypes.windll.user32.SetCursorPos(s[i][2][0], s[i][2][1])
                        
                        if s[i][1]=='mouse left down':
                            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                        elif s[i][1]=='mouse left up':
                            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                        elif s[i][1]=='mouse right down':
                            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
                        elif s[i][1]=='mouse right up':
                            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
                            
                        # else:   #background mode
                        #     def _windowEnumerationHandler(hwnd, resultList):
                        #         resultList.append((hwnd,win32gui.GetClassName(hwnd),win32gui.GetDlgCtrlID(hwnd)))
                        #     cwindows = []
                        #     win32gui.EnumChildWindows(rhwnd, _windowEnumerationHandler, cwindows)
                            
                        #     for hwnd, ClassName, DlgCtrlID in cwindows:
                        #         if ClassName == s[i][6]  and DlgCtrlID == s[i][7]:
                        #             tmp = win32api.MAKELONG(s[i][8][0], s[i][8][1])
                        #             win32gui.PostMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
                        #             if s[i][1]=='mouse left down':
                        #                 win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, tmp)
                        #             elif s[i][1]=='mouse left up':
                        #                 win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, tmp)
                        #             elif s[i][1]=='mouse right down':
                        #                 win32api.PostMessage(hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, tmp)
                        #             elif s[i][1]=='mouse right up':
                        #                 win32api.PostMessage(hwnd, win32con.WM_RBUTTONUP, win32con.MK_RBUTTON, tmp)
                        #             else:
                        #                 win32api.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, tmp)
                            

                    elif s[i][0] =='EK':
                        # if mself.smode.Value == 0:  #normal mode
                        key_code = s[i][2][0]
                        if key_code >= 160 and key_code <= 165:
                            key_code = (key_code//2) - 64
                        if s[i][1]=='key down':
                            win32api.keybd_event(key_code, 0, 0, 0)  
                        elif s[i][1]=='key up':
                            win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_KEYUP, 0)
                        # else:   #background mode
                        #     pass    #not developed

            mself.tnumrd.SetLabel('finished')
            mself.tstop.Shown = False
            
        except:
            print 'run error'
            traceback.print_exc()
            mself.tnumrd.SetLabel('failed')
            mself.tstop.Shown = False

# end of ThreadClass
