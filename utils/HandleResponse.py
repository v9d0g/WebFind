import re
from bs4 import BeautifulSoup


# 可以获取html中<opt1 opt2="的内容">或者<opt1>的内容</opt1>
# 返回列表
def getCont(html, opt1, opt2=None):
    try:
        soup = BeautifulSoup(html, "html.parser")
        # 使用 BeautifulSoup 解析 HTML 内容
        if opt2 is None:
            if opt1 == "title":
                # 获取页面的 title
                title = soup.title.string.strip() if soup.title else None
                if title == None:
                    return "暂无"
                return title
        else:
            # 获取页面中所有 <tag> 标签的 <attribute> 属性
            tags = soup.find_all(opt1, {opt2: True})
            tag = [tag[opt2] for tag in tags if tag.get(opt2)]
            return tag

    except Exception as e:
        # print(f"Error extracting content: {e} {html}")
        return "暂无"


def judgeAnd(html, yaml):
    time = len(yaml["and"]["regular"])
    try:
        for v in yaml["and"]["regular"]:
            # 该标签-属性 不需要判断
            if v == None:
                return True
            else:
                pattern = re.compile(v)
                for i in html:
                    if pattern.search(i):
                        time -= 1
                    else:
                        pass
                if time == 0:
                    return True
                else:
                    return False
    except Exception as e:
        print(f"{e}")


def judgeOr(html, yaml):
    try:
        for v in yaml["or"]["regular"]:
            # 该标签-属性 不需要判断
            if v == None:
                return True
            else:
                pattern = re.compile(v)
                for i in html:
                    if pattern.search(i):
                        return True
                return False
    except Exception as e:
        print(f"{e}")


def judgeEnds(html, yaml):
    try:
        res_and = judgeAnd(html, yaml)

        res_or = judgeOr(html, yaml)
        return res_and and res_or
        # 只要满足
    except Exception as e:
        print(f"Judge wrong:{e}")
