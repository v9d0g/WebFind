import getopt
import sys
import platform

from core.ThreadScan import *
from common.ConstShow import HELP, LOGO
from utils.HandleFlie import ReadFile, SaveFile
from common.ConstSetting import SETTINGS, HTTP
from common.ConstData import ALIVECOUNT, SUCCESSMESSAGE
from common.ComMsg import ComMsg

# 公有消息类
m = ComMsg()


# 读取输入的指令集
def sortOpt(opts):
    # 定义参数及其优先级
    arg_priority = {
        "-H": 0xFFF,  # 帮助
        "-p": 0xFEF,  # 代理
        "-P": 0xFED,
        "-C": 0xFEC,  # 显示状态码
        "-D": 0xFEB,  # 保存存活 输出excel貌似好一点
        "-u": 0xFEA,  # 显示细节 指纹以及title
        "-S": 0xFE9,  # 指定url
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
        if platform.system() == "Windows":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        loop = asyncio.get_event_loop()
        # 读取文件 并返回url列表 以及url计数
        urls, count, res_count = ReadFile(args[1])
        # 开始读取txt文件中的 url
        loop.run_until_complete(Start(urls))

        m.chgCont(
            f"Mission Accomplished: Input:{count} Useful:{res_count} \033[32mAlive:{len(ALIVECOUNT)}\033[0m."
        )
        m.addTags("Message", "white")
        m.printMsg()
    elif args[0] == "-C":
        SETTINGS["code"] = True
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

        # print(HTTP["proxy"]["url"] )


# 总体流程处理
def Command(argv):
    print(LOGO)
    # 获取命令参数
    try:
        opts, _args = getopt.getopt(
            argv,
            "HCSDPp:u:",
            ["help", "code", "save", "detail", "proxy", "Proxy=", "Url="],
        )
        opts = sortOpt(opts)
        # print(f"OPTS:{opts}")
    except getopt.GetoptError as e:
        m.chgCont(str(e))
        m.addTags("Error", "red")
        m.printMsg()
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
