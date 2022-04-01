# cython: language_level=3
import configparser
import os
import winreg

'''
    [Config]
    StartHotKeyIndex
    StopHotKeyIndex
    RecordHotKeyIndex
    LoopTimes
    Precision
    ExecuteSpeed
    Language
'''

conf = configparser.ConfigParser()
# 是否切换主要/次要功能键
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
    config.set('Config', 'RecordHotKeyIndex', '7')
    config.set('Config', 'LoopTimes', '1')
    config.set('Config', 'Precision', '200')
    config.set('Config', 'ExecuteSpeed', '100')
    config.set('Config', 'Language', 'zh-cn')

def getconfig():
    if not os.path.exists('config.ini'):
        setdefaultconf(conf)
        conf.write(open('config.ini', 'w'))
    else:
        conf.read('config.ini')
    return dict(conf.items('Config'))


def saveconfig(newConf):
    conf.set('Config', 'StartHotKeyIndex', str(newConf['starthotkeyindex']))
    conf.set('Config', 'StopHotKeyIndex', str(newConf['stophotkeyindex']))
    conf.set('Config', 'RecordHotKeyIndex', str(newConf['recordhotkeyindex']))
    conf.set('Config', 'LoopTimes', str(newConf['looptimes']))
    conf.set('Config', 'Precision', str(newConf['precision']))
    conf.set('Config', 'ExecuteSpeed', str(newConf['executespeed']))
    conf.set('Config', 'Language', str(newConf['language']))
    conf.write(open('config.ini', 'w'))
