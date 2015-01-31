#Boa:Frame:Frame1

import os
import wx
import wx.lib.buttons
import wx.lib.analogclock
import wx.lib.throbber
import pyHook
import win32ui,win32con,pythoncom,win32gui,win32process,win32api
import ctypes
import time
import threading


global record
record = []
global hm
hm = pyHook.HookManager()
hm.keyboard_hook = False
hm.mouse_hook = False
global hm2
hm2 = pyHook.HookManager()


def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1BTRECORD, wxID_FRAME1BTRUN, wxID_FRAME1BUTTON1, 
 wxID_FRAME1PANEL1, wxID_FRAME1SMODE, wxID_FRAME1STATICTEXT1, 
 wxID_FRAME1STATICTEXT2, wxID_FRAME1STATICTEXT3, wxID_FRAME1STATICTEXT4, 
 wxID_FRAME1STIMES, wxID_FRAME1TNUMRD, wxID_FRAME1TSTOP, 
] = [wx.NewId() for _init_ctrls in range(13)]

class Frame1(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(506, 283), size=wx.Size(292, 209),
              style=wx.STAY_ON_TOP | wx.DEFAULT_FRAME_STYLE,
              title='Keymouse Go')
        self.SetClientSize(wx.Size(284, 175))

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1', parent=self,
              pos=wx.Point(0, 0), size=wx.Size(284, 175),
              style=wx.NO_3D | wx.CAPTION)

        self.btrecord = wx.Button(id=wxID_FRAME1BTRECORD, label='Record Script',
              name='btrecord', parent=self.panel1, pos=wx.Point(16, 40),
              size=wx.Size(256, 24), style=0)
        self.btrecord.Bind(wx.EVT_BUTTON, self.OnBtrecordButton,
              id=wxID_FRAME1BTRECORD)

        self.btrun = wx.Button(id=wxID_FRAME1BTRUN, label='Run Script (F8)',
              name='btrun', parent=self.panel1, pos=wx.Point(16, 128),
              size=wx.Size(256, 24), style=0)
        self.btrun.Bind(wx.EVT_BUTTON, self.OnBtrunButton, id=wxID_FRAME1BTRUN)

        self.tnumrd = wx.StaticText(id=wxID_FRAME1TNUMRD, label='ready..',
              name='tnumrd', parent=self.panel1, pos=wx.Point(12, 156),
              size=wx.Size(38, 14), style=0)

        self.button1 = wx.Button(id=wxID_FRAME1BUTTON1, label='button1',
              name='button1', parent=self.panel1, pos=wx.Point(336, 8),
              size=wx.Size(75, 24), style=0)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_FRAME1BUTTON1)

        self.tstop = wx.StaticText(id=wxID_FRAME1TSTOP,
              label='If you want to stop it, Press F12', name='tstop',
              parent=self.panel1, pos=wx.Point(97, 156), size=wx.Size(179, 14),
              style=0)
        self.tstop.SetToolTipString('tstop')
        self.tstop.Show(False)

        self.stimes = wx.SpinCtrl(id=wxID_FRAME1STIMES, initial=0, max=100,
              min=0, name='stimes', parent=self.panel1, pos=wx.Point(18, 88),
              size=wx.Size(45, 18), style=wx.SP_ARROW_KEYS)
        self.stimes.SetValue(1)

        self.staticText1 = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label='Chose 0 for Infinite loop', name='staticText1',
              parent=self.panel1, pos=wx.Point(8, 108), size=wx.Size(132, 14),
              style=0)

        self.staticText2 = wx.StaticText(id=wxID_FRAME1STATICTEXT2,
              label='Loop times', name='staticText2', parent=self.panel1,
              pos=wx.Point(8, 70), size=wx.Size(60, 14), style=0)

        self.smode = wx.Slider(id=wxID_FRAME1SMODE, maxValue=1, minValue=0,
              name='smode', parent=self.panel1, pos=wx.Point(90, 8),
              size=wx.Size(76, 24), style=wx.SL_HORIZONTAL, value=0)
        self.smode.SetLabel('')
        self.smode.Bind(wx.EVT_SCROLL, self.OnSmodeScroll)

        self.staticText3 = wx.StaticText(id=wxID_FRAME1STATICTEXT3,
              label='Normal mode', name='staticText3', parent=self.panel1,
              pos=wx.Point(9, 13), size=wx.Size(80, 14), style=0)
        self.staticText3.SetToolTipString('staticText3')
        self.staticText3.SetHelpText('')
        self.staticText3.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.staticText4 = wx.StaticText(id=wxID_FRAME1STATICTEXT4,
              label='Background mode', name='staticText4', parent=self.panel1,
              pos=wx.Point(168, 13), size=wx.Size(111, 14), style=0)
        self.staticText4.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

    def __init__(self, parent):
        global mself
        mself=self
        
        self._init_ctrls(parent)

        def onKeyboardEvent2(event):
            
            if event.KeyID == 123:  #F12      
                mself.tnumrd.SetLabel('breaked')
            elif event.KeyID == 119:    #F8
                t = ThreadClass()
                t.start()
                

            return True
        hm2.KeyUp = onKeyboardEvent2
        hm2.HookKeyboard()
        

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
            record.append(['EM',event.MessageName,event.Message,event.Time - ttt,event.Position,event.Wheel,cname,dcid,pos])
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
            record.append(['EK',event.MessageName,event.Message,event.Time - ttt,event.KeyID,event.Key,cname,dcid])
            ttt = event.Time
            ts = self.tnumrd.GetLabel()
            ts = ts.replace(' actions recorded','')
            ts = str(eval(ts)+1)
            ts = ts + ' actions recorded'
            self.tnumrd.SetLabel(ts)
            return True
        

        try:
            if hm.keyboard_hook and hm.mouse_hook:
                hm.UnhookMouse()
                hm.UnhookKeyboard()
                del record[-2]
                del record[-1]
                f=file('1.txt','w')
                f.write(str(record))
                f.close
                self.btrecord.SetLabel('Record Script')
                self.tnumrd.SetLabel('finished')
                hm2.HookKeyboard()
            else:
                hm2.UnhookKeyboard()
                record=[]
                hm.MouseAll = onMouseEvent
                hm.KeyAll = onKeyboardEvent
                hm.HookMouse()
                hm.HookKeyboard()
                self.btrecord.SetLabel('Finish')
                self.tnumrd.SetLabel('0 actions recorded')

        except:
            print 'record errors'
        
        event.Skip()

    def OnBtrunButton(self, event):
                 
        t = ThreadClass()
        t.start()

        event.Skip()


    def OnSmodeScroll(self, event):
        if self.smode.Value == 0:   #normal mode
            self.btrun.Enabled = True
            self.btrun.SetLabel('Run Script (F8)')
        else:   #background mode
            self.btrun.Enabled = False
            self.btrun.SetLabel("Move to the title bar and Press F8 to runing")
        event.Skip()


