#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
import json
import gconf
import MySQLdb
from utils import dbutils
import datetime
from utils import crypt
import time 
import  geoip2.database
import  os


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

#用户管理

#end
# 资产管理
SQL_VALIDATE_ASSETS_MODIFY = 'select id from asset where id != %s and hostname = %s'
SQL_ASSETS_MODIFY= 'update asset set sn=%s,hostname=%s,os=%s,ip=%s,machine_room_id=%s,vendor=%s,model=%s,ram=%s,cpu=%s,disk=%s,time_on_shelves=%s,over_guaranteed_date=%s,buiness=%s,admin=%s,status=%s where id=%s'
SQL_ASSETS_DELETE = 'delete from asset where id = %s'
SQL_ASSETS_SAVE = 'insert into asset(sn,hostname,os,ip,machine_room_id,vendor,model,ram,cpu,disk,time_on_shelves,over_guaranteed_date,buiness,admin,status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
SQL_ASSET_LIST_COLUMNS = 'id,sn,hostname,os,ip,machine_room_id,vendor,model,ram,cpu,disk,time_on_shelves,over_guaranteed_date,buiness,admin,status'.split(',')
SQL_ASSET_LIST = 'select id,sn,hostname,os,ip,machine_room_id,vendor,model,ram,cpu,disk,time_on_shelves,over_guaranteed_date,buiness,admin,status from asset where status!=2;'
SQL_ASSET_BY_ID = 'select id,sn,hostname,os,ip,machine_room_id,vendor,model,ram,cpu,disk,time_on_shelves,over_guaranteed_date,buiness,admin,status from asset  where id=%s'
SQL_ASSET_BY_IP = 'select id,sn,hostname,os,ip,machine_room_id,vendor,model,ram,cpu,disk,time_on_shelves,over_guaranteed_date,buiness,admin,status from asset where status!=2 and ip=%s;'
SQL_MONITOR_HOST_LIST = 'select m_time,cpu,mem,disk from monitor_host where ip=%s and r_time>=%s order by m_time asc'
#end
#监控
SQL_MONITOR_HOST_CREATE =  'insert into monitor_host(ip, mem, cpu, disk, m_time, r_time) values(%s, %s, %s, %s, %s, %s)'

#告警

SQL_ALERT_LIST_COLUMNS = 'id,ip,message,admin,status,type,c_time'.split(',')
SQL_ALERT_LIST = 'select id,ip,message,admin,status,type,c_time from alert  where status!=2;'
SQL_ALERT_BY_ID = 'select id,ip,message,admin,status,type,c_time from alert  where id=%s'
SQL_ALERT_DELETE = 'delete from alert where id = %s'


SQL_ACCESSLOG_SAVE = 'insert into accesslog(a_time, ip, url, code, city_name) values(%s, %s, %s, %s, %s)'
SQL_GEOIP_CITY_NAME_EXISTS = 'select id from geoip where city_name=%s limit 1'
SQL_GEOIP_SAVE = 'insert into geoip(city_name, city_lat, city_lgt) values(%s, %s, %s)'

SQL_ACCESS_LIST = 'select ip,url,code,count(*) as cnt from accesslog group by ip, url, code order by cnt desc limit %s'

SQL_ACCESSLOG_CODE_DIST = 'select code, count(*) as cnt from accesslog group by code order by cnt desc'
SQL_ACCESSLOG_CODE_TIME_DIST = " select date_format(a_time, '%%Y-%%m-%%d %%H:00:00') as time, code, count(*) as cnt from accesslog group by time, code"

SQL_GEOIP_LIST = 'select city_name, city_lat, city_lgt from geoip'
SQL_ACCESS_IP_DIST = 'select city_name, count(*) as cnt from accesslog group by city_name'

def nginxlog(n=10):
    _, rt_list = dbutils.execute_sql(SQL_ACCESS_LIST, (n, ), True)
    return rt_list



#机房管理
def get_machines():
    sql = SQL_MACHINE_LIST
    args=()
    rt_cnt,rt_list=dbutils.execute_sql(sql,args,is_fetch=True)
    return [dict(zip(SQL_MACHINE_LIST_COLUMNS,line))  for line in rt_list]

