#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
year = raw_input('please year: ')
year = int(year)
if year % 4 == 0 and year % 100 !=0:
    print ' %s is rongnian' % year
else:
    if year % 400 == 0:
        print ' %s is rongnian' % year
    else:
        print ' %s is not rongnian' % year
