import configparser
import os

'''
    [Config]
    StartHotKeyIndex
    StopHotKeyIndex
    LoopTimes
    Precision
    ExecuteSpeed
'''

conf = configparser.ConfigParser()


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
