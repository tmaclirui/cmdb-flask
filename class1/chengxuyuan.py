#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
xigua = raw_input('can you show xigua?(Y/N)')
if xigua == 'Y':
    print '我看到西瓜啦'
    baozi = raw_input('can you show 1 baozi?(Y/N)')
    if baozi == 'Y':
        print '我买了一个包子'
    else:
        print '我买0个包子'
else:
    print '我没看到西瓜呀'
    baozi = raw_input('can you show 5 baozi?(Y/N)')
    if baozi == 'Y':
        print '我买了五个包子'
    else:
        print '我买0个包子'

print '老婆我东西卖完，回家喽'
