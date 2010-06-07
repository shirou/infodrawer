#! /usr/bin/env python
# -*- coding:utf-8 -*-

import re

import smtplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart 
from email.Header import Header
from email.Utils import formatdate

class Mail():

  def __init__(self, conf):
    self.from_addr = conf['from_addr']
    self.to_addr   = conf['mail_addr']
    if ('subject' in conf):
      self.subject    = conf['subject']
    else:
      self.subject    = None
    self.insta = False
    if ('insta' in conf):
      self.insta = conf['insta']
    if ('smtp' in conf):
      self.smtp    = conf['smtp']
    else:
      self.smtp    = None
    if ('use_gmail' in conf):
      if (conf['use_gmail'] == True):
	self.use_gmail = True
      else:
	self.use_gmail = False
    else:
      self.use_gmail = False
    if ('gmail_addr' in conf):
      self.gmail_addr = conf['gmail_addr']
    else:
      self.use_gmail = False
    if ('gmail_pass' in conf):
      self.gmail_pass= conf['gmail_pass']
    else:
      self.use_gmail = False

  def create_HTML_message(self, from_addr, to_addr, subject, html_body, encoding):
    msg = MIMEText(html_body.encode('utf-8'), 'html', 'utf-8')

    subject = subject.ljust(30) # title becomes max 30 length
    if (self.subject):
      subject = self.subject + " " + subject
    
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()

    return msg

  def send_mail(self, from_addr, to_addr, msg, smtp = None):
    # SMTPの引数を省略した場合はlocalhost:25
    if smtp == None:
      s = smtplib.SMTP()
    else:
      s = smtplib.SMTP(smtp)
    s.sendmail(from_addr, [to_addr], msg.as_string())
    s.close()

  def send_via_gmail(self, from_addr, to_addr, msg, gaddr, password):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(gaddr, password)
    s.sendmail(from_addr, [to_addr], msg.as_string())
    s.close()

  def output(self, input_dict):
    for url, value in  input_dict.iteritems():
      contents = None
      encoding = ""
      if ('Twitter' in value['input_from']):
	encoding = 'utf-8'
	contents = value['title']
      else:
	encoding = value['encoding']
	contents = value['contents']
      if (contents == None):
	continue # XXX 
      msg = self.create_HTML_message(self.from_addr,
				self.to_addr,
				value['title'],
				contents,
				encoding)
      if (self.use_gmail):
	self.send_via_gmail(self.from_addr, self.to_addr,
		       msg, self.gmail_addr, self.gmail_pass)
      else:
	self.send_mail(self.from_addr, self.to_addr,
			    msg, self.smtp)


if __name__ == '__main__':
  import sys,os
  import yaml
  
  sys.path.append("..")
  import History

  CONF_FILENAME="conf.yaml"

  hist = History.History()

  f = os.path.abspath(os.path.dirname(__file__)) + "/../" + CONF_FILENAME
  conf = yaml.load(open(f))

  
