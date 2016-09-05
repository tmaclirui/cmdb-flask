#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
mylist = [1,2,35,'lirui',5,6,8,00,12]
mylength = 0
myin = False
value = raw_input('please input a value:')
for i in mylist:
    mylength=mylength + 1
    if i == value:
        myin = True
        print ' %s in list:%s' % (value,myin)
print mylength
print len(mylist)
