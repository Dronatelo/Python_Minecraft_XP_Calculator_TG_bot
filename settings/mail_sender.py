from calculate_file import xlms_path_now, get_file_now_name

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders

from random import randint

#create passowrd
def get_value():
    value = randint(100000000,999999999)
    return value

mails = ["********.com","*********.com"]   

def send_mail_file(send_from,mail,subject,text,isTls=True):
    try:
        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = mail
        msg['Date'] = formatdate(localtime = True)
        msg['Subject'] = subject
        msg.attach(MIMEText(text))
        
        login = "************"
        password_mail = "****************"

        part = MIMEBase('application', "octet-stream")
        #переделать функцию , чтобы отправлять определённые файлы себе
        part.set_payload(open(xlms_path_now(), "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{get_file_now_name()}"')
        msg.attach(part)

        smtp = smtplib.SMTP("smtp.gmail.com",587)
        if isTls:
            smtp.starttls()
        smtp.login(login,password_mail)
        if mail in mails:
            smtp.sendmail(send_from, mail, msg.as_string())
            smtp.quit()
        else:
            return "Ваша почта не в списке!"
    except Exception as ex:
        return f"{ex}"

def send_mail_password(mail):
    try:
        #get password
        password = get_value()
        #connect to server mail
        sender = "**************"
        password_mail = "**************"

        #settings for mail
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(sender,password_mail)
        
        if mail in mails:
            server.sendmail(sender,mail,f"Subject: PASSWORD\n{password}")
            return password
        else:
            return "Ваша почта не в списке!"
    except Exception as ex:
        return f"{ex}\n check login or password!"

