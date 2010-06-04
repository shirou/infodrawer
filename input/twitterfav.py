#! /usr/bin/env python
# -*- coding:utf-8 -*-

import feedparser
import urllib
from datetime import datetime

class TwitterFav():
  '''
  TwitterのFavoritesを取り出す
  
  config.yamlの形式
      twitterfav:
          url: http://twitter.com/favorites/XXXXX.rss

  >>> conf = {}
  >>> conf['url'] = "http://twitter.com/favorites/7080152.rss"

  >>> t = TwitterFav(conf)

  引数に辞書を渡す。内部の形式は History.py に記載されている。
  この辞書のなかに url があれば、それはすでに他のモジュールが
  得ている url であるため、ここではなにもしない。

  返り値も同じ形式の辞書となる。
  
  >>> input_dict = {}
  >>> result = t.get(input_dict)
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
    
      if ( "title" in entry ):
	title = entry.title
      if ( "link" in entry ):
	link = entry.link

      if (link in input_dict): # already in the list from other input mod(s).
	continue
      
      input_dict[link] = {'title':title,
			  'input_from':'Twitter Favorite',
			  'input_date': d_str,
			  'tag' : ''}
      
    return input_dict


def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
  _test()
