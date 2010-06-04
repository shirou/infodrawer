#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os,sqlite3

HIST_FILENAME="input_hist.db"

class History():
  '''
  過去に登録した履歴URLを保存しておくDBを管理するクラス

  >>> hist = History()

  入力するデータ形式は、
  urlをキーとして、{title,input_date}を含む辞書。
  input_dateの形式は、ISO 8601 (YYYY-MM-DD)で、
  entryの日付ではなく、登録された日付

  >>> input_dict = {}
  >>> url = 'http://twitter.com/test/99999/'
  >>> input_dict[url] = {'title' : 'This is Title',
  ...                    'input_date': '2010-06-03T23:23:29.897471',
  ...                    'input_from':'TEST',
  ...                    'tag':''}

  データを渡すと、履歴があればその履歴を省いた辞書を返します。
  履歴がない場合は、自動的にDBに入ります。
  >>> result = hist.merge(input_dict)
  >>> print result
  {'http://twitter.com/test/99999/': {'input_from': 'TEST', 'tag': '', 'input_date': '2010-06-03T23:23:29.897471', 'title': 'This is Title'}}

  >>> hist.delete_test_data()
  
  '''
  
  def __init__(self):
    '''
    DBファイルがあればそれを開き、
    無ければ作成のフラグを立ててDBファイルを開く
    '''
    dbfilename = os.path.abspath(os.path.dirname(__file__)) + "/" + HIST_FILENAME

    if os.path.exists(dbfilename):
      self.conn = self.open_DB(dbfilename)
    else:
      self.conn = self.open_DB(dbfilename, True)
      
  def open_DB(self, dbfilename, create_flag = False):
    '''
    DBを開く
    create_flagがTrueであればDBを作成する

    >>> dbfilename = os.path.abspath(os.path.dirname(__file__)) + "/" + HIST_FILENAME
    >>> hist = History()
    >>> print os.path.exists(dbfilename)
    True
    '''
    conn = sqlite3.connect(dbfilename)
    if (create_flag):
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
    '''
    引数のurlがDB内にあればTrueを返し、無ければFalseを返す

    >>> hist = History()
    >>> url = 'http://twitter.com/test/99999/'
    >>> value = {'title' : """hoge's""", 'input_date': '2010-06-03T23:23:29.897471', 'input_from':'TEST', 'tag':''}
    >>> hist.is_exist(url)
    False
    >>> hist.insert_hist(url, value)
    >>> hist.is_exist(url)
    True
    >>> hist.delete_test_data()
    
    '''
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
    '''
    DBに履歴を入れる
    
    >>> hist = History()
    >>> url = 'http://twitter.com/test/99999/'
    >>> value = {'title' : """hoge's""", 'input_date': '2010-06-03T23:23:29.897471', 'input_from':'TEST', 'tag':''}
    >>> hist.is_exist(url)
    False
    >>> hist.insert_hist(url, value)
    >>> hist.is_exist(url)
    True
    >>> hist.delete_test_data()
    '''
    
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

  def delete_test_data(self):
    '''
    テスト用のデータを消去する
    
    >>> hist = History()
    >>> url = 'http://twitter.com/test/99999/'
    >>> value = {'title' : "hoge\'s", 'input_date': '2010-06-03T23:23:29.897471', 'input_from':'TEST', 'tag':''}
    >>> hist.insert_hist(url, value) # テストデータを入れる
    >>> hist.is_exist(url)
    True
    >>> hist.delete_test_data()
    >>> hist.is_exist(url)
    False
    '''
    
    cur = self.conn.cursor()
    try:
      q = "DELETE FROM history WHERE input_from='TEST'"
      cur.execute(q)
      
      self.conn.commit()
    finally:
      cur.close()

  def merge(self, input_dict):
    '''
    引数のinput_dictのうち、履歴DBにないurlをDBに入れる。
    返り値として、履歴DBにないurlのdictを返す。
    '''

    return_dict = {}
    for url,value in input_dict.iteritems():
      if (self.is_exist(url) == False):
	self.insert_hist(url, value)
	return_dict[url] = value

    return return_dict

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
  _test()
