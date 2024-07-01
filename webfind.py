import sys

from core.CmdOpt import Command
from common.ConstShow import LOGO

if __name__ == "__main__":
    print(LOGO)
    Command(sys.argv[1:])
