#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
import json
import gconf
import MySQLdb
#机房管理
SQL_MACHINE_LIST = 'select id,name,addr,ip_ranges from machine_room'
SQL_MACHINE_LIST_COLUMNS = ('id','name','addr','ip_ranges')

SQL_MACHINE_SAVE = 'insert into machine_room(name,addr,ip_ranges) values(%s,%s,%s)'
SQL_MACHINE_BY_ID_COLUMNS = ('id', 'name', 'addr','ip_ranges')

SQL_MACHINE_MODIFY = 'update machine_room set name=%s, addr=%s,ip_ranges=%s where id=%s'

SQL_MACHINE_BY_ID = 'select id, name,addr,ip_ranges from machine_room where id=%s'
SQL_VALIDATE_MACHINE_MODIFY = 'select id from user where id != %s and name = %s'

SQL_MACHINE_DELETE = 'delete from machine_room where id = %s'
#end


SQL_VALIDATE_LOGIN_COLUMNS = ('id', 'name')

SQL_VALIDATE_LOGIN = 'select id, name from user where name = %s and password = md5(%s)'
SQL_USER_SAVE = 'insert into user(name, age, password) values(%s, %s, md5(%s))'

SQL_USER_LIST_COLUMNS = ('id', 'name', 'age')
SQL_USER_LIST = 'select id, name, age from user'

SQL_USER_BY_ID_COLUMNS = ('id', 'name', 'age')
SQL_USER_BY_ID = 'select id, name, age from user where id=%s'

SQL_USER_MODIFY = 'update user set name=%s, age=%s where id=%s'
SQL_VALIDATE_USER_MODIFY = 'select id from user where id != %s and name = %s'

SQL_USER_DELETE = 'delete from user where id = %s'

def get_users():
    conn = MySQLdb.connect(host=gconf.MYSQL_HOST,\
                       port=gconf.MYSQL_PORT,\
                       user=gconf.MYSQL_USER,\
                       passwd=gconf.MYSQL_PASSWD,\
                       db=gconf.MYSQL_DB,\
                       charset=gconf.MYSQL_CHARSET)
    cursor = conn.cursor()
    cursor.execute(SQL_USER_LIST)
    rt_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return [dict(zip(SQL_USER_LIST_COLUMNS,line))  for line in rt_list]

def validate_login(username,password):
    conn = MySQLdb.connect(host=gconf.MYSQL_HOST,\
                       port=gconf.MYSQL_PORT,\
                       user=gconf.MYSQL_USER,\
                       passwd=gconf.MYSQL_PASSWD,\
                       db=gconf.MYSQL_DB,\
                       charset=gconf.MYSQL_CHARSET)

    cursor = conn.cursor()
    cursor.execute(SQL_VALIDATE_LOGIN,(username,password))
    rt = cursor.fetchone()
    cursor.close()
    conn.close()
    return None if rt is None else dict(zip(SQL_VALIDATE_LOGIN_COLUMNS,rt))

def save_users(users):
    fh = open(gconf.USER_DB_PATH,'w')
    fh.write(json.dumps(users))
    fh.close()   

def get_user_by_id(uid):
    conn = MySQLdb.connect(host=gconf.MYSQL_HOST,\
                       port=gconf.MYSQL_PORT,\
                       user=gconf.MYSQL_USER,\
                       passwd=gconf.MYSQL_PASSWD,\
                       db=gconf.MYSQL_DB,\
                       charset=gconf.MYSQL_CHARSET)
    cursor = conn.cursor()
    cursor.execute(SQL_USER_BY_ID,(uid,))
    rt = cursor.fetchone()
    cursor.close()
    conn.close()
    return {} if rt is None else dict(zip(SQL_USER_BY_ID_COLUMNS,rt))

