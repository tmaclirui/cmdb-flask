#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
lngs = ['C','js','python','js','css','js','html','node','js','python','js','css','js','html','node','js','python','js','css','js','html','node','css','js','html','node','js','python','js','css','js','html','node','js','python','js','css','js','html','node']
lng_status = {}
for lng in lngs:
    lng_status.setdefault(lng,0)
    lng_status[lng]+=1
print lng_status

