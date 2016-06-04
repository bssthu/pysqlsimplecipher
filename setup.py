#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Module        : setup.py
# Author        : bssthu
# Project       : pysqlsimplecipher
# Creation date : 2016-06-05
# Description   :
#


from setuptools import setup


setup(name='pysqlsimplecipher',
      version='0.2',
      url='https://github.com/bssthu/pysqlsimplecipher',
      license='GNU Lesser General Public License Version 3',
      author='bssthu',
      description='A tool for sqlite database encryption or decryption like sqlcipher without install sqlcipher',
      install_requires=['pycrypto'],
      packages=['pysqlsimplecipher']
      )
