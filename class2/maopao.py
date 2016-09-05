#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
num = [1,2,555,999,34,123,9878,4,666]
for j in range(1,len(num)):
    for i in range(len(num)-j):
        if num[i]> num[i+1]:
            num[i],num[i+1] = num[i+1],num[i]
print num

        
        
