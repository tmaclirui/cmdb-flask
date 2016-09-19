#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
import sys,time
file1 = open('ok.txt','r')
line = file1.read().split('\n')[-10:]
line.pop(-1)
print line
while True:
    # line = file1.read().split('\n')[-10:]
    time.sleep(1)
    #if line:
    for i in line:
        sys.stdout.write(i)
       #sys.stdout.write(i + '\n')
    #print ''
