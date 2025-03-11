import enum


class State(enum.IntEnum):
    IDLE = 0
    SETTING_HOT_KEYS = 1
    RUNNING = 2
    RECORDING = 3
    PAUSE_RUNNING = 4
    PAUSE_RECORDING = 5
