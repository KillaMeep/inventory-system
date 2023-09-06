from termcolor import colored,cprint
import os
os.system('color')

class status():
    OK = colored('[OK]','green')
    WARN = colored('[WARN]','yellow')
    ERROR = colored('[ERROR]','red')
    INFO = colored('[INFO]','magenta')
