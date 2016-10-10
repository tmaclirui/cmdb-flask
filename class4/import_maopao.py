#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
import maopao2
import sys
print sys.path
print globals()
unsort_list2 = [(1, 2), (6, 3), (4, 1), (2, 10), (3, 5), (5, 7)]
unsort_list1 = [2,3,1,4,9,5,10,6,8]
maopao2.bubble_sort(unsort_list1)
maopao2.bubble_sort(unsort_list2,key=maopao2.get_tuplekey)
print unsort_list1
print unsort_list2
