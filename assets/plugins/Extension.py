from UIFunc import ScriptEvent


class Extension:
    def __init__(self, runtimes, speed, thd=None, swap=None):
        self.runtimes = runtimes
        self.speed = speed
        self.thd = thd
        self.swap = swap

    # 腳本執行前需要做的事
    def onbeginp(self):
        pass

    # 每次錄制事件後需要做的事,返回True保存事件
    def onrecord(self, event, currentindex):
        return True

    # 每次腳本執行前需要做的事,返回True執行本行腳本
    def onbeforeeachloop(self, currentloop):
        return True

    # 每行腳本執行前需要做的事,返回True執行本行腳本
    def onrunbefore(self, event, currentindex):
        return True

    # 每行腳本執行後需要做的事
    def onrunafter(self, event, currentindex):
        pass

    # 每次腳本全部執行完後需要做的事
    def onaftereachloop(self, currentloop):
        pass

    # 全部循環全部執行完後需要做的事
    def onendp(self):
        pass
