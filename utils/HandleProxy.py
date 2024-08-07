import requests
import json
import base64
import httpx
import asyncio
import aiofiles
from common.ComMsg import ComMsg, ErrorExit
from utils.HandleCoroutine import CoroutineMain
from common.ConstSetting import SETTINGS, HTTP

# 该模块中的信息输出类
m = ComMsg()


# 获取ip列表 同步
def getIp(email, key, q):
    if email == "" or key == "":
        ErrorExit(f"email:< {email} > key:< {key} >.")
    m.changeContents("Start Init Proxy ...")
    m.printMessage("white", "MESSAGE")
    try:
        qbase64 = base64.b64encode(q.encode("utf-8")).decode("utf-8")
        fofaurl = f"http://fofa.info/api/v1/search/all?email={email}&key={key}&qbase64={qbase64}&size=10000"
        fofares = requests.get(fofaurl)

        data = json.loads(fofares.text)
        if "errmsg" in data:
            ErrorExit(data["errmsg"])
        if SETTINGS["number"] != None:
            res = [result[0] for result in data["results"]][: int(SETTINGS["number"])]
        else:
            res = [result[0] for result in data["results"]]
        m.changeContents(f"Get Socks-proxy ip and port, counts:{len(res)}.")
        m.printMessage("white", "MESSAGE")
    except Exception as e:
        ErrorExit(e)
    return res


# 代理ip中开放的端口
open_proxies = []
ip_ports = None
port_count = []


async def testPort(proxy, semaphore, lock=asyncio.Lock()):
    async with semaphore:
        ip, port = proxy.split(":")
        try:
            # 创建一个TCP socket连接
            """loop = asyncio.get_event_loop()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setblocking(False)
            await loop.sock_connect(sock, (ip, int(port)))"""
            reader, writer = await asyncio.open_connection(ip, int(port))
            # 如果连接成功，添加到开放代理列表
            async with lock:
                open_proxies.append(proxy)
                # 关闭连接
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass
        finally:
            async with lock:
                port_count.append(1)
                m.changeContents(
                    f"Start Testing Ports: {len(port_count)}/{int(len(ip_ports))}."
                )
                m.printMessage("magenta", "TESTING", refresh=True)


proxy_count = []


async def testProxy(proxy, semaphore, lock=asyncio.Lock()):
    """
    测试代理是否可用
    :param proxy: ip与端口
    :param semaphore: 并发数
    :param lock: 资源锁
    """
    async with semaphore:
        try:
            timeout = httpx.Timeout(
                connect=SETTINGS["connect"],
                read=SETTINGS["read"],
                write=SETTINGS["write"],
                pool=SETTINGS["pool"],
            )
            async with httpx.AsyncClient(
                proxies={
                    "http://": f"socks5://{proxy}",
                    "https://": f"socks5://{proxy}",
                },
                timeout=timeout,
                verify=True,
            ) as client:
                response = await client.get(
                    url="https://www.baidu.com/",
                    headers=HTTP["headers"],
                    cookies=HTTP["cookies"],
                )

                if response.status_code == 200:
                    async with lock:
                        async with aiofiles.open("proxies.txt", mode="a") as file:
                            await file.write(f"{proxy}\n")

        except Exception as e:
            pass
        finally:
            async with lock:
                proxy_count.append(1)
                m.changeContents(
                    f"Start Testing Proxy: {len(proxy_count)}/{len(open_proxies)}."
                )
                m.printMessage("magenta", "TESTING", refresh=True)
            if len(proxy_count) == len(open_proxies):
                return


def GetProxy():
    global ip_ports
    ip_ports = getIp(HTTP["proxy"]["email"], HTTP["proxy"]["key"], HTTP["proxy"]["q"])
    CoroutineMain(ip_ports, testPort)
    print("")
    CoroutineMain(open_proxies, testProxy)
    print("")
    m.changeContents(f"\033[KTesting Done.")
    m.printMessage("white", "MESSAGE")
