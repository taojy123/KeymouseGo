#!/usr/bin/env python
#Boa:App:BoaApp

import Frame1
import wx
import time
import sys
import json


modules = {'Frame1': [1, 'Main frame of Application', u'Frame1.py']}


class BoaApp(wx.App):
    def OnInit(self):
        self.main = Frame1.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True


def main():
    application = BoaApp(0)
    application.MainLoop()


def single_run(script_path, run_times=1):
    j = 0
    while j < run_times or run_times == 0:
        j += 1
        print('===========', j, '==============')
        Frame1.RunScriptClass.run_script_once(script_path)
    print('script run finish!')


if __name__ == '__main__':

    print(sys.argv)

    if len(sys.argv) > 1:
        script_path = sys.argv[1]
        run_times = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        single_run(script_path, run_times)
    else:
        main()

