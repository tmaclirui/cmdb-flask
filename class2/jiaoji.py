#!/usr/bin/python
# coding: utf-8
arr1 = [1,2,3,4,2,12,3,14,3,2,12,3,14,3,21,2,2,3,4111,22,3333,4]
arr2 = [2,1,3,2,43,234,454,452,234,14,21,14]
arr1_ = []
arr2_ = []
arr = []
for i in arr1:
	if not i in arr1_:
		arr1_.append(i)
for j in arr2:
	if not j in arr2_:
		arr2_.append(j)
for i in arr1_:
	if i in arr2_:
		arr.append(i)
print arr
    
