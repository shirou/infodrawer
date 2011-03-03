#! /usr/bin/env python
# -*- coding:utf-8 -*-

import urllib

class InstaPaper():
  def __init__(self, conf):
    self.username = conf['username']
    self.password = conf['password']

  def output(self, input_dict):
    INSTAPAPER_API_URL = 'https://www.instapaper.com/api/add'
    pd = {'username':self.username, 'password':self.password}
    result_list = []
    for url,entry in input_dict.iteritems():
      result = {}
      pd['url'] = url
      pd['title'] = entry['title'].encode('UTF-8')
      params = urllib.urlencode(pd)
      response = urllib.urlopen(INSTAPAPER_API_URL, params)
      if (response.code != 200):
        next
      result['code'] = response.code
      result['link'] = pd['url'] 
      result['title'] = pd['title']
      result_list.append(result)
    return result_list
