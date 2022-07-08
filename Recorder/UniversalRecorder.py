from pynput import mouse, keyboard
from Event import ScreenWidth as SW, ScreenHeight as SH
import Recorder.globals as globalv

record_signals = globalv.RecordSignal()

buttondic = {mouse.Button.left: 'left',
             mouse.Button.right: 'right',
             mouse.Button.middle: 'middle'
             }


def get_delay(message):
    delay = globalv.current_ts() - globalv.latest_time

    # 录制鼠标轨迹的精度，数值越小越精准，但同时可能产生大量的冗余
    mouse_move_interval_ms = globalv.mouse_interval_ms or 999999

    if message == 'mouse move' and delay < mouse_move_interval_ms:
        return -1

    if globalv.latest_time < 0:
        delay = 0
    globalv.latest_time = globalv.current_ts()
    return delay


def get_mouse_event(x, y, message):
    tx = x / SW
    ty = y / SH
    tpos = (tx, ty)
    delay = get_delay(message)
    if delay < 0:
        return None
    else:
        return globalv.ScriptEvent({
            'delay': delay,
            'event_type': 'EM',
            'message': message,
            'action': tpos,
            'addon': None
        })


def on_move(x, y):
    event = get_mouse_event(x, y, 'mouse move')
    if event:
        record_signals.event_signal.emit(event)


def on_click(x, y, button, pressed):
    message = 'mouse {0} {1}'.format(buttondic[button],
                                     'down' if pressed else 'up')
    event = get_mouse_event(x, y, message)
    if event:
        record_signals.event_signal.emit(event)


def on_scroll(x, y, dx, dy):
    message = 'mouse wheel {0}'.format('down' if dy < 0 else 'up')
    event = get_mouse_event(x, y, message)
    if event:
        record_signals.event_signal.emit(event)


def get_keyboard_event(key, message):
    delay = get_delay(message)
    if delay < 0:
        return None
    else:
        try:
            event = globalv.ScriptEvent({
                'delay': delay,
                'event_type': 'EK',
                'message': message,
                'action': (key.vk, key.char, 0),
                'addon': None
            })
        except AttributeError:
            event = globalv.ScriptEvent({
                'delay': delay,
                'event_type': 'EK',
                'message': message,
                'action': (key.value.vk, key.name, 0),
                'addon': None
            })
        return event


def on_press(key):
    event = get_keyboard_event(key, 'key down')
    if event:
        record_signals.event_signal.emit(event)


def on_release(key):
    event = get_keyboard_event(key, 'key up')
    if event:
        record_signals.event_signal.emit(event)


def setuphook(commandline=False):
    if not commandline:
        mouselistener = mouse.Listener(
            on_move=on_move,
            on_scroll=on_scroll,
            on_click=on_click
        )
        mouselistener.start()
    keyboardlistener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    )
    keyboardlistener.start()
