import getopt
import sys

from core.ThreadScan import *
from common.ConstShow import HELP, LOGO
from utils.HandleFlie import ReadFile, SaveFile
from utils.HandleCoroutine import CoroutineMain
from utils.HandleProxy import GetProxy
from common.ConstSetting import SETTINGS, HTTP
from common.ConstData import ALIVECOUNT, SUCCESSMESSAGE
from common.ComMsg import ComMsg

# 公有消息类
m = ComMsg()


# 读取输入的指令集
def sortOpt(opts):
    # 定义参数及其优先级
    arg_priority = {
        "-H": 0xFFF,
        "-p": 0xFEF,
        "-P": 0xFED,
        "-D": 0xFEC,
        "-u": 0xFEB,
        "-S": 0xFEA,
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
    # print(f"res:{res}")
    return res


# 排序后的输入指令集 for
def procOpt(args, SETTINGS=SETTINGS, HTTP=HTTP):
    if args[0] == "-H":
        print(HELP)
    elif args[0] == "-u":
        # 读取文件 并返回url列表 以及url计数
        urls, count, res_count = ReadFile(args[1])
        CoroutineMain(urls, ScanWeb)
        m.chgCont(
            f"Mission Accomplished: Input:{count} Useful:{res_count} \033[32mAlive:{len(ALIVECOUNT)}\033[0m."
        )
        m.printMsg("white", "Message")
    elif args[0] == "-S":
        SETTINGS["save"] = True
    elif args[0] == "-D":
        SETTINGS["detail"] = True
    elif args[0] == "-p" or args[0] == "-P":
        # auto proxy
        SETTINGS["proxy"] = True
        # 有参数 无参数为None
        if args[1] != "" and args[0] == "-p":
            HTTP["proxy"]["url"] = args[1]
        # 无参数 自动获取
        else:
            try:
                if os.path.exists("proxies.txt"):
                    m.chgCont(f"The File proxies.txt Exists.")
                    m.printMsg("white", "Message")
                    HTTP["proxy"]["url"] = "use file"
                else:
                    m.chgCont(f"The File proxies.txt Not Found.")
                    m.printMsg("yellow", "Warning")
                    GetProxy()  # 生成文件
            except Exception as e:
                ErrorExit(e)


# 总体流程处理
def Command(argv):
    # 获取命令参数
    try:
        opts, _args = getopt.getopt(
            argv,
            "HSDPp:u:",
            ["Help", "Save", "Detail", "Proxy", "proxy=", "url="],
        )
        opts = sortOpt(opts)
        # print(f"OPTS:{opts}")
    except getopt.GetoptError as e:
        m.chgCont(str(e))
        m.printMsg("red", "Error")
        print(HELP)
        # sys.exit(1)

    # 处理参数
    try:
        # print(f"SORTEDOPTS:{opts}")
        for _k, v in opts.items():
            procOpt(v)
        if SETTINGS["save"]:
            # print(SUCCESSMESSAGE)
            SaveFile(SUCCESSMESSAGE)
    # loop.close()
    except:
        sys.exit(0)
    return
