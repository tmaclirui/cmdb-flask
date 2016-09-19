#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
try:
    f = open('ok.txt')
except IOError:
    print 'the file not exits'
else:
    print 'success to close'
    f.close()
