import configparser
import os
import winreg

'''
    [Config]
    StartHotKeyIndex
    StopHotKeyIndex
    LoopTimes
    Precision
    ExecuteSpeed
'''

conf = configparser.ConfigParser()
swapmousebuttons = True if winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                                              r'Control Panel\Mouse',
                                                              0,
                                                              winreg.KEY_READ),
                                               'SwapMouseButtons')[0] == '1' else False
swapmousemap = {'mouse left down': 'mouse right down', 'mouse left up': 'mouse right up',
                'mouse right down': 'mouse left down', 'mouse right up': 'mouse left up'}


def setdefaultconf(config):
    config.add_section('Config')
    config.set('Config', 'StartHotKeyIndex', '3')
    config.set('Config', 'StopHotKeyIndex', '6')
    config.set('Config', 'LoopTimes', '1')
    config.set('Config', 'Precision', '200')
    config.set('Config', 'ExecuteSpeed', '100')


def getconfig():
    if not os.path.exists('config.ini'):
        setdefaultconf(conf)
        conf.write(open('config.ini', 'w'))
    else:
        conf.read('config.ini')
    return conf.items('Config')


def saveconfig(newStartIndex, newStopIndex, newTimes, newPrecsion, newSpeed):
    conf.set('Config', 'StartHotKeyIndex', str(newStartIndex))
    conf.set('Config', 'StopHotKeyIndex', str(newStopIndex))
    conf.set('Config', 'LoopTimes', str(newTimes))
    conf.set('Config', 'Precision', str(newPrecsion))
    conf.set('Config', 'ExecuteSpeed', str(newSpeed))
    conf.write(open('config.ini', 'w'))
