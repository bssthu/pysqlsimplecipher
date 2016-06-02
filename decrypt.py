#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Module        : decrypt.py
# Author        : bssthu
# Project       : pysqlsimplecipher
# Creation date : 2016-06-03
# Description   :
#


import sys
from pysqlsimplecipher import decryptor


def usage():
    print('Usage: python decrypt.py encrypted.db password output.db')


def main():
    # arguments
    argv = sys.argv
    if len(argv) != 4:
        usage()
        return
    filename_in = argv[1]
    password = bytearray(argv[2].encode('utf8'))
    filename_out = argv[3]

    decryptor.decrypt_file(filename_in, password, filename_out)


if __name__ == '__main__':
    main()
