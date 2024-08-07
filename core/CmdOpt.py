import getopt
import sys
import time

from core.ThreadScan import *
from common.ConstShow import HELP
from utils.HandleFlie import ReadFile, SaveFile
from utils.HandleCoroutine import CoroutineMain
from utils.HandleProxy import GetProxy
from common.ConstSetting import SETTINGS, HTTP
from common.ConstData import ALIVECOUNT, SUCCESSMESSAGE, OPTIONS
from common.ComMsg import ComMsg


# 公有消息类
message = ComMsg()


def sortOptions(opts: list):
    arg_priority = {
        "-H": 0xFFF,  # 程序开始前
        "-p": 0xFEF,  # 程序运行-探测前
        "-P": 0xFED,  # 程序运行-探测前
        "-R": 0xFEF,  # 程序运行-探测中
        "-r": 0xFEE,  # 程序运行-探测中
        "-u": 0xFED,  # 程序运行-探测中
        "-S": 0xFDF,  # 程序运行-探测后
    }

    temp = {}
    for opt in opts:
        if len(opt[0]) > 2:
            opt = (opt[0][1:3], opt[1])
        if opt[0] in arg_priority:
            priority = arg_priority[opt[0]]
            temp[priority] = opt

    # 降序排序
    res = {k: temp[k] for k in sorted(temp, reverse=True)}
    return res


def procOptions(args, SETTINGS=SETTINGS, HTTP=HTTP):
    if args[0] == "-H":
        print(HELP)
    elif args[0] == "-p" or args[0] == "-P":
        if args[1] != "" and args[0] == "-p":
            HTTP["proxy"]["url"] = args[1]
            OPTIONS["proxy"] = args[1]
        else:
            try:
                if os.path.exists("proxies.txt"):
                    message.changeContents(f"The File proxies.txt Exists.")
                    message.printMessage("white", "MESSAGE")
                else:
                    message.changeContents(f"The File proxies.txt Not Found.")
                    message.printMessage("yellow", "WARNING")
                    # TODO: 优化代理获取 代理池
                    GetProxy()  # 生成文件
            except Exception as e:
                ErrorExit(e)
    elif args[0] == "-u":
        urls, count, res_count = ReadFile(args[1])
        start_time = time.time()
        CoroutineMain(urls, ScanWeb)
        end_time = time.time()
        message.changeContents(
            f"Mission Accomplished Spend \033[32m{int(end_time-start_time)}s\033[0m: Input:{count} Useful:{res_count} \033[32mAlive:{len(ALIVECOUNT)}\033[0m."
        )
        message.printMessage("white", "MESSAGE")
    elif args[0] == "-S":
        SETTINGS["save"] = True
    elif args[0] == "-r" or args[0] == "-R":
        if args[0] == "-r":
            OPTIONS["recognize"] = args[1]
            SETTINGS["recognize"] = args[1]
        else:
            OPTIONS["recognize"] = "all"
            SETTINGS["recognize"] = "all"


# 总体流程处理
def Command(argv):
    try:
        options, _args = getopt.getopt(
            argv,
            "HSPRr:p:u:",
            ["Help", "Save", "Proxy", "Recognize", "recognize=", "proxy=", "url="],
        )
        options = sortOptions(options)
    except getopt.GetoptError as e:
        ErrorExit(str(e))
    try:
        for _k, v in options.items():
            procOptions(v)
        if SETTINGS["save"]:
            SaveFile(SUCCESSMESSAGE, "result.xlsx")
            SaveFile({**IGNOREMESSAGE, **FAILEDMESSAGE}, "error.xlsx")
    except:
        sys.exit(0)
    return
