#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
from flask import render_template
from flask import request
from flask import redirect
from flask import session
import json

from cmdb import app
import models
import time
import datetime


@app.route('/users/save/',methods=['post'])
def users_save():
    if session.get('user') is None: return redirect('/')
    username = request.form.get('username','')
    password = request.form.get('password','')
    age = request.form.get('age',0)
    department = request.form.get('department','')
    sex = request.form.get('sex','')
    if request.form.get('birthday'):
        birthday = request.form.get('birthday')
    else:
        birthday = datetime.datetime.now()
    email = request.form.get('email')
    hobby = request.form.getlist('hobby')
    hobby = ' '.join(hobby)
    user = models.User(0,username,password,age,department,sex,birthday,email,hobby)
    ok,error = user.validate_save()
    if ok:
        user.save()
        return  json.dumps({'code':200})
    else:
        return  json.dumps({'code':400,'error': error})


@app.route('/users/view/')
def users_view():
    if session.get('user') is None: return redirect('/')
    user = models.User.get_by_key(request.args.get('id',0))
    user['birthday'] = user['birthday'].strftime('%Y-%m-%d')
    return json.dumps(user)


@app.route('/users/delete/')
def users_delete():
    if session.get('user') is None: return json.dumps({'code' : 403, 'error' : ''})
    models.User.delete_by_key(request.args.get('id', 0))
    return json.dumps({'code' : 200})

@app.route('/users/modify/',methods=['POST'])
def users_modify():
    if session.get('user') is None: return redirect('/')
    uid = request.form.get('id','')
    username = request.form.get('name','')
    age = request.form.get('age','')
    department = request.form.get('department','')
    sex = request.form.get('sex','')
    birthday = request.form.get('birthday')
    email = request.form.get('email')
    hobby = request.form.getlist('hobby')
    hobby = ' '.join(hobby)
    user = models.User(uid,username,'',age,department,sex,birthday,email,hobby)
    ok,error = user.validate_modify()
    if ok:
        user.modify()
        return json.dumps({'error':''})
    else:
        return  json.dumps({'code':400,'error': error})

@app.route('/users/password/modify/',methods=['POST'])
def password_modify():
    if session.get('user') is None: return  json.dumps({'code':400,'error': error})
    uid = request.form.get('id','')
    password = request.form.get('password','')
    admin_password = request.form.get('admin_password','')
    if  models.User.validate_password(session['user']['id'],admin_password):
        user = models.User(uid,'',password,'','','',datetime.datetime.now(),'','')
        ok,error = user.validate_password_modify()
        if ok:
            user.password_modify()
            return json.dumps({'code' : 200})
        return  json.dumps({'code':400,'error': error})
    else:
        return  json.dumps({'code':400,'error': u'管理员密码错误'})

@app.route('/users/')
def users():
    if session.get('user') is None: return redirect('/')
    return render_template('users.html',users=models.User.get_list())


@app.route('/users/list/')
def users_list():
    if session.get('user') is None: return redirect('/')
    users=models.User.get_list()
    print users
    return json.dumps({'data': users})
   
@app.route('/')
def index():
    if session.get('user'): return redirect('/users/')
    return  render_template('index.html')

@app.route('/login/',methods=['post','get'])
def login():
    if session.get('user'): return redirect('/users/')
    username = ''
    password = ''
    params = request.form if 'POST' == request.method  else request.args
    username = params.get('username','')
    password = params.get('password','')
    user = models.User.login(username,password)
    if user:
        session['user'] = user
        return redirect('/users/')
    else:
        return render_template('index.html',username=username,password=password,error=u"用户名或者密码错误")            

@app.route('/logs/')
def log():
    if session.get('user') is None: return redirect('/')
    topn= request.args.get('topn',10)
    topn= int(topn) if str(topn).isdigit() else 10
    log_file = '/data/lirui/access.log'
    result=models.nginxlog(log_file,topn)
    return  render_template('logs.html',logs=result)

#文件上传
@app.route('/log/upload/', methods=['POST'])
def log_upload():
    if session.get('user') is None: return redirect('/')
    file = request.files.get('log')
    if file:
        filename = file.filename
        file.save('/data/lirui/%s' % filename)
    return redirect('/logs/')

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/')



# 机房管理
@app.route('/machine/')
def machine():
    return render_template('machine.html',machines=models.get_machines())

@app.route('/machines/list/')
def machines_list():
    machines=models.get_machines()
    return json.dumps({'data': machines})

@app.route('/machine/create/')
def machine_create():
    return render_template('machine_create.html')

@app.route('/machine/save/',methods=['post'])
def machine_save():
    name = request.form.get('name','')
    addr = request.form.get('addr','')
    ip_ranges= request.form.get('ip_ranges','')
    ok,error = models.validate_machine_save(name,addr,ip_ranges)
    print ok
    if ok:
        models.add_machines(name, addr,ip_ranges)
        return  json.dumps({'code':200})
    else:
        return  json.dumps({'code':400,'error': error})
        
