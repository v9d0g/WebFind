import asyncio
import httpx
import os
import random

from common.ComMsg import ComMsg, ErrorExit
from common.ConstSetting import SETTINGS, HTTP
from common.ConstData import FAILEDMESSAGE, SUCCESSMESSAGE, ALIVECOUNT
from utils.HandleResponse import *
from utils.HandleFlie import *
from utils.HandleProxy import GetProxy

# 公有锁
lock = asyncio.Lock()
# 公有对象 以免多协程多次创建
m = ComMsg()


def judgeFinger(html):
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "../", "common", "fingers"
    )
    try:
        """循环获取指纹文件名"""
        for filename in os.listdir(path):  # filename = HjHr.yaml
            """循环获取每个指纹文本中 需要判断的标签 属性"""
            for ruleTags, ruleProperties in ReadYaml(
                path + "\\" + filename, opt1=None
            ).items():
                # ruleTags yaml文件中 每个需要判断的标签
                # ruleTags= img
                """循环需要判断的标签 的属性"""
                for (
                    ruleProperty
                ) in ruleProperties:  # rules yaml文件中 ruleTags中对应的判断条件
                    # ruleProperties={'src': {'and': {'regular': [None]}, 'or': {'regular': ['^/images/hcm/themes/default/login']}}}
                    if (
                        judgeEnds(
                            # getCont()=(*)=list[<ruleTags ruleProperty="*">]
                            getCont(html, ruleTags, ruleProperty),
                            # ReadYaml()=(*)=dict{ruleTags:ruleProperty:{*}}
                            ReadYaml(path + "\\" + filename, ruleTags, ruleProperty),
                        )
                        == True
                    ):
                        return filename[:-5]
    except Exception as e:
        ErrorExit(e)


# 修改后的 scanWeb 函数
async def ScanWeb(url, semaphore, SETTINGS=SETTINGS, HTTP=HTTP):
    async with semaphore:
        try:
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
                timeout=timeout, verify=False, follow_redirects=True, proxies=proxies
            ) as client:
                response = await client.get(
                    url=url,
                    headers=HTTP["headers"],
                    cookies=HTTP["cookies"],
                )
                if response.status_code in SETTINGS["allow"]:
                    # 加锁 保证多协程不会出现竞争
                    async with lock:
                        code = response.status_code
                        title = getCont(response.text, "title")
                        finger = judgeFinger(response.text)
                        m.chgCont(f"{url}" + " ")
                        m.addTags(f"{code}", "yellow")
                        if SETTINGS["detail"]:
                            # 识别指纹
                            m.addTags(finger, "green", "R")
                            m.addTags(title, "black", "R")
                        m.printMsg("green", "Alive")
                        ALIVECOUNT.append("ok")
                        SUCCESSMESSAGE.update(
                            {
                                url: {
                                    "code": f"{code}",
                                    "title": f"{title}",
                                    "finger": f"{finger}",
                                }
                            }
                        )
        # 其余错误
        except Exception as e:
            FAILEDMESSAGE.update({url: f"{e}"})


# 用于运行多个协程任务
"""
async def Start(urls):
    semaphore = asyncio.Semaphore(SETTINGS["thread"])
    tasks = [scanWeb(url, semaphore) for url in urls]
    await asyncio.gather(*tasks)
"""
