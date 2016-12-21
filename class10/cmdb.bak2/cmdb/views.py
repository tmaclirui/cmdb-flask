#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
from flask import render_template
from flask import request
from flask import redirect
from flask import session
import json
from cmdb import app
import models

@app.route('/users/save/',methods=['post'])
def users_save():
    if session.get('user') is None: return redirect('/')
    username = request.form.get('username','')
    password = request.form.get('password','')
    age = request.form.get('age',0)
    department = request.form.get('department','')
    sex = request.form.get('sex','')
    birthday = request.form.get('birthday')
    email = request.form.get('email')
    hobby = request.form.getlist('hobby')
    hobby = ' '.join(hobby)
    ok,error = models.validate_user_save(username,password,age)
    if ok:

        models.add_users(username, password,age,department,sex,birthday,email,hobby)
        return  json.dumps({'code':200})
    else:
        return  json.dumps({'code':400,'error': error})


@app.route('/users/view/')
def users_view():
    if session.get('user') is None: return redirect('/')
    user = models.get_user_by_id(request.args.get('id',0))
    return render_template('user_view.html',id=user.get('id',''),\
     username=user.get('name',''),age=user.get('age',0),\
     department=user.get('department'),sex=user.get('sex'),\
     birthday=user.get('birthday'),email=user.get('email'),\
     hobby=user.get('hobby'))


@app.route('/users/delete/')
def users_delete():
    user = models.get_user_by_id(request.args.get('id',0))
    id=user.get('id','')
    models.user_delete(id)
    return redirect('/users/')


@app.route('/users/modify/',methods=['POST'])
def users_modify():
    if session.get('user') is None: return redirect('/')
    uid = request.form.get('id','')
    username = request.form.get('username','')
    age = request.form.get('age','')
    department = request.form.get('department','')
    sex = request.form.get('sex','')
    birthday = request.form.get('birthday')
    email = request.form.get('email')
    hobby = request.form.getlist('hobby')
    hobby = ' '.join(hobby)
    ok,error = models.validate_user_modify(uid,username,age)
    if ok:
        models.user_modify(uid,username,age,department,sex,birthday,email,hobby)
        return redirect('/users/')
    else:
        return render_template('user_view.html',id=uid,username=username,age=age,error=error)


@app.route('/users/create/')
def users_create():
    if session.get('user') is None: return redirect('/')
    return render_template('user_create.html')


@app.route('/users/')
def users():
    if session.get('user') is None: return redirect('/')
    return render_template('users.html',users=models.get_users())

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
    user = models.validate_login(username,password)
    if user:
        session['user'] = user
        return redirect('/users/')
    else:
        return render_template('index.html',username=username,password=password,error="username or password is error")            

@app.route('/log/')
def log():
    if session.get('user') is None: return redirect('/')
    topn= request.args.get('topn',10)
    topn= int(topn) if str(topn).isdigit() else 10
    log_file = '/opt/nginx/logs/access.log'
    result=models.nginxlog(log_file,topn)
    return  render_template('log.html',logs=result)

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/')
@app.route('/test/')
def test():
    return render_template('test.html')

# 机房管理
@app.route('/machine/')
def machine():
    return render_template('machine.html',machines=models.get_machines())

@app.route('/machine/create/')
def machine_create():
    return render_template('machine_create.html')

@app.route('/machine/save/',methods=['post'])
def machine_save():
    name = request.form.get('name','')
    addr = request.form.get('addr','')
    ip_ranges= request.form.get('ip_ranges','')
    ok,error = models.validate_machine_save(name,addr,ip_ranges)
    if ok:
        models.add_machines(name, addr,ip_ranges)
        return  json.dumps({'code':200})
    else:
        return  json.dumps({'code':400,'error': error})
        
@app.route('/machine/view/')
def machine_view():
    machines = models.get_machine_by_id(request.args.get('id',0))

    return render_template('machine_view.html',id=machines.get('id',''), name=machines.get('name',''),addr=machines.get('addr',''),ip_ranges=machines.get('ip_ranges',''))


@app.route('/machine/modify/',methods=['POST'])
def machine_modify():
    uid = request.form.get('id','')
    name = request.form.get('name','')
    addr = request.form.get('addr','')
    ip_ranges = request.form.get('ip_ranges','')
    ok,error = models.validate_machine_modify(uid,name,addr,ip_ranges)
    if ok:
        models.machine_modify(uid,name,addr,ip_ranges)
        return redirect('/machine/')
    else:
        return render_template('machine_view.html',id=uid,name=name,addr=addr,ip_ranges=ip_ranges,error=error)

@app.route('/machine/delete/')
def machine_delete():
    machines = models.get_machine_by_id(request.args.get('id',0))
    id=machines.get('id','')
    models.machine_delete(id)
    return redirect('/machine/')

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