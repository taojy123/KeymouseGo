import pyWinhook
from pyWinhook import cpyHook, HookConstants
import win32api
from Event import ScreenWidth as SW, ScreenHeight as SH, flag_multiplemonitor
from loguru import logger
import Recorder.globals as globalv
import collections
from winreg import QueryValueEx, OpenKey, HKEY_CURRENT_USER, KEY_READ
# 是否切换主要/次要功能键
swapmousebuttons = True if QueryValueEx(OpenKey(HKEY_CURRENT_USER,
                                                r'Control Panel\Mouse',
                                                0,
                                                KEY_READ),
                                        'SwapMouseButtons')[0] == '1' else False

msgdic = {0x0201: 'mouse left down', 0x0202: 'mouse left up',
          0x0204: 'mouse right down', 0x0205: 'mouse right up',
          0x0200: 'mouse move',
          0x0207: 'mouse middle down', 0x0208: 'mouse middle up',
          0x020a: 'mouse wheel',
          0x020b: 'mouse x down', 0x020c: 'mouse x up'}
datadic = {0x10000: 'x1', 0x20000: 'x2'}
MyMouseEvent = collections.namedtuple("MyMouseEvent", ["MessageName"])

record_signals = globalv.RecordSignal()


# def threadwrapper(func):
#     def wrapper(*args):
#         threading.Thread(target=func, args=args).start()
#
#     return wrapper


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
    message = event.MessageName
    if message == 'mouse wheel':
        message += ' up' if event.Wheel == 1 else ' down'
    elif message in globalv.swapmousemap and swapmousebuttons:
        message = globalv.swapmousemap[message]
    all_messages = ('mouse left down', 'mouse left up', 'mouse right down', 'mouse right up', 'mouse move',
                    'mouse middle down', 'mouse middle up', 'mouse wheel up', 'mouse wheel down',
                    'mouse x1 down', 'mouse x1 up', 'mouse x2 down', 'mouse x2 up'
                    )
    if message not in all_messages:
        return True

    pos = win32api.GetCursorPos()

    delay = globalv.current_ts() - globalv.latest_time

    # 录制鼠标轨迹的精度，数值越小越精准，但同时可能产生大量的冗余
    mouse_move_interval_ms = globalv.mouse_interval_ms or 999999

    if message == 'mouse move' and delay < mouse_move_interval_ms:
        return True

    if globalv.latest_time < 0:
        delay = 0
    globalv.latest_time = globalv.current_ts()

    if not flag_multiplemonitor:
        x, y = pos
        pos = (x / SW, y / SH)

    sevent = globalv.ScriptEvent({
        'delay': delay,
        'event_type': 'EM',
        'message': message,
        'action': pos
    })
    record_signals.event_signal.emit(sevent)
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

    all_messages = ('key down', 'key up')
    if message not in all_messages:
        return True

    key_info = (event.KeyID, event.Key, event.Extended)

    delay = globalv.current_ts() - globalv.latest_time
    if globalv.latest_time < 0:
        delay = 0
    globalv.latest_time = globalv.current_ts()

    sevent = globalv.ScriptEvent({
        'delay': delay,
        'event_type': 'EK',
        'message': message,
        'action': key_info
    })
    record_signals.event_signal.emit(sevent)
    return True


def mouse_handler(msg, x, y, data, flags, time, hwnd, window_name):
    try:
        name = msgdic[msg]
        if name == 'mouse wheel':
            name = name + (' up' if data > 0 else ' down')
        elif name in ['mouse x down', 'mouse x up']:
            name = name.replace('x', datadic[data])
        on_mouse_event(MyMouseEvent(name))
    except KeyError as e:
        logger.debug('Unknown mouse event, keyid {0}'.format(e))
    finally:
        return True


# @threadwrapper
def setuphook(commandline=False):
    hm = pyWinhook.HookManager()
    if not commandline:
        # 使用一般的HookMouse无法捕获鼠标侧键操作，因此采用cpyHook捕获鼠标操作
        cpyHook.cSetHook(HookConstants.WH_MOUSE_LL, mouse_handler)
    hm.KeyAll = on_keyboard_event
    hm.HookKeyboard()
    # Wait Forever
    # pythoncom.PumpMessages()
