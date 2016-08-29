#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
import random
print "----------猜数字游戏开始啦-----------"
while True:
    number = raw_input('please input a number:')
    number = int(number)
    rnum = random.randint(0,100)
    if number == rnum:
        print "---恭喜你！猜对了---"
        break
    else:
        print "---哦哦,你猜错了哦,继续加油哦---"
        
