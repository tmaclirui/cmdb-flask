#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
def add_multi(m,n):
    add = 0
    multi = 1
    for i in range(m,n+1):
        add = add + i
        multi = multi * i
    return add,multi
print add_multi(1,2)
