#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Module        : decryptor.py
# Author        : bssthu
# Project       : pysqlsimplecipher
# Creation date : 2016-06-03
# Description   :
#


import hashlib
import hmac
from pysqlsimplecipher import config
from pysqlsimplecipher import util


def decrypt_file(filename_in, password, filename_out):
    if not isinstance(filename_in, str):
        raise RuntimeError('filename_in must be a str.')
    if not isinstance(password, bytearray):
        raise RuntimeError('password must be a bytearray.')
    if not isinstance(filename_out, str):
        raise RuntimeError('filename_out must be a str.')

    # read
    with open(filename_in, 'rb') as fp:
        raw = fp.read()

    # decrypt
    dec = decrypt_default(raw, password)

    # write
    with open(filename_out, 'wb') as fp:
        fp.write(dec)


def decrypt_default(raw, password):
    # configs
    salt_mask = config.salt_mask
    key_sz = config.key_sz
    hmac_key_sz = config.hmac_key_sz
    page_sz = config.page_sz
    iv_sz = config.iv_sz
    reserve_sz = config.reserve_sz
    hmac_sz = config.hmac_sz

    return decrypt(raw, password, salt_mask, key_sz, hmac_key_sz, page_sz, iv_sz, reserve_sz, hmac_sz)


def decrypt(raw, password, salt_mask, key_sz, hmac_key_sz, page_sz, iv_sz, reserve_sz, hmac_sz):
    dec = b'SQLite format 3\0'

    # derive key
    salt_sz = 16
    salt = raw[:salt_sz]
    key, hmac_key = key_derive(salt, password, salt_mask, key_sz, hmac_key_sz)

    # decrypt pages
    for i in range(0, (int)(len(raw) / 1024)):
        page = raw[page_sz*i:page_sz*(i+1)]
        if i == 0:
            # skip salt
            page = page[salt_sz:]
        page_content = page[:-reserve_sz]
        reserve = page[-reserve_sz:]
        iv = reserve[:iv_sz]
        # check hmac
        hmac_old = reserve[iv_sz:iv_sz+hmac_sz]
        hmac_obj = hmac.new(hmac_key, page_content + iv, hashlib.sha1)
        hmac_obj.update((i+1).to_bytes(4, 'little'))
        hmac_new = hmac_obj.digest()
        if not hmac_old == hmac_new:
            raise RuntimeError('hmac check failed in page %d.' % (i+1))
        # decrypt content
        page_dec = util.decrypt(page_content, key, iv)
        dec += page_dec + reserve       # TODO: use random

    return dec


def key_derive(salt, password, salt_mask, key_sz, hmac_key_sz):
    """Derive an encryption key for page decryption, an key for hmac generation"""
    key_iter = 64000
    key = hashlib.pbkdf2_hmac('sha1', password, salt, key_iter, key_sz)

    hmac_key_iter = 2
    hmac_salt = bytearray([x ^ salt_mask for x in salt])
    hmac_key = hashlib.pbkdf2_hmac('sha1', key, hmac_salt, hmac_key_iter, hmac_key_sz)

    return key, hmac_key
