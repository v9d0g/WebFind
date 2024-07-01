import pandas as pd
import yaml
import os
import random

from common.ComMsg import ComMsg, ErrorExit

m = ComMsg()


# 处理重复url以及前缀
def handUrls(urls):
    # 使用一个集合来存储去掉前缀后的URL
    unique_urls = set()
    res = []

    for url in urls:
        # 默认添加http://
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        # 去掉前缀
        if url.startswith("https://"):
            url_no_prefix = url[8:]
        elif url.startswith("http://"):
            url_no_prefix = url[7:]
        else:
            url_no_prefix = url

        # 如果这个去掉前缀后的URL不在集合中，则添加到结果中
        if url_no_prefix not in unique_urls:
            unique_urls.add(url_no_prefix)
            res.append(url)
        # 如果这个去掉前缀后的URL已经在集合中，而且当前URL是http://前缀的，就跳过
        elif url.startswith("http://"):
            continue
        # 如果这个去掉前缀后的URL已经在集合中，而且当前URL是https://前缀的，就替换掉之前的http://前缀的
        elif url.startswith("https://"):
            res = [
                u
                for u in res
                if not (u.startswith("http://") and u[7:] == url_no_prefix)
            ]
            res.append(url)

    return res, len(res)


# 处理ip 8.8.8.8/24 8.8.8.8-255 8.8.8.8三种方式
def handIp(ip):
    pass


# 读取url.txt 返回处理后的列表 以及输入时的个数和最终个数
def ReadFile(filename):
    temp = []
    # 结果
    res = []
    all_count = 0
    try:
        m.chgCont(f"Load {filename}.")
        m.printMsg("white", "Message")
        with open(filename, "r") as file:
            for line in file:
                stripped_line = line.strip()
                if not stripped_line:  # 跳过空行
                    continue
                temp.append(stripped_line)
                all_count += 1
            # 排除重复后的列表以及个数
            res, res_count = handUrls(temp)
        return res, all_count, res_count
    # 没有找到
    except FileNotFoundError:
        ErrorExit(f"{filename} is not found or is not a text file.")
    # 目录
    except IsADirectoryError:
        ErrorExit(f"{filename} is a directory, not a file.")
    # 读取错误
    except IOError:
        ErrorExit(f"Error reading file: {filename}.")
    except Exception as e:
        ErrorExit(f"Unknown error: {e}.")


def ReadProxy():
    try:
        with open("proxies.txt", "r") as file:
            proxies = file.readlines()
            if proxies:
                return random.choice(proxies).strip()
            else:
                ErrorExit("proxies.txt has no content.")
    except FileNotFoundError:
        ErrorExit("proxies.txt not found.")


# 保存文件为excel
def SaveFile(inputs):
    try:
        if type(inputs) == dict:
            data = []
            filename = "output.xlsx"
            for k, v in inputs.items():
                entry = {"url": k}
                entry.update(v)
                data.append(entry)
            df = pd.DataFrame(data)
            df.to_excel(filename, index=True)
            m.chgCont(f"The file \033[32m{filename}\033[0m is saved.")
            m.printMsg("white", "Message")
        else:
            m.chgCont(f"{inputs} is not suitable.")
            m.printMsg("red", "Error")
    except Exception as e:
        ErrorExit(e)


# 根据opt读取yaml文件内容
def ReadYaml(path, opt1, opt2=None):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    with open(path, "r") as file:
        data = yaml.safe_load(file)
    if opt1 != None:
        if opt2 != None:
            return data[opt1][opt2]
        return data[opt1]

    else:
        return data
