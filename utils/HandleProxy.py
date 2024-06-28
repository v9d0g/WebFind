import requests
import json
import base64

from common.ComMsg import ComMsg, ErrorExit
from common.ConstSetting import HTTP

# 该模块中的信息输出类
m = ComMsg()


# 获取ip列表
def getIp(email, key, q):
    if email == "" or key == "":
        ErrorExit(f"email:{email} key:{key} Is Wrong.")
    m.chgCont("proxies.txt not Found.")
    m.addTags("Warn", "yellow")
    m.printMsg()
    m.chgCont("Start Init Proxy ...")
    m.addTags("Message", "white")
    m.printMsg()
    try:
        qbase64 = base64.b64encode(q.encode("utf-8")).decode("utf-8")
        fofaurl = f"http://fofa.info/api/v1/search/all?email={email}&key={key}&qbase64={qbase64}&size=10000"
        fofares = requests.get(fofaurl)

        data = json.loads(fofares.text)
        res = [result[0] for result in data["results"]]
        m.chgCont(f"Get Socks5 ip and port, counts:{len(res)}.")
        m.addTags("Message", "white")
        m.printMsg()
    except Exception as e:
        ErrorExit(e)
    return res


import socket
import concurrent.futures

# 代理ip中开放的端口
open_proxies = []


def testPort(proxy):
    # print(proxy)
    ip, port = proxy.split(":")
    try:
        # 创建一个TCP socket连接
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)  # 设置超时时间为2秒

        # 尝试连接端口
        result = sock.connect_ex((ip, int(port)))
        m.chgCont(f"Testing port open: {proxy}.")
        m.addTags("Message", "white")
        m.printMsg(refresh=True)
        # 如果端口开放，添加到开放代理列表
        if result == 0:
            open_proxies.append(proxy)

        sock.close()
    except socket.error:
        pass


# 设置线程池数量为10


from concurrent.futures import ThreadPoolExecutor
import warnings

warnings.filterwarnings("ignore")


def testProxy(proxy):
    try:
        response = requests.get(
            "https://www.baidu.com/",
            proxies={"http": f"socks5://{proxy}", "https": f"socks5://{proxy}"},
            timeout=6,
            verify=False,
        )
        if response.status_code == 200:
            m.chgCont(f"Testing proxy: {proxy}.")
            m.addTags("Message", "white")
            m.printMsg(refresh=True)
            with open("proxies.txt", "a") as file:
                file.write(f"{proxy}\n")
    except:
        pass


def GetProxy():
    max_workers = 100

    # 使用线程池测试端口
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(
            testPort,
            getIp(HTTP["proxy"]["email"], HTTP["proxy"]["key"], HTTP["proxy"]["q"]),
        )

    # 验证可用
    m.chgCont(f"Proxy ip:port test done.")
    m.addTags("Message", "white")
    m.printMsg(refresh=True)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(testProxy, open_proxies)
    m.chgCont("proxies.txt is saved.")
    m.addTags("Message", "white")
    m.printMsg()
