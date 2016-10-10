#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
unsort_list2 = [(1,2),(6,3),(4,1),(2,10),(3,5),(5,7)]
def compare(value):
    if value[0] > value[1]:
        return value[0]
    else:
        return value[1]
unsort_list = sorted(unsort_list2,key = lambda v: compare(v))
print unsort_list
