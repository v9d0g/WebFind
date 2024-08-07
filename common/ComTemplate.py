from common.ComMsg import ErrorExit
from bs4 import BeautifulSoup


# 识别模板的数组
class ComTemplate:
    # 初始化选项 是单个模板还是一个模板数组
    def __init__(self) -> None:
        pass

    def recognizeHtml(self, html: str, opt: str):
        self.html = html
        self.opt = opt
        # 获取模板目标文件路径
        self.generateTemplateTarget()
        # 按照路径逐一打开模板文件
        self.openTemplate()

    def generateTemplateTarget(self):
        import os

        try:
            if self.opt == "all":
                path = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)), "fingers"
                )
                filelist = os.listdir(path)
                filepath = []
                for i in filelist:
                    filepath.append(
                        os.path.join(
                            os.path.dirname(os.path.abspath(__file__)), "fingers", i
                        )
                    )
                self.target = filepath
                print(f"all:{filepath}")
            else:
                # with open(filename, "r") as file:
                filepath = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)), "fingers", self.opt
                )
                print(f"temp:{filepath}")
                self.target = filepath
                """
                with open(filepath, "r") as file:
                    print(file)
                """
        except Exception as e:
            ErrorExit(str(e))
        # print(self.target)

    def openTemplate(self):
        import yaml

        if type(self.target) == list:
            for path in self.target:
                # 打开yaml文件
                with open(path, "r", encoding="utf-8") as file:
                    # 获取yaml字段
                    data = dict(yaml.safe_load(file))
                    for key in list(data.keys()):
                        # 根据yaml字段名获取对应html字段
                        self.getContents(key)
            pass
        else:
            with open(self.target, "r", encoding="utf-8") as file:
                data = dict(yaml.safe_load(file))
                print(list(data.keys()))

    # TODO:直接获取标签的所有内容<div xxx="xxx">xxxx</div> 目前只能获取文本内容
    # 按照模板文件中字段 获取html中的字段
    def getContents(self, target: str):
        try:
            soup = BeautifulSoup(self.html, "html.parser")
            labels = soup.find_all(target)
            contents = [tag.text for tag in labels if tag.text.strip()]
            return contents
        except Exception as e:
            pass

    def judgeTemplate(self, contents):
        for content in contents:
            pass
        pass
