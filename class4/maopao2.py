#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
def cmp_value(a,b):
    return a > b
def get_key(x):
    return x
def get_tuplekey(x):
    return x[1]
def bubble_sort(unsort_list,cmp=cmp_value,key=get_key):
    length=len(unsort_list)
    for j in range(0,length-1):
        for i in range(0,length-1):
            if cmp(key(unsort_list[i]),key(unsort_list[i+1])):
                unsort_list[i],unsort_list[i+1]=unsort_list[i+1],unsort_list[i]
unsort_list2 = [(1, 2), (6, 3), (4, 1), (2, 10), (3, 5), (5, 7)]
unsort_list1 = [2,3,1,4,9,5,10,6,8]
bubble_sort(unsort_list1)
bubble_sort(unsort_list2,key=get_tuplekey)
if __name__ == '__main__':
    print unsort_list1
    print unsort_list2
    print globals()
