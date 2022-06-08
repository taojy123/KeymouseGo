from UIFunc import ScriptEvent, PlayPromptTone


class Extension:
    def __init__(self, runtimes, speed, thd=None, swap=None):
        self.runtimes = runtimes
        self.speed = speed
        self.thd = thd
        self.swap = swap

    # 脚本执行前需要做的事
    def onbeginp(self):
        PlayPromptTone(1, 0).start()

    # 每次录制事件后需要做的事,返回True保存事件
    def onrecord(self, event, currentindex):
        return True

    # 每次脚本执行前需要做的事,返回True执行本行脚本
    def onbeforeeachloop(self, currentloop):
        return True

    # 每行脚本执行前需要做的事,返回True执行本行脚本
    def onrunbefore(self, event, currentindex):
        return True

    # 每行脚本执行后需要做的事
    def onrunafter(self, event, currentindex):
        pass

    # 每次脚本全部执行完后需要做的事
    def onaftereachloop(self, currentloop):
        pass

    # 全部循环全部执行完后需要做的事
    def onendp(self):
        PlayPromptTone.play_end_sound()
