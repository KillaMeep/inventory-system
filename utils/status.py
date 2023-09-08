from termcolor import colored,cprint
import os
os.system('color')

#create a status class for better formatting in print statements
class status():
    OK = colored('[OK]','green')
    WARN = colored('[WARN]','yellow')
    ERROR = colored('[ERROR]','red')
    INFO = colored('[INFO]','magenta')
