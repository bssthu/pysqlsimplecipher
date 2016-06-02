#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Module        : util.py
# Author        : bssthu
# Project       : pysqlsimplecipher
# Creation date : 2016-06-03
# Description   :
#


from Crypto.Cipher import AES


def decrypt(raw, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(raw)
