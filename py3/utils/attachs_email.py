# !/usr/bin/python
# coding:utf-8

import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class MailSender():

    def __init__(self):
        self.username = "BI"
        self.password = "xxxxx"
        self.server = smtplib.SMTP("postbox.jianke.com:25")

    def login(self):
        self.server.login(self.username, self.password)

    def add_attachment(self, filename, filepath):
        '''
        可接收多个文件 作为附件
        '''
        attachments = []
        att = MIMEText(open(filepath, 'rb').read(), 'base64', 'UTF-8')
        att["Content-Type"] = 'application/octet-stream'
        att.add_header('Content-Disposition', 'attachment',
                       filename=('gbk', '', filename) )
        encoders.encode_base64(att)
        attachments.append(att)
        return attachments

    def send_email(self):
        msg = MIMEMultipart()
        today = datetime.today().strftime('%Y%m%d')
        body = '大数据组：{}-天猫爬虫数据(自动发送)'.format(today)
        emailfrom = "BI@jianke.com"
        #emailto = ["liling1@jianke.com"]
        emailto = ["liling1@jianke.com", "chenchujun@jianke.com",
                   "zhengbenyu@jianke.com", "zhangxiaoxiao@jianke.com",
                   "yangxiaohuan@jianke.com"]

        msg["From"] = emailfrom
        msg["To"] =  ";".join(emailto)
        msg["Subject"] = body

        files = os.listdir(os.path.join(BASE_DIR, 'data'))
        files = list(filter(lambda x: today in x, files))
        newest_file = sorted(files, reverse=True)[0]
        filepath = os.path.join(BASE_DIR, 'data/{}'.format(newest_file))
        for att in self.add_attachment(newest_file, filepath):
            msg.attach(att)
        body = MIMEText(body, 'plain', 'utf-8')
        msg.attach(body)
        self.login()
        self.server.sendmail(emailfrom, emailto, msg.as_string())

    def close(self):
        self.server.quit()

    def main(self):
        self.send_email()
        self.close()

if __name__ == '__main__':
    MailSender().main()

