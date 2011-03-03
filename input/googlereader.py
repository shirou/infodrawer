#! /usr/bin/env python
# -*- coding:utf-8 -*-

import feedparser
from datetime import datetime
import sys

class GoogleReader():
  '''
  GoogleReaderでStarをつけたエントリを取得する。

  config.yamlでは、'url'だけを使用する

  >>> conf = {}
  >>> conf['url'] = "http://feeds.feedburner.com/blogspot/dtKx"
  ... # doct testでは違うURLを使用しているが、本来は以下の形式
  ... # http://www.google.com/reader/public/atom/user/XXXXX/state/com.google/starred

  >>> g = GoogleReader(conf)

  引数に辞書を渡す。内部の形式は History.py に記載
  この辞書のなかに url があれば、それはすでに他のモジュールが
  得ている url であるため、ここではなにもしない。

  返り値も同じ形式の辞書となる
  
  >>> input_dict = {}
  >>> result = g.get(input_dict)
  >>> print len(result)
  25
  '''
  
  def __init__(self, conf):
    self.input_url = conf['url']
    
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
      if "link" in entry:
        link = entry.link
      if link in input_dict: # already in the list from other input mod(s).
        continue
      input_dict[link] = {'title':title,
                          'input_from':'Google Reader',
                          'input_date':d_str,
                          'tag':''}
    return input_dict

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
  _test()
