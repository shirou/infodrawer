#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages
import os

VERSION = '0.1.0'
README = os.path.join(os.path.dirname(__file__), 'README')
long_description = open(README).read() + '\n\n'

setup(name='infodrawer',
      version=VERSION,
      description=("An application that inport information, output to services"),
      long_description=long_description,
      classifiers=[
        "Programming Language :: Python",
	"Topic :: Communications :: Email",
	"Topic :: Internet :: WWW/HTTP",
	"Development Status :: 2 - Pre-Alpha",
	"License :: OSI Approved :: BSD License"
      ],
      keywords="infodrawer rss mail evernote twitter hatena",
      author='shirou',
      author_email='shirou.faw@gmail.com',
      license='BSD',
      packages=find_packages(),
      install_requires=['feedparser', 'PyYAML'],
      )
