import asyncio
import platform

from common.ConstSetting import SETTINGS


# 协程任务调度 params作为传入列表 func作为函数
async def coroutineStart(params, func):
    semaphore = asyncio.Semaphore(SETTINGS["thread"])
    tasks = [func(param, semaphore) for param in params]
    await asyncio.gather(*tasks)


# 协程主函数
def CoroutineMain(params, func):
    # lock = asyncio.Lock()
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(coroutineStart(params, func))
