#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
num = [1,2,555,999,34,123,9878,4,666]
for i in range(len(num)-1):
    for j in range(i+1,len(num)):
        if num[i] > num[j]:
            num[i],num[j] = num[j],num[i]
print num
 
