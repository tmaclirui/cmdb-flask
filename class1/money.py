#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
money  = raw_input('please you a num:')
money = int(money)
sum = money * 2
rate  = 0.03
year = 0
while money <= sum:
    money = money*(1 + rate)
    year = year + 1
print ' %s is double, money is %s' % (year,money)



