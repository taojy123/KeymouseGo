class Extension:
    def __init__(self):
        pass

    # 每次录制事件后需要做的事,返回True保存事件
    def onrecord(self, event, currentindex):
        return True

    # 每次脚本执行前需要做的事,返回True执行本行脚本
    def onbeforeeachloop(self, currentloop):
        # print('beforeloop', currentloop)
        return True

    # 每行脚本执行前需要做的事,返回True执行本行脚本
    def onrunbefore(self, event, currentindex):
        # print('runbefore', currentindex)
        return True

    # 每行脚本执行后需要做的事
    def onrunafter(self, event, currentindex):
        # print('runafter', currentindex)
        pass

    # 每次脚本全部执行完后需要做的事
    def onaftereachloop(self, currentloop):
        # print('afterloop', currentloop)
        pass
