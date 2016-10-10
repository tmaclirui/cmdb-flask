#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
src_path = "/home/wwwroot/test.txt"
dst_path = "/home/wwwroot/test2.txt"
src_file = open(src_path,"r")
dst_file = open(dst_path,"w")
size = 1024
while True:
    file = src_file.read(size)
    if file =="":
        break
    dst_file.write(file)

src_file.close()
dst_file.close()
