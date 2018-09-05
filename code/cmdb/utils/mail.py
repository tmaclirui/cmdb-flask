#encoding: utf-8
import smtplib
from email.mime.text import MIMEText
import email.utils
from datetime import datetime

SERVER_ADDR = 'smtp.163.com'
SERVER_PORT = 25
USER = '18393648073@163.com'
PASSWORD = 'lirui213'

def send_mail(to, message, subject=u'CMDB告警'):
    if not isinstance(to, list):
        to = [to]

    _smtp_server = smtplib.SMTP(SERVER_ADDR, SERVER_PORT)
    _smtp_server.ehlo()
    _smtp_server.starttls()
    _smtp_server.login(USER, PASSWORD)
    _smtp_server.set_debuglevel(True)

    _msg = MIMEText(message, 'html', 'utf-8')
    _msg['Subject'] = subject
    _msg['From'] = USER
    _msg['To'] = '; '.join(to)
    _msg['Date'] = datetime.now().strftime('%Y-%d-%m %H:%M:%S')

    _smtp_server.sendmail(USER, to, _msg.as_string())
    _smtp_server.quit()


if __name__ == '__main__':
    send_mail('717810674@qq.com', u'测试')
