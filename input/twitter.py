#! /usr/bin/env python
# -*- coding:utf-8 -*-

import feedparser
import urllib
import sys
from datetime import datetime

class Twitter():
  '''
  TwitterのTimeLine中、任意の keyword が含まれているエントリを取り出す
  
  config.yamlの形式
      twitter:
          url: http://twitter.com/statuses/user_timeline/XXXXX.rss
          keyword: "メモ"
  >>> conf = {}
  >>> conf['url'] = "http://twitter.com/statuses/user_timeline/7080152.rss"
  >>> conf['keyword'] = u"こんにちは"
  
  >>> t = Twitter(conf)
  
  引数に辞書を渡す。内部の形式は History.py に記載されている。
  この辞書のなかに url があれば、それはすでに他のモジュールが
  得ている url であるため、ここではなにもしない。

  返り値も同じ形式の辞書となる。
  
  >>> input_dict = {}
  >>> result = t.get(input_dict)
  '''
  def __init__(self, conf):
    self.input_url = conf['url']
    if 'keyword' in conf:
      self.keyword = conf['keyword']
    else:
      self.keyword = None

  def get(self, input_dict):
    try:
      fdp = feedparser.parse(self.input_url)
    except:
      print "(Error) can not get the RSS..."
      sys.exit(1)
    d_str = datetime.now().isoformat()
    for entry in fdp['entries']:
      title = ""
      link = ""
      if "title" in entry:
        title = entry.title
      if self.keyword and self.keyword not in title:
        continue
      if "link" in entry:
        link = entry.link
      if link in input_dict: # already in the list from other input mod(s).
        continue
      input_dict[link] = {'title':title,
                          'input_from':'Twitter Memo',
                          'input_date':d_str,
                          'tag':''}
    return input_dict

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
  _test()
