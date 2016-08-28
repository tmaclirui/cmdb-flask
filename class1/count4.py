#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
danci = {}
list_danci = ['C','js','python','js','css','js','html','node','js','python','js','css','js','html','node','js','python','js','css','js','html','node','css','js','html','node','js','python','js','css','js','html','node','js','python','js','css','js','html','node']
for name in list_danci:
    if not( name in danci):
        danci[name] = 1
    else:
        danci[name] += 1

print danci
        
        

