import os
import sys

#class util():

def clear():
    mysystem = sys.platform
    #myos = os.name
    clear = ''
    if mysystem == 'darwin' or mysystem == 'linux':
        clear = 'clear'
    elif mysystem == 'win32' or mysystem == 'win64':
        clear = 'cls'
    else:
        return False
    os.system(clear)

def version():
    print(sys.version)

def sayhello(name):
    print('hello, ' + name + '!')