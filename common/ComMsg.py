from datetime import datetime

from common.ConstShow import HELP


class ComMsg:
    def __init__(self, content=None) -> None:
        self.content = content

    def chgCont(self, content):
        self.content = content

    def addTags(self, tag, option, direct="L"):
        colors = {
            "red": "\033[31m",
            "green": "\033[32m",
            "yellow": "\033[33m",
            "blue": "\033[34m",
            "magenta": "\033[35m",
            "cyan": "\033[36m",
            "white": "\033[37m",
            "black": "\033[90m",
            "bold": "\033[1m",
            "reset": "\033[0m",
        }
        if direct == "L":
            self.content = f"[{colors[option]}{tag}{colors['reset']}] " + self.content
        else:
            self.content = self.content + f"[{colors[option]}{tag}{colors['reset']}]"

    def printMsg(self, tags_color, tagscontent, refresh=False):
        self.addTags(tagscontent, tags_color)
        self.addTags(datetime.now().strftime("%H:%M:%S"), "blue")
        if refresh:
            print(f"{self.content:<50}", end="\r")
        # 重置
        else:
            print(f"{self.content}")
        self.chgCont("")


# 出现错误 输出错误信息并退出
def ErrorExit(message):
    m = ComMsg(message)
    m.printMsg("red", "Error")
    print(HELP)
    import sys

    sys.exit(0)