def add_machines(name,addr,ip_ranges):
    sql = SQL_MACHINE_SAVE
    args = (name,addr,ip_ranges)
    cnt,rt=dbutils.execute_sql(sql,args,is_fetch=False)
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
    args = (uid,)
    machines_list = []
    rc_cnt,rt_list = dbutils.execute_sql(SQL_MACHINE_BY_ID,args,is_fetch=True)
    for rt in rt_list:
        machine_list = dict(zip(SQL_MACHINE_BY_ID_COLUMNS,rt))
        machines_list.append(machine_list)
    return  machines_list[0] if  machines_list else {}

def validate_machine_modify(uid,name,addr,ip_ranges):
    if not get_machine_by_id(uid):
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
    sql = SQL_VALIDATE_MACHINE_MODIFY
    args = (uid, name.strip())
    cnt,rt=dbutils.execute_sql(sql,args,is_fetch=True)
    if cnt != 0:
        return False, 'name is same to other'
    return True,''

def machine_modify(uid,name,addr,ip_ranges):
    sql = SQL_MACHINE_MODIFY
    args = (name,addr,ip_ranges,uid)
    cnt,rt=dbutils.execute_sql(sql,args,is_fetch=False)
    return True

def machine_delete(uid):
    sql = SQL_MACHINE_DELETE
    args = (uid,)
    cnt,rt=dbutils.execute_sql(sql,args,is_fetch=False)
    return True

# 资产管理    
def get_assets():
    rc_cnt,rt_list = dbutils.execute_sql(SQL_ASSET_LIST,(),True)
    assets = []
    rooms = get_machine_rooms_index_by_id()
    for rt in rt_list:
        asset = dict(zip(SQL_ASSET_LIST_COLUMNS,rt))
        for key in 'time_on_shelves,over_guaranteed_date'.split(','):
            if asset[key]:
                asset[key] = asset[key].strftime('%Y-%m-%d')
        asset['machine_room_name'] = rooms.get(asset['machine_room_id'],{}).get('name','')
        assets.append(asset)
    return assets

def get_asset_by_id(aid):
    args = (aid,)
    rc_cnt,rt_list = dbutils.execute_sql(SQL_ASSET_BY_ID,args,True)
    assets = []
    for rt in rt_list:
        asset = dict(zip(SQL_ASSET_LIST_COLUMNS,rt))
        for key in 'time_on_shelves,over_guaranteed_date'.split(','):
            if asset[key]:
                asset[key] = asset[key].strftime('%Y-%m-%d')
        assets.append(asset)
    return assets[0] if assets else {}

def get_asset_by_ip(ip):
    rt_cnt,rt_list = dbutils.execute_sql(SQL_ASSET_BY_IP, (ip,), True)
    assets = []
    for rt in rt_list:
        asset = dict(zip(SQL_ASSET_LIST_COLUMNS, rt))
        for key in 'time_on_shelves,over_guaranteed_date'.split(','):
            if asset[key]:
                asset[key] = asset[key].strftime('%Y-%m-%d')
        assets.append(asset)
    return assets[0] if assets else {}
    
def add_assets(sn,hostname,os,ip,machine_room_id,vendor,model,ram,cpu,disk,time_on_shelves,over_guaranteed_date,buiness,admin,status):
    sql = SQL_ASSETS_SAVE
    args = (sn,hostname,os,ip,machine_room_id,vendor,model,ram,cpu,disk,time_on_shelves,over_guaranteed_date,buiness,admin,status)
    rc_cnt,rt_list = dbutils.execute_sql(SQL_ASSETS_SAVE,args,False)
    assets = []
    for rt in rt_list:
        asset = dict(zip(SQL_ASSET_LIST_COLUMNS,rt))
        for key in 'time_on_shelves,over_guaranteed_date'.split(','):
            if asset[key]:
                asset[key] = asset[key].strftime('%Y-%m-%d')
        assets.append(asset)
    return rc_cnt !=0 

def validate_assets_save(hostname):
    if hostname.strip()=='':
        return False,'hostname is empty'
    return True,''

def assets_delete(uid):
    sql = SQL_ASSETS_DELETE
    args = (uid,)
    cnt,rt=dbutils.execute_sql(sql,args,is_fetch=False)
    return True

def add_assets_update(uid,sn,hostname,os,ip,machine_room_id,vendor,model,ram,cpu,disk,time_on_shelves,over_guaranteed_date,buiness,admin,status):
    sql = SQL_ASSETS_MODIFY
    args = (sn,hostname,os,ip,machine_room_id,vendor,model,ram,cpu,disk,time_on_shelves,over_guaranteed_date,buiness,admin,status,uid)
    cnt,rt=dbutils.execute_sql(sql,args,is_fetch=False)
    return True

