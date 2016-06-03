#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Module        : util.py
# Author        : bssthu
# Project       : pysqlsimplecipher
# Creation date : 2016-06-03
# Description   :
#


import os
import math
import hashlib
import hmac
from Crypto.Cipher import AES


def encrypt(raw, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(raw)


def decrypt(raw, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(raw)


def is_valid_database_header(header):
    return header[:16] == b'SQLite format 3\0' and is_valid_decrypted_header(header[16:])


def is_valid_decrypted_header(header):
    # skip first 16 bytes
    return header[21-16] == 64 and header[22-16] == 32 and header[23-16] == 32


def get_page_size_from_database_header(header):
    page_sz = int.from_bytes(header[16:18], 'big')
    if page_sz == 1:        # since SQLite version 3.7.1
        page_sz = 65536
    return page_sz


def get_reserved_size_from_database_header(header):
    return int(header[20])


def is_valid_page_size(page_sz):
    # page_sz must be power of 2, and greater than 512
    return page_sz >= 512 and page_sz == 2 ** int(math.log(page_sz, 2))


def get_page(raw, page_sz, page_no):
    return raw[page_sz*(page_no-1):page_sz*page_no]


def random_bytes(n):
    return os.urandom(n)


def key_derive(salt, password, salt_mask, key_sz, hmac_key_sz):
    """Derive an encryption key for page encryption/decryption, an key for hmac generation"""
    key_iter = 64000
    key = hashlib.pbkdf2_hmac('sha1', password, salt, key_iter, key_sz)

    hmac_key_iter = 2
    hmac_salt = bytearray([x ^ salt_mask for x in salt])
    hmac_key = hashlib.pbkdf2_hmac('sha1', key, hmac_salt, hmac_key_iter, hmac_key_sz)

    return key, hmac_key


def generate_hmac(hmac_key, content, page_no):
    hmac_obj = hmac.new(hmac_key, content, hashlib.sha1)
    hmac_obj.update(page_no.to_bytes(4, 'little'))
    return hmac_obj.digest()
