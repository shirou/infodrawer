#! /usr/bin/env python
# -*- coding:utf-8 -*-

import feedparser
import urllib
from datetime import datetime

class TwitterFav():

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
			  'input_from':'Twitter Favorites',
			  'input_date': d_str}
      
    return input_dict


if __name__ == '__main__':
  CONF_FILENAME="conf.yaml"
  import sys,os,yaml

  f = os.path.abspath(os.path.dirname(__file__)) + "/../" + CONF_FILENAME
  conf = yaml.load(open(f))
  c = conf

  # Fav一覧を取得
  import_m = TwitterFav(conf['input']['twitterfav'])
  print import_m.get({})