def validate_assets_update(uid,hostname):
    if hostname.strip()=='':
        return False,'hostname is empty'
    sql = SQL_VALIDATE_ASSETS_MODIFY
    args = (uid, hostname.strip())
    cnt,rt=dbutils.execute_sql(sql,args,is_fetch=True)
    if cnt != 0:
        return False, 'name is same to other'
    return True,''

def get_machine_rooms_index_by_id():
    rt_list = get_machines()
    rt_dict = {}
    for room in rt_list:
        rt_dict[room['id']] = room
    return rt_dict

def monitor_host_create(req):
    values = []
    for key in ['ip','mem','cpu','disk','m_time']:
        values.append(req.get(key,''))
    values.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    dbutils.execute_sql(SQL_MONITOR_HOST_CREATE,values,False)
    return True 

def monitor_host_list(ip):
    start_time = (datetime.datetime.now() - datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
    rt_cnt,rt_list = dbutils.execute_sql(SQL_MONITOR_HOST_LIST,(ip,start_time),True)
    categoy_list,cpu_list,disk_list,mem_list = [],[],[],[]
    for line in rt_list:
        categoy_list.append(line[0].strftime('%H:%M'))
        cpu_list.append(line[1])
        mem_list.append(line[2])
        disk_list.append(line[3])

    return  {'categories': categoy_list,
            'series': [{
                    'name': 'cpu',
                    'data': cpu_list
                }, {
                    'name': '内存',
                    'data': mem_list
                }, {
                    'name': '磁盘',
                    'data': disk_list
                }]
        }
    
#修改密码
def validate_password_modify(uid,password,admin_uid,admin_password):
    if not get_user_by_id(uid):
        return False,u'用户不存在'
    if not validate_password(admin_uid,admin_password):
        return False,u'管理员密码错误'
    if password.strip()=='':
        return False,u'密码不能为空'
    if len(password.strip()) > 25:
        return False,u'密码长度过长'
    if len(password.strip()) < 6:
        return False,u'密码过短了'
    return True,''

def password_modify(uid,password):
    dbutils.execute_sql(SQL_USER_PASSWORD_MODIFY,(crypt.md5_str(password.strip()),uid),False)
    return True

#告警

def get_alerts():
    rc_cnt,rt_list = dbutils.execute_sql(SQL_ALERT_LIST,(),True)
    alerts = []
    for rt in rt_list:
        alert = dict(zip(SQL_ALERT_LIST_COLUMNS,rt))
        for key in 'c_time'.split(','):
            if alert[key]:
                alert[key] = alert[key].strftime('%Y-%m-%d')
        alerts.append(alert)
    return alerts

def get_alert_by_id(uid):
    rt_cnt,rt_list = dbutils.execute_sql(SQL_ALERT_BY_ID, (uid,), True)
    alerts = []
    for rt in rt_list:
        alert = dict(zip(SQL_ALERT_LIST_COLUMNS, rt))
        for key in 'c_time'.split(','):
            if alert[key]:
                alert[key] = alert[key].strftime('%Y-%m-%d')
        alerts.append(alert)
    return alerts[0] if alerts else {}

def alerts_delete(uid):
    sql = SQL_ALERT_DELETE
    args = (uid,)
    cnt,rt=dbutils.execute_sql(sql,args,is_fetch=False)
    return True
#------------------------------------------------------------------------------------------------------------------#
class User(object):
    KEY = 'id'
    SQL_LOGIN = 'select id, name from user where name = %s and password = %s'
    SQL_LOGIN_COLUMNS = ('id', 'name')

    SQL_LIST_COLUMNS = ('id', 'name', 'age','department','sex','birthday','email','hobby')
    SQL_LIST = 'select id, name, age,department,sex,birthday,email,hobby from user'

    SQL_SAVE = 'insert into user(name, age, password,department,sex,birthday,email,hobby) values(%s, %s, %s,%s,%s,%s,%s,%s)'

    SQL_GET_BY_KEY_COLUMNS = ('id', 'name', 'age','department','sex','birthday','email','hobby')
    SQL_GET_BY_KEY = 'select id, name, age,department,sex,birthday,email,hobby from user where {key} = %s'

    SQL_MODIFY = 'update user set name=%s, age=%s,department=%s,sex=%s,birthday=%s,email=%s,hobby=%s where id=%s'

    SQL_VALIDATE_PASSWORD = 'select * from user where id = %s and password = %s'
    SQL_PASSWORD_MODIFY = 'update user set password= %s where id=%s'

    SQL_DELETE_BY_KEY = 'delete from user where {key} = %s'

    def __init__(self,id,username,password,age,department,sex,birthday,email,hobby):
        self.id = id
        self.username = username.strip()
        self.password = password.strip()
        self.age = age
        self.department = department
        self.sex = sex
        self.birthday = birthday
        self.email = email
        self.hobby = hobby

    @classmethod
    def login(cls,username,password):
        rt_cnt,rt=dbutils.execute_sql(cls.SQL_LOGIN,(username,crypt.md5_str(password)),is_fetch=True)
        return None  if len(rt) == 0 else dict(zip(cls.SQL_LOGIN_COLUMNS,rt[0]))

    @classmethod
    def validate_password(cls,uid,password):
        rt_cnt,rt=dbutils.execute_sql(cls.SQL_VALIDATE_PASSWORD,(uid,crypt.md5_str(password)),is_fetch=True)
        return rt_cnt > 0

    @classmethod
    def get_list(cls):
        users_list = []
        rt_cnt,rt_list=dbutils.execute_sql(cls.SQL_LIST,(),is_fetch=True)
        for line in rt_list:
            user_list = dict(zip(cls.SQL_LIST_COLUMNS,line))
            user_list['birthday'] = user_list['birthday'].strftime('%Y-%m-%d')
            users_list.append(user_list)
        return users_list 

    def validate_save(self):
        if self.username =='':
            return False,u'用户名不能为空'
        if len(self.username) > 25:
            return False,u'用户名的长度不能超过25'
        if self.password =='':
            return False,u'密码不能为空'
        if len(self.password) < 6 or len(self.password) > 25:
            return False,u'密码长度在6到25之间'
        if not str(self.age).isdigit() or int(self.age)<1 or int(self.age)>100:
            return False,u'年龄在1到100之间'

        user = self.get_by_key(self.username,'name')
        if user:
            return False,u'用户名不能重复'

        return True,''

    def save(self):
        cnt,rt=dbutils.execute_sql(self.SQL_SAVE,(self.username,
                                             self.age,
                                             crypt.md5_str(self.password),
                                             self.department,
                                             self.sex,
                                             self.birthday,
                                             self.email,
                                             self.hobby),is_fetch=False)
        return cnt !=0 

    @classmethod
    def get_by_key(cls,value,key=None):
        sql = cls.SQL_GET_BY_KEY.format(key=cls.KEY if key is None else key)
        cnt,rt_list = dbutils.execute_sql(sql,(value,),True)
        return dict(zip(cls.SQL_GET_BY_KEY_COLUMNS,rt_list[0])) if rt_list else None 

    def validate_modify(self):
        if not self.get_by_key(self.id ):
            return False,u'用户不存在'
        if self.username=='':
            return False,u'用户名是空的'
        if len(self.username) > 25:
            return False,u'用户名长度不能超过25'
        if not str(self.age).isdigit() or int(self.age) < 1 or int(self.age) > 100:
            return False, u'年龄必须在1到100之间'
       
        user = self.get_by_key(self.username,'name')
        if user  and  str(user['id']) != str(self.id):
            return False,u'用户名不能重复'

        return True,''

    def modify(self):
        
        args = (self.username,self.age,self.department,self.sex,self.birthday,self.email,self.hobby,self.id)
        dbutils.execute_sql(self.SQL_MODIFY,args,is_fetch=False)
        return True 

    def validate_password_modify(self):
        if not self.get_by_key(self.id):
            return False,u'用户不存在'
        if self.password=='':
            return False,u'密码不能为空'
        if len(self.password) > 25:
            return False,u'密码长度过长'
        if len(self.password) < 6:
            return False,u'密码过短了'
        return True,''

    def password_modify(self):
        dbutils.execute_sql(self.SQL_PASSWORD_MODIFY,(crypt.md5_str(self.password),self.id),False)

        return True
    
    @classmethod
    def delete_by_key(cls,value,key=None):
        sql = cls.SQL_DELETE_BY_KEY.format(key=cls.KEY if key is None else key)
        dbutils.execute_sql(sql,(value,),False)
        return True

def access_log_import(filename):
    if os.path.exists(filename):
        fhandler = None
        geo_reader = None
        db_connection = None
        db_cursor = None

        try:
            fhandler = open(filename,'rb')
            geo_reader = geoip2.database.Reader(gconf.GeoLite2)
            db_connection = MySQLdb.connect(host=gconf.MYSQL_HOST,\
                                   port=gconf.MYSQL_PORT,\
                                   user=gconf.MYSQL_USER,\
                                   passwd=gconf.MYSQL_PASSWD,\
                                   db=gconf.MYSQL_DB,\
                                   charset=gconf.MYSQL_CHARSET)
            db_cursor = db_connection.cursor()
            line_count = 0
            for line in fhandler:
                try:
                    elements = line.split()
                    #time,ip,url,code

                    a_time = time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(elements[3],'[%d/%b/%Y:%H:%M:%S'))
                    ip = elements[0]
                    url = elements[6]
                    code = elements[8]
                    response = geo_reader.city(ip)
                    if response.country.names.get('en','').lower() == 'china':
                        city_name = response.city.names.get('zh-CN','')
                        if city_name:
                            city_lat = response.location.latitude
                            city_lgt = response.location.longitude
                            print ip,url,code,city_name,city_lat,city_lgt
                            db_cursor.execute(SQL_ACCESSLOG_SAVE,(a_time, ip, url, code, city_name))

                            if 0 == db_cursor.execute(SQL_GEOIP_CITY_NAME_EXISTS,(city_name,)):
                                db_cursor.execute(SQL_GEOIP_SAVE,(city_name,city_lat,city_lgt))
                            line_count += 1

                            if line_count ==1000:
                                db_connection.commit()
                                line_count = 0

                except BaseException as e:
                    print e

        except BaseException as e:
            print e 

        finally:
            if db_cursor:
                db_cursor.close()
            if db_connection:
                db_connection.commit()
                db_connection.close()
            if geo_reader:
                geo_reader.close()
            if fhandler:
                fhandler.close()
                os.unlink(filename)

