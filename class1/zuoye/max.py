#/usr/bin/python
# ^_^ coding: utf-8 ^_^
list_num = [1,2,3,2,12,3,1,3,21,2,2,3,4111,22,3333,444,111,4,5,777,65555,65555,45,33,45]
list_num = sorted(list_num,reverse = True)
max_1 = list_num[0]
for max_2 in list_num:
    if max_2 < max_1:
        break
print 'first  num:%d \nsecond num:%d' % (max_1,max_2)
