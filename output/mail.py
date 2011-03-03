#! /usr/bin/env python
# -*- coding:utf-8 -*-

import smtplib
import sys
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart 
from email.Header import Header
from email.Utils import formatdate

class Mail():
  def __init__(self, conf):
    self.input_conf(conf)
    
  def input_conf(self, conf):
    self.from_addr = conf['from_addr']
    self.to_addr = conf['mail_addr']
    if 'subject' in conf:
      self.subject = conf['subject']
    else:
      self.subject = None
    self.insta = False
    if 'insta' in conf:
      if conf['insta'] == 'yes':
        self.insta = True
      else:
        self.insta = False
    if 'smtp' in conf:
      self.smtp = conf['smtp']
    else:
      self.smtp = None
    if 'use_gmail' in conf:
      if conf['use_gmail'] == 'yes':
        self.use_gmail = True
      else:
        self.use_gmail = False
    else:
      self.use_gmail = False
    if 'gmail_addr' in conf:
      self.gmail_addr = conf['gmail_addr']
    else:
      self.use_gmail = False
    if 'gmail_pass' in conf:
      self.gmail_pass= conf['gmail_pass']
    else:
      self.use_gmail = False

  def create_HTML_message(self, from_addr, to_addr, subject, html_body, encoding):
    msg = MIMEText(html_body.encode('utf-8'), 'html', 'utf-8')
    subject = subject.ljust(30) # title becomes max 30 length
    if self.subject:
      subject = self.subject + " " + subject
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()
    return msg

  def send_mail(self, from_addr, to_addr, msg):
    self.mail_status.sendmail(from_addr, [to_addr], msg.as_string())

  def login(self):
    if self.use_gmail:
      self.mail_status = smtplib.SMTP('smtp.gmail.com', 587)
      self.mail_status.ehlo()
      self.mail_status.starttls()
      self.mail_status.ehlo()
      self.mail_status.login(self.gmail_addr, self.gmail_pass)
    else:
      # SMTPの引数を省略した場合はlocalhost:25
      if self.smtp == None:
        s = smtplib.SMTP()
      else:
        s = smtplib.SMTP(self.smtp)

  def logout(self):
    self.mail_status.close()

  def output(self, input_dict):      
    try:
      self.login()
    except:
      print "Mail Login error:", sys.exc_info()[0]
      raise
    
    for url, value in  input_dict.iteritems():
      contents = None
      encoding = ""
      if value and value.has_key('input_from'):
        if 'Twitter' in value['input_from']:
          encoding = 'utf-8'
          contents = value['title']
      else:
        try:
          encoding = value['encoding']
          contents = value['contents']
        except TypeError:
          print value
          print sys.exc_info()[0]
          raise
      if contents == None:
        continue # XXX 
      msg = self.create_HTML_message(self.from_addr,
                                     self.to_addr,
                                     value['title'],
                                     contents,
                                     encoding)
      try:
        self.send_mail(self.from_addr, self.to_addr, msg)
      except:
        print "Sending Mail Error:", sys.exc_info()[0]
        raise

    self.logout()

def test():
  sys.path.extend(['..', '.'])
  import history
  test_conf = {'mail_addr':''
               'from_addr':''
               'smtp':'localhost',
               'insta':'no',
               'subject':'test',
               'use_gmail':'yes',
               'gmail_addr':''
               'gmail_pass':''}
  output_m = Mail(test_conf)
  hist = history.History()
  hist.get_hist = test_get_hist
  output_m.output(hist.get_hist())

def test_get_hist():
  test_url = 'http://www.yahoo.com'
  output_dict = {}
  output_dict[test_url] = {'title':'my name is yasuharu sawada',
                           'input_from':'TEST',
                           'has_url':True,
                           'contents':'yasu',
                           'encoding':'utf-8',
                           'tag':''}
  return output_dict

if __name__ == '__main__':
  test()
  
