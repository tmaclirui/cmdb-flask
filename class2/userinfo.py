#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
userinfo=[]
info=[]
while True:
    user=raw_input('please input your info,for exapmle user:id,or input stop:')
    userinfo.append(user)
    if user=='stop':
        userinfo.pop()
        break
for i in range(len(userinfo)-1):
    info.append(tuple(userinfo[i].split(':')))
print info
    

