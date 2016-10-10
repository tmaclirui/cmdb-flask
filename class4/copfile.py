#!/usr/bin/python
# coding: utf-8
src_path = "/home/wwwroot/test.txt"
dst_path = "/home/wwwroot/test1.txt"
fhandler = open(src_path,"r")
cxt = fhandler.read()
fhandler.close()

fhandler = open(dst_path,"w")
fhandler.write(cxt)
fhandler.close()
