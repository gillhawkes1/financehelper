import os
import sys


#clear your console depending on your operating system 
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

#get your systems version
def version():
    print(sys.version)

def sayhello(name):
    print('hello, ' + name + '!')