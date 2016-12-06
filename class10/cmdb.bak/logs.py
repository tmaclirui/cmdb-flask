# ^_^ coding: utf-8 ^_^
#打开文件
def nginxlog(log_file,n=10):
    log_file = open(log_file,'r')
    rs = {}
    for l in log_file:
        a = l.split(' ')
        ip = a[0]
        url = a[6]
        status = a[8]
        rs[(ip,url,status)] = rs.get((ip,url,status),0) + 1 
    rs_list = [(k[0],k[1],k[2],v) for k,v in rs.items() ]
    rs_list2 = sorted(rs_list,key=lambda v: v[3],reverse=True)[:n]
    return rs_list2
    log_file.close()
if __name__=='__main__':
    log_file = '/opt/nginx/logs/access.log'
    result=nginxlog(log_file)
    tbody = ' '
    for  line  in result:
     tbody=tbody +  '''<tr>
            <td>{ip}</td>
            <td>{url}</td>
            <td>{status}</td>
            <td>{count}</td>
            </tr>'''.format(ip=line[0],url=line[1],status=line[2],count=line[3])

    html = '''<!DOCTYPE html>
 <html>
     <head>
        <!--  我是一个注释-->
      <meta charset="utf-8" />
      <title> 我是李瑞</title>
  </head>
  <body>
     <table border="1">
        <thead>
            <tr>
            <th>ip</th>
            <th>url</th>
            <th>status</th>
            <th>count</th>
        </tr>
        </thead>
        <tbody>
            {tbody}
        </tbody>
     </table>   
  </body>
  </html>'''.format(tbody=tbody)
    fh = open('topn.html','w')
    fh.write(html)
    fh.close()