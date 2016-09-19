#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
path = 'ok.text'
read_file= open(path,'r')
file_ = read_file.read()
read_file.close()

read_file= open(path,'r')
cx = ''
cx1=''
while True:
    _butter = read_file.read(8)
    if _butter == '':
        break
    cx += _butter
read_file.close()

read_file= open(path,'r')
while True:
    _butter = read_file.readline()
    if _butter == '':
        break
    cx1 += _butter
read_file.close()
print file_,cx,cx1
print file_ == cx 
print cx == cx1
