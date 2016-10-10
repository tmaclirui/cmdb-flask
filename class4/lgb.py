#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
a = 1
b = []
c = []
m = 10
def change(x,y,z):
    m,n = 1,2
    print locals()
    globals_dict = globals()
    print globals_dict
    print dir(globals_dict['__builtins__'])
    print "**********"
    print a
    print n
    print m
    print "**********"
if __name__=='__main__':
    change(a,b,c)
    print a,b,c,m
