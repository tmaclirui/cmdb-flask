#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
mylist = [1,2,3,4,5,6,7,8,9]
temp = 0
for i in range(len(mylist)/2):
    temp = mylist[i]
    mylist[i] = mylist[-i-1]
    mylist[-i-1] = temp
print mylist
