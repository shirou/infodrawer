#! /usr/bin/env python
# coding: utf-8

import sys, os
import yaml

import History

CONF_FILENAME="conf.yaml"

if __name__ == '__main__':
  f = os.path.abspath(os.path.dirname(__file__)) + "/" + CONF_FILENAME
  conf = yaml.load(open(f).read().decode('utf8'))

  input_dict = {}
  
  for i in conf['input']:
    input_m = None
    if (i == "googlereader"):
      from input import googlereader
      input_m = googlereader.GoogleReader(conf['input'][i])
    elif (i == "twitter"):
      from input import twitter
      input_m = twitter.Twitter(conf['input'][i])
    elif (i == "twitterfav"):
      from input import twitterfav
      input_m = twitterfav.TwitterFav(conf['input'][i])
    if input_m:
      input_dict = input_m.get(input_dict)

  hist = History.History()
  input_dict = hist.merge(input_dict)

  if len(input_dict) > 0:
    for o in conf['output']:
      output_m = None
      if (o == "instapaper"):
	from output import instapaper
	output_m = instapaper.InstaPaper(conf['output'][o])
      elif (o == "mail"):
	from output import mail
	output_m = mail.Mail(conf['output'][o])
      elif (o == "evernote"):
	from output import evernote
	output_m = evernote.Evernote(conf['output'][o])

      if output_m:
	print output_m.outpu(input_dict)

  hist.append_file() # write to hist_file
