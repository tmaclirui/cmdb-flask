#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
#打开文件
log_file = open('www_access_20140823.log','r')
rs = {}
for l in log_file:
    # 每循环一次就把一行的内容用空格切割，并将对应的值赋值给ip,url,status
    a = l.split(' ')
    ip = a[0]
    url = a[6]
    status = a[8]
    #（ip,url,status）这个元组作为key，如果key不存在，就返回默认值，并加1
    rs[(ip,url,status)] = rs.get((ip,url,status),0) + 1 
# for循环得到的值赋值给for前面的表达式，rs_list是一个列表
rs_list = [(k[0],k[1],k[2],v) for k,v in rs.items() ]
# 用sorted排序，rs_list,是一个可迭代的对象，key是一个匿名函数lambda，每次
# 将列表中的元素赋值给key，通过key排序
for k in sorted(rs_list,key=lambda v: v[3],reverse=True)[:10]:
        print k

