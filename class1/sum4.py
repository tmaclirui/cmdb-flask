#!/usr/bin/python
# coding: utf-8
total = 0
count = 0
while True:
    num = raw_input('please input your name:')
    if num == 'exit':
        break
    else:
        num = int(num)
        total += num
        count += 1
        if count !=0:
            average = total / count
print 'total:%d,average:%d' % (total,average)
