#! /usr/bin/env python
# -*- coding:utf-8 -*-

import smtplib
import re
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.Header import Header
from email.Utils import formatdate

class Evernote():
    def __init__(self, conf):
        self.input_conf(conf)
        
    def input_conf(self, conf):
        self.conf = conf
        self.from_addr = conf['from_addr']
        self.to_addr = conf['mail_addr']
        if 'smtp' in conf:
            self.smtp = conf['smtp']
        else:
            self.smtp = None
            self.insta = False
        if 'insta' in conf:
            self.insta = conf['insta']
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
            self.gmail_pass = conf['gmail_pass']
        else:
            self.use_gmail = False
        if 'note' in conf:
            self.note = conf['note']
        else:
            self.note = None
        if 'tag' in conf:
            self.tag = conf['tag']
        else:
            self.tag = None
        if 'twitter_account' in conf:
            self.twitteraccount = conf['twitter_account']
        else:
            self.twitteraccount = None
        if 'tweetmemo' in conf:
            self.tweetmemo = conf['tweetmemo']
        else:
            self.tweetmemo = None

    def output(self, input_dict):
        import mail
        mail_o = mail.Mail(self.conf)
        mail_o.login()
        evernote_tag = self.tag
        evernote_note = self.note
        for url, value in  input_dict.iteritems():
            contents = None
            encoding = ""
            if 'Twitter' in value['input_from']:
                encoding = 'utf-8'
                contents = value['title']
                evernote_note = 'twitter'
                if self.tag:
                    evernote_tag = self.tag
                else:
                    evernote_tag = ''
                if value.has_key("has_url"):
                    if value["has_url"]:
                        contents = value['contents']
                if self.twitteraccount:
                    owntweet = re.match(self.twitteraccount, contents)
                    if owntweet:
                        contents = contents[owntweet.end() + 2:]
                        evernote_note = self.tweetmemo
            else:
                encoding = value['encoding']
                contents = value['contents']
            if contents == None:
                continue # XXX
        subject = value['title']
        if evernote_note:
            subject = subject + " @" + evernote_note
        if evernote_tag:
            subject = subject + " #"+ evernote_tag
        msg = mail_o.create_HTML_message(self.from_addr,
                                         self.to_addr,
                                         subject,
                                         contents,
                                         encoding)
        mail_o.send_mail(self.from_addr, self.to_addr, msg)
        mail_o.logout()

def test():
    import sys,os
    import yaml
    sys.path.extend(["..", '.'])
    import history
    CONF_FILENAME="conf.yaml"
    hist = history.History()
    f = os.path.abspath(os.path.dirname(__file__)) + "/../" + CONF_FILENAME
    conf = yaml.load(open(f).read().decode('utf8'))
    output_m = Evernote(conf['output']['evernote'])
    hist.get_hist = test_get_hist
    output_m.output(hist.get_hist())

def test_get_hist():
    test_url = 'http://www.google.com'
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