def validate_user_modify(uid,username,age):
    if not get_user_by_id(uid):
        return False,'user is not found'
    if username.strip()=='':
        return False,'username is empty'
    if len(username.strip()) > 25:
        return False,'username len is not gt 25'
    if not str(age).isdigit() or int(age) < 1 or int(age) > 100:
        return False, 'age is not a between 1 and 100 integer'
    conn = MySQLdb.connect(host=gconf.MYSQL_HOST, \
                            port=gconf.MYSQL_PORT, \
                            user=gconf.MYSQL_USER, \
                            passwd=gconf.MYSQL_PASSWD, \
                            db=gconf.MYSQL_DB, \
                            charset=gconf.MYSQL_CHARSET)

    cursor = conn.cursor()
    cnt = cursor.execute(SQL_VALIDATE_USER_MODIFY, (uid, username.strip()))
    cursor.close()
    conn.close()
    if cnt != 0:
        return False, 'username is same to other'
    return True,''

def user_modify(uid,username,age):
    conn = MySQLdb.connect(host=gconf.MYSQL_HOST,\
                       port=gconf.MYSQL_PORT,\
                       user=gconf.MYSQL_USER,\
                       passwd=gconf.MYSQL_PASSWD,\
                       db=gconf.MYSQL_DB,\
                       charset=gconf.MYSQL_CHARSET)
    cursor = conn.cursor()
    cnt = cursor.execute(SQL_USER_MODIFY,(username,age,uid))
    conn.commit()
    cursor.close()
    conn.close()
    return True

def user_delete(uid):
    conn = MySQLdb.connect(host=gconf.MYSQL_HOST,\
                       port=gconf.MYSQL_PORT,\
                       user=gconf.MYSQL_USER,\
                       passwd=gconf.MYSQL_PASSWD,\
                       db=gconf.MYSQL_DB,\
                       charset=gconf.MYSQL_CHARSET)
    cursor = conn.cursor()
    cnt = cursor.execute(SQL_USER_DELETE,(uid,))
    conn.commit()
    cursor.close()
    conn.close()
    return True

def add_users(username,password,age):
    conn = MySQLdb.connect(host=gconf.MYSQL_HOST,\
                       port=gconf.MYSQL_PORT,\
                       user=gconf.MYSQL_USER,\
                       passwd=gconf.MYSQL_PASSWD,\
                       db=gconf.MYSQL_DB,\
                       charset=gconf.MYSQL_CHARSET)
    cursor = conn.cursor()
    cnt = cursor.execute(SQL_USER_SAVE,(username,age,password))
    conn.commit()
    cursor.close()
    conn.close()
    return cnt !=0 
    
def validate_login(username,password):
    conn = MySQLdb.connect(host=gconf.MYSQL_HOST,\
                       port=gconf.MYSQL_PORT,\
                       user=gconf.MYSQL_USER,\
                       passwd=gconf.MYSQL_PASSWD,\
                       db=gconf.MYSQL_DB,\
                       charset=gconf.MYSQL_CHARSET)
    cursor = conn.cursor()
    cursor.execute(SQL_VALIDATE_LOGIN,(username,password))
    record = cursor.fetchone()
    rt = None
    if record is not None:
        rt = {'id': record[0],'name':record[1]}
    cursor.close()
    conn.close()
    return rt 
    
def validate_user_save(username,password,age):
    if username.strip()=='':
        return False,'username is empty'
    if len(username.strip()) > 25:
        return False,'username len is not gt 25'
    if password.strip()=='':
        return False,'password is empty'
    if len(password.strip()) < 6 or len(password.strip()) > 25:
        return False,'password len is between 6 and 25'
    if not str(age).isdigit() or int(age)<1 or int(age)>100:
        return False,'age is not a between 1 and 100'

    return True,''

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



#机房管理
def get_machines():
    conn = MySQLdb.connect(host=gconf.MYSQL_HOST,\
                       port=gconf.MYSQL_PORT,\
                       user=gconf.MYSQL_USER,\
                       passwd=gconf.MYSQL_PASSWD,\
                       db=gconf.MYSQL_DB,\
                       charset=gconf.MYSQL_CHARSET)
    cursor = conn.cursor()
    cursor.execute(SQL_MACHINE_LIST)
    rt_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return [dict(zip(SQL_MACHINE_LIST_COLUMNS,line))  for line in rt_list]

