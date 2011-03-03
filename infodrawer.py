#! /usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import yaml
import urllib
import urllib2
import history

CONF_FILENAME = "conf.yaml"

def encoding_detect(orig_str):
  try:
    return ('iso-2022-jp', orig_str.decode('iso-2022-jp'))
  except UnicodeDecodeError:
    try:
      return ('euc-jp', orig_str.decode('euc-jp'))
    except UnicodeDecodeError:
      try:
        return ('cp932', orig_str.decode('cp932'))
      except UnicodeDecodeError:
        try:
          return ('utf-8', orig_str.decode('utf-8'))
        except UnicodeDecodeError:
          return (None, None)

def create_contents(url, value, insta=True):
  if insta:
    url = "http://www.instapaper.com/text?u=" + urllib.quote_plus(url)
  req = urllib2.Request(url)
  response = None
  try:
    response = urllib2.urlopen(req)
  except urllib2.URLError, error:
    return ''
  msg = response.read()
  (value['encoding'], value['contents']) = encoding_detect(msg)
  return value

def inputter(conf, input_dict):
  for i in conf['input']:
    input_m = None
    if i == 'googlereader':
      from input import googlereader
      input_m = googlereader.GoogleReader(conf['input'][i])
    elif i == "twitter":
      from input import twitter
      input_m = twitter.Twitter(conf['input'][i])
    elif i == "twitterfav":
      from input import twitterfav
      input_m = twitterfav.TwitterFav(conf['input'][i])
    if input_m:
      input_dict = input_m.get(input_dict)
  return input_dict

def outputter(conf, input_dict):
  if len(input_dict) > 0:
    for o in conf['output']:
      output_m = None
      if o == "instapaper":
        from output import instapaper
        output_m = instapaper.InstaPaper(conf['output'][o])
      elif o == "mail":
        from output import mail
        output_m = mail.Mail(conf['output'][o])
      elif o == "evernote":
        from output import evernote
        output_m = evernote.Evernote(conf['output'][o])
      if output_m:
          try:
              output_m.output(input_dict)
          except:
              print "An exception occurs. but continue:" , sys.exc_info()[0]
              continue  

def main():
  # 設定ファイルのロード
  conf_path = os.path.abspath(os.path.dirname(__file__)) + "/" + CONF_FILENAME
  conf = yaml.load(open(conf_path).read().decode('utf8'))
  # input データの取得
  input_dict = {}
  input_dict = inputter(conf, input_dict)
  # 重複を除く
  hist = history.History()
  input_dict = hist.merge(input_dict)

  for url, value in input_dict.iteritems():
    print url, ":", value
    ret = create_contents(url, value)
    if len(ret) > 0:
      input_dict[url] = ret
  # データを出力
  outputter(conf, input_dict)

if __name__ == '__main__':
  main()
