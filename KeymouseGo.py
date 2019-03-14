#!/usr/bin/env python
#Boa:App:BoaApp

import wx
import time
import Frame1
import sys
import json
import win32ui,win32con,pythoncom,win32gui,win32process,win32api
import ctypes


modules ={'Frame1': [1, 'Main frame of Application', u'Frame1.py']}

class BoaApp(wx.App):
    def OnInit(self):
        self.main = Frame1.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True


def main():
    application = BoaApp(0)
    application.MainLoop()


def single_run(script_path, times=1):

    s = file(script_path, 'r').read()
    s = json.loads(s)
    l = len(s)

    for j in range(times):
        
        for i in range(0, l):
            
            time.sleep(s[i][3]/1000.0)
            
            if s[i][0]=='EM':

                ctypes.windll.user32.SetCursorPos(s[i][2][0], s[i][2][1])
                
                if s[i][1]=='mouse left down':
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                elif s[i][1]=='mouse left up':
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                elif s[i][1]=='mouse right down':
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
                elif s[i][1]=='mouse right up':
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
                    
            elif s[i][0] =='EK':

                key_code = s[i][2][0]
                if key_code >= 160 and key_code <= 165:
                    key_code = (key_code//2) - 64

                if s[i][1]=='key down':
                    win32api.keybd_event(key_code, 0, 0, 0)  
                elif s[i][1]=='key up':
                    win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_KEYUP, 0)


if __name__ == '__main__':

    print sys.argv

    if len(sys.argv) > 1:
        script_path = sys.argv[1]
        try:
            times = int(times = sys.argv[2])
        except Exception as e:
            times = 1
        single_run(script_path, times)
    else:
        main()

