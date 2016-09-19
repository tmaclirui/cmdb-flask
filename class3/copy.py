#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
src = open('copyfile.txt','w')
src.writelines(['Hello,kk','\n'])
src.close()

src = open('copyfile.txt','r')
des = open('copyfile1.txt','w')
des.write(src.read())
src.close()
des.close()
