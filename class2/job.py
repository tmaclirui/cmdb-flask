#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
jobs =[]
while True:
    string = raw_input('please input you string:')
    if string == 'add':
        renwu = raw_input('please input your jobs:')
        jobs.append(renwu)
    elif string =='do':
        if len(jobs)==0:
            print 'no job'
            break
        else:
            ok  = jobs.pop(0)
            print 'the job is %s' % ok
    elif string !='add' and string !='do':
        print 'you input have error'
   
       