@app.route('/machine/view/')
def machine_view():
    machines = models.get_machine_by_id(request.args.get('id',0))
    return json.dumps(machines)
    


@app.route('/machine/modify/',methods=['POST'])
def machine_modify():
    uid = request.form.get('id','')
    name = request.form.get('name','')
    addr = request.form.get('addr','')
    ip_ranges = request.form.get('ip_ranges','')
    ok,error = models.validate_machine_modify(uid,name,addr,ip_ranges)
    if ok:
        models.machine_modify(uid,name,addr,ip_ranges)
        return json.dumps({'error':''})
    else:
        return  json.dumps({'code':400,'error': error})

@app.route('/machine/delete/')
def machine_delete():
    machines = models.get_machine_by_id(request.args.get('id',0))
    id=machines.get('id','')
    models.machine_delete(id)
    return json.dumps({'code':200})

#资产管理
@app.route('/assets/')
def assets():
    if session.get('user') is None: return redirect('/')
    machines_room = models.get_machines()
    return render_template('assets.html',machines_room=machines_room)

@app.route('/assets/list/')
def asset_list():
    assets = models.get_assets()
    return json.dumps({'data': assets})

@app.route('/assets/view/')
def asset_view():
    aid = request.args.get('id',0)
    asset = models.get_asset_by_id(aid)
    return json.dumps(asset)

@app.route('/assets/update/',methods=['POST'])
def assets_update():
    uid = request.form.get('id','')
    sn = request.form.get('sn','')
    hostname = request.form.get('hostname','')
    os = request.form.get('os','')
    ip = request.form.get('ip','')
    machine_room_id = request.form.get('machine_room_id','')
    vendor = request.form.get('vendor','')
    model = request.form.get('model','')
    ram = request.form.get('ram','')
    cpu = request.form.get('cpu','')
    disk = request.form.get('disk','')
    time_on_shelves = request.form.get('time_on_shelves','')
    over_guaranteed_date = request.form.get('over_guaranteed_date','')
    buiness = request.form.get('buiness','')
    admin = request.form.get('admin','')
    status = request.form.get('status','')
    ok,error = models.validate_assets_update(uid,hostname)
    if ok:
        models.add_assets_update(uid,sn,hostname,os,ip,machine_room_id,vendor,model,ram,cpu,disk,time_on_shelves,over_guaranteed_date,buiness,admin,status)
        return json.dumps({'error':''})
    else:
        return  json.dumps({'code':400,'error': error})

@app.route('/assets/save/',methods=['post'])
def assets_save():
    sn = request.form.get('sn','')
    hostname = request.form.get('hostname','')
    os = request.form.get('os','')
    ip = request.form.get('ip','')
    machine_room_id = request.form.get('machine_room_id','')
    vendor = request.form.get('vendor','')
    model = request.form.get('model','')
    ram = request.form.get('ram','')
    cpu = request.form.get('cpu','')
    disk = request.form.get('disk','')
    time_on_shelves = request.form.get('time_on_shelves','')
    over_guaranteed_date = request.form.get('over_guaranteed_date','')
    buiness = request.form.get('buiness','')
    admin = request.form.get('admin','')
    status = request.form.get('status','')

    ok,error = models.validate_assets_save(hostname)
    if ok:
        models.add_assets(sn,hostname,os,ip,machine_room_id,vendor,model,ram,cpu,disk,time_on_shelves,over_guaranteed_date,buiness,admin,status)
        return  json.dumps({'code':200})
    else:
        return  json.dumps({'code':400,'error': error})

@app.route('/assets/delete/')
def asset_delete():
    assets = models.get_asset_by_id(request.args.get('id',0))
    id=assets.get('id','')
    models.assets_delete(id)
    return json.dumps({'code':200})
    
@app.route('/monitor/host/create/',methods=['POST'])
def monitor_host_create():
    models.monitor_host_create(request.form)
    return json.dumps({'code': 200, 'result': ''})

@app.route('/monitor/host/list/')
def monitor_host_list():
    asset = models.get_asset_by_id(request.args.get('id',0))
    ip = asset.get('ip','')
    result = models.monitor_host_list(ip)
    return json.dumps({'code':200,'result':result})

#告警
@app.route('/alerts/')
def alerts():
    if session.get('user') is None: return redirect('/')
    return render_template('alerts.html')

@app.route('/alerts/list/')
def alert_list():
    alerts = models.get_alerts()
    return json.dumps({'data': alerts})

@app.route('/alerts/delete/')
def alert_delete():
    alerts = models.get_alert_by_id(request.args.get('id',0))
    uid=alerts.get('id','')
    print uid
    models.alerts_delete(uid)

    return json.dumps({'code':200})