def accesslog_code_dist():
    _,rt_list = dbutils.execute_sql(SQL_ACCESSLOG_CODE_DIST,(),True)
    legend = []
    data = []

    for line in rt_list:
        legend.append(line[0])
        data.append({'value':line[1],'name':line[0]})

    return legend,data

def accesslog_code_time_dist():
    legend = []
    xAxis = []
    data = []
    temp_data = {}

    _,rt_list = dbutils.execute_sql(SQL_ACCESSLOG_CODE_TIME_DIST,(),True)

    for line in rt_list:
        if line[0] not in xAxis:
            xAxis.append(line[0]) # time
        if line[1] not in legend: # code
            legend.append(line[1])
        #line[2] # count
        temp_data.setdefault(line[1],{})
        temp_data[line[1]][line[0]] = line[2]
    xAxis.sort()

    for code in temp_data:
        code_time_data = []
        for time in xAxis:
            code_time_data.append(temp_data[code].get(time,0))
        data.append({'name' : code,'type' : 'bar','stack':'code','data':code_time_data})

    return legend,xAxis,data

def accesslog_ip_dist():
    legend =[]
    geoCoord = {}
    markline_data = []
    markpoint_data = []


    server_ip = '47.153.191.255'

    geo_reader = geoip2.database.Reader(gconf.GeoLite2)
    server_response = geo_reader.city(server_ip)
    geo_reader.close()

    server_city_name = server_response.city.names.get('zh-CN', u'北京')
    legend.append(server_city_name)

    geoCoord[server_city_name] = [server_response.location.longitude, server_response.location.latitude]

    _, rt_list = dbutils.execute_sql(SQL_GEOIP_LIST, (), True)

    for line in rt_list:
        geoCoord[line[0]] = [line[2], line[1]]

    _, rt_list = dbutils.execute_sql(SQL_ACCESS_IP_DIST, (), True)
    for line in rt_list:
        markline_data.append([{'name' : line[0]}, {'name' : server_city_name, 'value' : line[1]}])
        markpoint_data.append({'name': line[0], 'value' : line[1]})

    return legend, geoCoord, markline_data, markpoint_data

if __name__=='__main__':
    print 'ok'


