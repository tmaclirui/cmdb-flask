#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
#打开文件
log = raw_input('请输入你的nginx或者httpd的日志路径: ')
dstpath=raw_input('请输入你的分析之后的nginx的日志文件路径: ')
log_file = open(log,'r')
def nginxlog(log_file,dstpath,n=10):
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
    dst_file = open(dstpath,'w')
    rs_list2 = sorted(rs_list,key=lambda v: v[3],reverse=True)
    rs_list2 = [(v[0],v[1],v[2],str(v[3])) for v in rs_list2 ]
    for k in rs_list2[:n]:
        k= ' '.join(k)
        print k
        dst_file.write(k + '\n') 
    log_file.close()        
    dst_file.close()
if __name__=='__main__':
    nginxlog(log_file,dstpath)
