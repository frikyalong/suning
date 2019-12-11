# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import csv
import time

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class GaojiesiPipeline(object):

    def open_spider(self, spider):
        self.store_file = os.path.dirname(__file__) + '/../result/result_%s.csv' % time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        self.file = open(self.store_file, 'a+', encoding="utf-8", newline='')
        # csv写法
        self.writer = csv.writer(self.file, dialect="excel")
        # write header
        self.writer.writerow(['cmmdtyCode', 'price', 'shoppingCart', 'area_name'])

    def process_item(self, item, spider):
        if item['cmmdtyCode']:
            self.writer.writerow([item['cmmdtyCode'], item['price'], item['shoppingCart'], item['area_name']])
        return item

    def close_spider(self, spider):
        self.file.close()
        subject = "高洁丝货品统计"
        sender = "109332409@qq.com"
        content = "请查看附件"
        receiver = list()
        receiver.append('wangyangiam@hotmail.com')
        receiver.append('109332409@qq.com')
        password = "bbwqyblqiqnabhed"
        message = MIMEMultipart()
        message['Subject'] = subject
        message['To'] = ';'.join(receiver)
        message['From'] = sender
        att = MIMEText(open(self.store_file, 'rb').read(), 'base64', 'utf-8')
        att["Content-Disposition"] = 'attachment; filename="gaojiesi.csv"'
        message.attach(att)
        message.attach(MIMEText(content, 'plain', 'utf-8'))
        smtp = smtplib.SMTP_SSL("smtp.qq.com", 465)
        smtp.login(sender, password)  # 发件人登录
        smtp.sendmail(sender, ';'.join(receiver), message.as_string())  # as_string 对 message 的消息进行了封装
        smtp.close()

