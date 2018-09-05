#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
if __name__ == '__main__':
    print 'start'
    try:
        1/0
    except BaseException as e:
        print e
    print 'end'
