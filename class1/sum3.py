#!/usr/bin/python
# coding: utf-8
total = 0
for x in range(5):
    if x ==3:
        continue
    total = total + x
print total 
total = 0
for x in range(5):
    if x ==3:
        break
    total = total + x
print total

