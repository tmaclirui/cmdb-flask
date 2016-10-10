#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
def cmp_value(v1,v2):
    return v1 > v2
def cmp_tuple(v1,v2):
    return v1[1] > v2[1]
def bubble_sort(unsort_list,cmp=cmp_value):
    length=len(unsort_list)
    for j in range(0,length-1):
        for i in range(0,length-1):
            if cmp(unsort_list[i],unsort_list[i+1]):
                unsort_list[i],unsort_list[i+1]=unsort_list[i+1],unsort_list[i]
unsort_list2 = [(1, 2), (6, 3), (4, 1), (2, 10), (3, 5), (5, 7)]
unsort_list1 = [2,3,1,4,9,5,10,6,8]
bubble_sort(unsort_list1)
bubble_sort(unsort_list2,cmp=cmp_tuple)
print unsort_list1
print unsort_list2
