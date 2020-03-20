import smtplib
from email.mime.text import MIMEText
import email
import imaplib

SMTP_SSL_HOST = "smtp.gmail.com"
SMTP_SSL_PORT = 465
USERNAME = "SOME GMAIL"
PASSWORD = "SOME PASSWORD"
IMAP_SERVER = 'imap.gmail.com'

class Message:

    def __init__(self, subject, recipient, text, sender = USERNAME):
        self.recipient = recipient
        self.subject = subject
        self.text = text
        self.sender = sender
        self.message = MIMEText(text)
        self.message["from"] = USERNAME
        self.message["to"] = recipient
        self.message["subject"] = subject

    def asString(self):
        return self.message.as_string()

    def __str__(self):
        return "\nSUBJECT: %s\nTO: %s\nFROM: %s\nTEXT: %s\n" % (
                self.subject, self.recipient, self.sender, self.text)

    def __repr__(self):
        return self.__str__()

def sendEmails(emailList):
    
    server = smtplib.SMTP_SSL(SMTP_SSL_HOST, SMTP_SSL_PORT)
    server.login(USERNAME, PASSWORD)
    
    for message in emailList:
        server.sendmail(USERNAME, [message.recipient], message.asString())

    server.quit()

def getEmails():


    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(USERNAME, PASSWORD)
    mail.select('inbox')
    status, data = mail.search(None, 'ALL')
    mail_ids = []
    for block in data:
        mail_ids += block.split()

    msgs = []

    for i in mail_ids:
        status, data = mail.fetch(i, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1])
                mail_from = message['from']
                mail_subject = message['subject']
                if message.is_multipart():
                    mail_content = ''
                    for part in message.get_payload():
                        if part.get_content_type() == 'text/plain':
                            mail_content += part.get_payload()
                else:
                    mail_content = message.get_payload()

                msgs.append(Message(mail_subject, USERNAME, mail_content,
                    mail_from)) 

    return msgs