class ThreadClass(threading.Thread):
    def run(self):
        try:
            rhwnd = win32gui.WindowFromPoint(win32gui.GetCursorPos())
            f = file('1.txt','r')
            s=f.read()
            s=eval(s)
            l=len(s)
            mself.tnumrd.SetLabel('runing..')
            mself.tstop.Shown = True

            j=0
            while j < mself.stimes.Value or mself.stimes.Value == 0:
                if mself.tnumrd.GetLabel() == 'breaked' or mself.tnumrd.GetLabel() == 'finished':
                    break
                if mself.stimes.Value<>0:
                    j=j+1
                
                for i in range(0,l):
                    
                    time.sleep(s[i][3]/1000.0)
                    
                    if mself.tnumrd.GetLabel() == 'breaked' or mself.tnumrd.GetLabel() == 'finished':
                        break
                    
                    if s[i][0]=='EM':
                        if mself.smode.Value == 0:  #normal mode
                            ctypes.windll.user32.SetCursorPos(s[i][4][0], s[i][4][1])
                            
                            if s[i][1]=='mouse left down':
                                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                            elif s[i][1]=='mouse left up':
                                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                            elif s[i][1]=='mouse right down':
                                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
                            elif s[i][1]=='mouse right up':
                                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
                            
                        else:   #background mode
                            def _windowEnumerationHandler(hwnd, resultList):
                                resultList.append((hwnd,win32gui.GetClassName(hwnd),win32gui.GetDlgCtrlID(hwnd)))
                            cwindows = []
                            win32gui.EnumChildWindows(rhwnd, _windowEnumerationHandler, cwindows)
                            
                            for hwnd, ClassName, DlgCtrlID in cwindows:
                                if ClassName == s[i][6]  and DlgCtrlID == s[i][7]:
                                    tmp = win32api.MAKELONG(s[i][8][0], s[i][8][1])
                                    win32gui.PostMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
                                    if s[i][1]=='mouse left down':
                                        win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, tmp)
                                    elif s[i][1]=='mouse left up':
                                        win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, tmp)
                                    elif s[i][1]=='mouse right down':
                                        win32api.PostMessage(hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, tmp)
                                    elif s[i][1]=='mouse right up':
                                        win32api.PostMessage(hwnd, win32con.WM_RBUTTONUP, win32con.MK_RBUTTON, tmp)
                                    else:
                                        win32api.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, tmp)
                            

                    elif s[i][0] =='EK':
                        if mself.smode.Value == 0:  #normal mode
                            if s[i][4]>=160 and s[i][4]<=165:
                                s[i][4]=(s[i][4]//2)-64
                            if s[i][1]=='key down':
                                win32api.keybd_event(s[i][4],0,0,0)  
                            elif s[i][1]=='key up':
                                win32api.keybd_event(s[i][4],0,win32con.KEYEVENTF_KEYUP,0)
                        else:   #background mode
                            pass    #not developed

            mself.tnumrd.SetLabel('finished')
            mself.tstop.Shown = False
            f.close
            
        except:
            print 'run error'
            mself.tnumrd.SetLabel('failed')
            mself.tstop.Shown = False

# end of ThreadClass

