import asyncio
import httpx

from common.ComMsg import ComMsg, ErrorExit
from common.ConstSetting import SETTINGS, HTTP
from common.ConstData import FAILEDMESSAGE, IGNOREMESSAGE, SUCCESSMESSAGE, ALIVECOUNT
from common.ComTemplate import ComTemplate
from utils.HandleResponse import *
from utils.HandleFlie import *

# 公有锁
lock = asyncio.Lock()
# 公有对象 以免多协程多次创建
m = ComMsg()
# 公有模板类
T = ComTemplate()


"""
from tenacity import retry, stop_after_attempt, wait_fixed
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
"""


async def ScanWeb(url, semaphore, SETTINGS=SETTINGS, HTTP=HTTP):
    async with semaphore:
        try:
            if (
                SETTINGS["connect"] == None
                and SETTINGS["read"] == None
                and SETTINGS["write"] == None
                and SETTINGS["pool"] == None
            ):
                timeout = None
            else:
                timeout = httpx.Timeout(
                    connect=SETTINGS["connect"],
                    read=SETTINGS["read"],
                    write=SETTINGS["write"],
                    pool=SETTINGS["pool"],
                )
            # 发送http请求
            # verify忽略证书验证
            # follow_redirects跟随重定向
            if SETTINGS["proxy"]:  # 开启代理的情况
                if HTTP["proxy"]["url"] != "" and HTTP["proxy"]["url"] != None:
                    try:
                        proxy = HTTP["proxy"]["url"]
                    except Exception as e:
                        ErrorExit(e)
                # 无参数 自动获取
                else:
                    proxy = ReadProxy()

                proxies = {
                    "http://": f"socks5://{proxy}",
                    "https://": f"socks5://{proxy}",
                }
            else:
                proxies = None
            async with httpx.AsyncClient(
                timeout=timeout,
                verify=False,
                follow_redirects=SETTINGS["redirect"],
                proxies=proxies,
                http2=True,
            ) as client:
                headers = HTTP["headers"]
                cookies = HTTP["cookies"]
                # TODO:随机User-Agent
                headers["User-Agent"] = random.choice(HTTP["headers"]["User-Agent"])
                response = await client.get(
                    url=url,
                    headers=headers,
                    cookies=cookies,
                )
                code = response.status_code
                title = getCont(response.text, "title")
                size = int(len(response.content) / 1024)
                if response.status_code in SETTINGS["allow"]:
                    if SETTINGS["recognize"] != False:
                        T.recognizeHtml(response.text, SETTINGS["recognize"])
                        # T.chgTemplateOpt(SETTINGS["recognize"])
                        # T.judgeTemplate(response.text)
                        # m.addTags("探测结果", "green", "R")
                        pass
                    m.changeContents(f"{url}" + " ")
                    m.addTags(f"{code}", "yellow")
                    m.addTags(f"{title} {size}KB", "black", "R")
                    ALIVECOUNT.append("ok")
                    SUCCESSMESSAGE.update(
                        {
                            url: {
                                "状态码": f"{code}",
                                "标题": f"{title}",
                                "模板匹配": "无",
                            }
                        }
                    )
                    m.printMessage("green", "ALIVE")
                else:
                    m.changeContents(f"{url}" + " ")
                    m.addTags(f"{code}", "yellow")
                    m.addTags(f"{title} {size}KB", "black", "R")
                    m.printMessage("white", "IGNORE")
                    IGNOREMESSAGE.update(
                        {
                            url: {
                                "状态码": f"{code}",
                                "标题": f"{title}",
                                "模板匹配": "无",
                            }
                        }
                    )
        except Exception as e:
            m.changeContents(f"{url} ")
            m.addTags(f"{e}", "red", "R")
            m.printMessage("red", "ERROR")
            FAILEDMESSAGE.update(
                {
                    url: {
                        "状态码": f"无法连接",
                        "标题": f"{e}",
                        "模板匹配": f"无",
                    }
                }
            )
