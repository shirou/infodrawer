#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os,yaml

HIST_FILENAME="input_hist.yaml"

class History():
  def __init__(self):
    '''
    hist_map は、urlをキーとして、{title,date}を含む辞書を持つ。
    dateの形式は、ISO 8601 (YYYY-MM-DD)で、
    entryの日付ではなく、登録された日付

    hist_dict = {'http://...': {'title':'...', 'date': '...'},
                'http://...': {'title':'...', 'date': '...'}, ... }
    
    '''
    f = os.path.abspath(os.path.dirname(__file__)) + "/" + HIST_FILENAME

    self.hist_dict = {}
    
    if os.path.exists(f):
      self.hist_dict =  yaml.load(open(f))

  def get_hist(self):
    return self.hist_dict

  def append_file(self, write_dict):
    f = os.path.abspath(os.path.dirname(__file__)) + "/" + HIST_FILENAME
    fp = open(f,"a")
    output = yaml.dump(write_dict)
    fp.write(output)
    fp.close()

  def merge(self, input_dict):
    return_dict = {}
    for url,value in input_dict.iteritems():
      if (url not in self.hist_dict):
	self.hist_dict[url] = value
	return_dict[url] = value

    return return_dict

if __name__ == '__main__':
  import sys,os
  import yaml
  
  import History

  hist = History.History()

  input_dict = {}
  input_dict['http://twitter.com/SamFURUKAWA/statuses/13878785385'] = 'hoge'

  input_dict = hist.merge(input_dict)

  print input_dict
