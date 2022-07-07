from platform import system


if system() == 'Windows':
    import Event.WindowsEvents as _Event
    event_cls = _Event.WindowsEvent
elif system() in ['Linux', 'Darwin']:
    pass
else:
    raise OSError("Unsupported platform '{}'".format(system()))

ScriptEvent = event_cls
ScreenWidth = _Event.SW
ScreenHeight = _Event.SH
