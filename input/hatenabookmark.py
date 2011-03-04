#! /usr/bin/env python
# -*- coding:utf-8 -*-

import feedparser
from datetime import datetime
import sys

class HatenaBookmark():
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
      tags = []
      if "title" in entry:
        title = entry.title
      if "tags" in entry:
          for tag in entry['tags']:
              tags.append(tag.get('term', ''))
          if len(tags) > 0:
              input_tag = ' #'.join(tags)
          else:
              input_tag = ''
      if "link" in entry:
        link = entry.link
      if link in input_dict: # already in the list from other input mod(s).
        continue
      input_dict[link] = {'title':title,
                          'input_from':'HatenaBookmark',
                          'input_date':d_str,
                          'tag':input_tag}
    return input_dict

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
  _test()

