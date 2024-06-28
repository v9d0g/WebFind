import os

from utils.HandleFlie import ReadYaml

# 构建相对路径
# path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../", "settings.yaml")

SETTINGS = ReadYaml("../settings.yaml", "SETTINGS")

HTTP = ReadYaml("../settings.yaml", "HTTP")
