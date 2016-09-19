#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
with open('ok.txt') as f:
    f.seek(0,2)
    while True:
        last_pos = f.tell()
        line = f.readline()
        if line:
            print line
