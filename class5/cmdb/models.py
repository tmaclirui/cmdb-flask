#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
import json
import gconf

def get_users():
    fh = open(gconf.USER_DB_PATH,'r')
    users = json.loads((fh.read()))
    fh.close()
    return users

def save_users(users):
    fh = open(gconf.USER_DB_PATH,'w')
    fh.write(json.dumps(users))
    fh.close()   

def add_users(username,password):
    _users = get_users()
    _users_tmp = sorted(_users,key=lambda v: v['id'],reverse=True)
    id = _users_tmp[0]['id'] + 1
    _user = { 'id':id,'name':username,'password':password}
    _users.append(_user)
    save_users(_users)

def validate_login(username,password):
    users = get_users()
    for user in users:
        if user.get('name')==username and user.get('password') == password:
           return user
    return None

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