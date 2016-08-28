#!/usr/bin/python
# coding: utf-8
num = [5,6,9,8,7]
max_ = None
for i in num:
    if max_ is None:
        max_ = i
    elif max_ < i:
        max_ = i
print max_

