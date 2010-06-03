#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os,sqlite3

HIST_FILENAME="input_hist.db"

class History():
  def __init__(self):
    dbfilename = os.path.abspath(os.path.dirname(__file__)) + "/" + HIST_FILENAME

    if os.path.exists(dbfilename):
      self.conn = self.openDB(dbfilename)
    else:
      self.conn = self.openDB(dbfilename, True)
      
  def openDB(self, dbfilename, createFlag = False):
    conn = sqlite3.connect(dbfilename)
    if (createFlag):
      conn.executescript("""CREATE TABLE history(
                               _id INTEGER PRIMARY KEY,
                               url TEXT NOT NULL,
                               title TEXT,
                               input_date TEXT NOT NULL,
                               input_from TEXT,
                               tag TEXT
                               );""")
      conn.commit()
    return conn

  def is_exist(self, url):
    cur = self.conn.cursor()
    try:
      cur.execute("SELECT * From history WHERE url=?", [url])
      r = cur.fetchone()
      if (r):
	return True
      else:
	return False
    finally:
	cur.close()

  def insert_hist(self, url, value):
    cur = self.conn.cursor()
    try:
      q = "INSERT INTO history (url, title, input_date, input_from, tag) values(?,?,?,?,?)"
      cur.execute(q, (url,
		      value['title'],
		      value['input_date'],
		      value['input_from'],
		      value['tag']))
      
      self.conn.commit()
    finally:
      cur.close()

  def merge(self, input_dict):
    '''
    input_dict は、urlをキーとして、{title,input_date}を含む辞書を持つ。
    input_dateの形式は、ISO 8601 (YYYY-MM-DD)で、
    entryの日付ではなく、登録された日付

    input_dict = {'http://...': {'title':'...', 'input_date': '...'},
                  'http://...': {'title':'...', 'input_date': '...'}, ... }
    
    '''

    return_dict = {}
    for url,value in input_dict.iteritems():
      if (self.is_exist(url) == False):
	self.insert_hist(url, value)
	return_dict[url] = value

    return return_dict

if __name__ == '__main__':
  import sys,os
  import yaml
  
  import History

  hist = History.History()

  url = 'http://twitter.com/SamFURUKAWA/statuses/13878785385'
  print hist.is_exist(url);

  input_dict = {}
  input_dict[url] = {'title' : """hoge's""", 'input_date': '2010-06-03T23:23:29.897471', 'input_from':'TEST', 'tag':''}

  input_dict = hist.merge(input_dict)

  print input_dict
