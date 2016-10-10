#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
def cmp_value(v1,v2):
    return v1 > v2
def bubble_sort(unsort_list):
    length=len(unsort_list)
    for j in range(0,length-1):
        for i in range(0,length-1):
            if cmp_value(unsort_list[i],unsort_list[i+1]):
                unsort_list[i],unsort_list[i+1]=unsort_list[i+1],unsort_list[i]

unsort_list=[7,8,1,6,2,3,9,10]
bubble_sort(unsort_list)
print unsort_list
