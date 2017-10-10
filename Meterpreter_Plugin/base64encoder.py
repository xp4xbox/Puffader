'''
Simple Program To Encode Shellcode to base64 by xp4xbox
https://github.com/xp4xbox/Puffader
'''

import base64

# raw shellcode (eg. xr8\x02...)
shellcode = ""

# print shellcode as base64
print base64.b64encode(shellcode)
