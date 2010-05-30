#! /usr/bin/env python
# coding: utf-8

import urllib2

import smtplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart 
from email.Header import Header
from email.Utils import formatdate

class Evernote():

  def __init__(self, conf):
    self.conf = conf
    self.from_addr = conf['from_addr']
    self.to_addr   = conf['mail_addr']
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

    if ('note' in conf):
      self.note      = conf['note']
    else:
      self.note      = None
    if ('tag' in conf):
      self.tag       = conf['tag']
    else:
      self.tag       = None

  def send(self, input_dict):
    import mail
    mail_o = mail.Mail(self.conf)
    for url, value in  input_dict.iteritems():
      (encoding, contents) = mail_o.create_contents(url)
      if (contents == None):
	continue # XXX

      subject = value['title']
      if (self.note):
	subject = subject + " @" + self.note
      if (self.tag):
	subject = subject + " #"+ self.tag
      msg = mail_o.create_HTML_message(self.from_addr,
				self.to_addr,
				subject,
				contents,
				encoding)
      if (self.use_gmail):
	mail_o.send_via_gmail(self.from_addr, self.to_addr,
			      msg, self.gmail_addr, self.gmail_pass)
      else:
	mail_o.send_mail(self.from_addr, self.to_addr,
			 msg, self.smtp)


if __name__ == '__main__':
  import sys,os
  import yaml
  
  sys.path.append("..")
  import History

  CONF_FILENAME="conf.yaml"

  hist = History.History()
  
  f = os.path.abspath(os.path.dirname(__file__)) + "/../" + CONF_FILENAME
  conf = yaml.load(open(f).read().decode('utf8'))

  output_m = Evernote(conf['output']['evernote'])
  output_m.send(hist.get_hist())
  
