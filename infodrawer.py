#! /usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import yaml
import urllib
import urllib2
from input import googlereader, twitter, twitterfav, hatenabookmark
from output import instapaper, mail, evernote
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
                    return ''

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
            input_m = googlereader.GoogleReader(conf['input'][i])
        elif i == "twitter":
            input_m = twitter.Twitter(conf['input'][i])
        elif i == "twitterfav":
            input_m = twitterfav.TwitterFav(conf['input'][i])
        elif i == "hatenabookmark":
            input_m = hatenabookmark.HatenaBookmark(conf['input'][i])
        if input_m:
            input_dict = input_m.get(input_dict)
    return input_dict

def outputter(conf, output_dict):
    if len(output_dict) > 0:
        for out_module in conf['output']:
            output_m = None
            if out_module == "instapaper":
                output_m = instapaper.InstaPaper(conf['output'][out_module])
            elif out_module == "mail":
                output_m = mail.Mail(conf['output'][out_module])
            elif out_module == "evernote":
                output_m = evernote.Evernote(conf['output'][out_module])
            if output_m:
                try:
                    output_m.output(output_dict)
                except:
                    print "An exception occurs. but continue:", \
                          sys.exc_info()[0]
                    continue
                  
def main():
    # 設定ファイルのロード
    conf_path = os.path.abspath(os.path.dirname(__file__)) + "/" + CONF_FILENAME
    conf = yaml.load(open(conf_path).read().decode('utf-8'))
    # input データの取得
    input_dict = {}
    input_dict = inputter(conf, input_dict)
    # 重複を除く
    hist = history.History()
    input_dict = hist.merge(input_dict)
    output_dict = {}
    for url, value in input_dict.iteritems():
        ret = create_contents(url, value)
        if len(ret) > 0:
            output_dict[url] = ret
    # データを出力
    outputter(conf, output_dict)

if __name__ == '__main__':
    main()
