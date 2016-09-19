#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
lngs = ['C','js','python','js','css','js','html','node','js','python','js','css','js','html','node','js','python','js','css','js','html','node','css','js','html','node','js','python','js','css','js','html','node','js','python','js','css','js','html','node']
lng_status = {}
for lng in lngs:
    cnt = lng_status.get(lng,0)
    lng_status[lng]= cnt + 1
print lng_status