def add_machines(name,addr,ip_ranges):
    conn = MySQLdb.connect(host=gconf.MYSQL_HOST,\
                       port=gconf.MYSQL_PORT,\
                       user=gconf.MYSQL_USER,\
                       passwd=gconf.MYSQL_PASSWD,\
                       db=gconf.MYSQL_DB,\
                       charset=gconf.MYSQL_CHARSET)
    cursor = conn.cursor()
    cnt = cursor.execute(SQL_MACHINE_SAVE,(name,addr,ip_ranges))
    conn.commit()
    cursor.close()
    conn.close()
    return cnt !=0 

def validate_machine_save(name,addr,ip_ranges):
    if name.strip()=='':
        return False,'machinename is empty'
    if len(name.strip()) > 25:
        return False,'machinename len is not gt 25'
    if addr.strip()=='':
        return False,'addr is empty'
    if len(addr.strip()) > 30:
        return False,'addr len is not gt 30'
    if len(ip_ranges.strip()) > 100:
        return False,'addr len is not gt 100'

    return True,''

def get_machine_by_id(uid):
    conn = MySQLdb.connect(host=gconf.MYSQL_HOST,\
                       port=gconf.MYSQL_PORT,\
                       user=gconf.MYSQL_USER,\
                       passwd=gconf.MYSQL_PASSWD,\
                       db=gconf.MYSQL_DB,\
                       charset=gconf.MYSQL_CHARSET)
    cursor = conn.cursor()
    cursor.execute(SQL_MACHINE_BY_ID,(uid,))
    rt = cursor.fetchone()
    cursor.close()
    conn.close()
    return {} if rt is None else dict(zip(SQL_MACHINE_BY_ID_COLUMNS,rt))

def validate_machine_modify(uid,name,addr,ip_ranges):
    if not get_user_by_id(uid):
        return False,'machine is not found'
    if name.strip()=='':
        return False,'machine name is empty'
    if len(name.strip()) > 25:
        return False,'name len is not gt 25'
    if addr.strip()=='':
        return False,'addr is empty'
    if len(addr.strip()) > 30:
        return False,'addr len is not gt 30'
    if len(ip_ranges.strip()) > 100:
        return False,'addr len is not gt 100'
    conn = MySQLdb.connect(host=gconf.MYSQL_HOST, \
                            port=gconf.MYSQL_PORT, \
                            user=gconf.MYSQL_USER, \
                            passwd=gconf.MYSQL_PASSWD, \
                            db=gconf.MYSQL_DB, \
                            charset=gconf.MYSQL_CHARSET)

    cursor = conn.cursor()
    cnt = cursor.execute(SQL_VALIDATE_MACHINE_MODIFY, (uid, name.strip()))
    cursor.close()
    conn.close()
    if cnt != 0:
        return False, 'name is same to other'
    return True,''

def machine_modify(uid,name,addr,ip_ranges):
    conn = MySQLdb.connect(host=gconf.MYSQL_HOST,\
                       port=gconf.MYSQL_PORT,\
                       user=gconf.MYSQL_USER,\
                       passwd=gconf.MYSQL_PASSWD,\
                       db=gconf.MYSQL_DB,\
                       charset=gconf.MYSQL_CHARSET)
    cursor = conn.cursor()
    cnt = cursor.execute(SQL_MACHINE_MODIFY,(name,addr,ip_ranges,uid))
    conn.commit()
    cursor.close()
    conn.close()
    return True

def machine_delete(uid):
    conn = MySQLdb.connect(host=gconf.MYSQL_HOST,\
                       port=gconf.MYSQL_PORT,\
                       user=gconf.MYSQL_USER,\
                       passwd=gconf.MYSQL_PASSWD,\
                       db=gconf.MYSQL_DB,\
                       charset=gconf.MYSQL_CHARSET)
    cursor = conn.cursor()
    cnt = cursor.execute(SQL_MACHINE_DELETE,(uid,))
    conn.commit()
    cursor.close()
    conn.close()
    return True

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