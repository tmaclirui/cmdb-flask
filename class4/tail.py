#!/usr/bin/python
# coding: utf-8
file = open("/home/wwwroot/test.txt","r")
file.seek(0,2)
line = " "

while True:
    line += file.readline()
    if line.endswith("\n"):
        print line
        line = " "

