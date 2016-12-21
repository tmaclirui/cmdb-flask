#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
import hashlib

def md5_str(string):
    md5 = hashlib.md5()
    md5.update(string)
    return md5.hexdigest()

def md5_file(path):
    fhandler = open(path,'rb')
    md5 = hashlib.md5()
    for line in fhandler:
        md5.update(line)
    fhandler.close()
    return md5.hexdigest()