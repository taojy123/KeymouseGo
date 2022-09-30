from platform import system


if system() == 'Windows':
    import Event.WindowsEvents as _Event
    event_cls = _Event.WindowsEvent
    flag_multiplemonitor = _Event.numofmonitors > 1
elif system() in ['Linux', 'Darwin']:
    import Event.UniversalEvents as _Event
    event_cls = _Event.UniversalEvent
    flag_multiplemonitor = False
else:
    raise OSError("Unsupported platform '{}'".format(system()))

ScriptEvent = event_cls
ScreenWidth = _Event.SW
ScreenHeight = _Event.SH
