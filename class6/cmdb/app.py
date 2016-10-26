#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

import models


#创建Flask对象
app = Flask(__name__)

@app.route('/users/save/',methods=['post'])
def users_save():
    username = request.form.get('username','')
    password = request.form.get('password','')
    age = request.form.get('age',0)
    ok,error = models.validate_user_save(username,password,age)
    if ok:
        models.add_users(username, password,age)
        return  redirect('/users/')
    else:
        return render_template('user_create.html',username=username,age=age,error=error)

@app.route('/users/view/')
def users_view():
    user = models.get_user_by_id(request.args.get('id',0))

    return render_template('user_view.html',id=user.get('id',''), username=user.get('name',''),age=user.get('age',0))

@app.route('/users/delete/')
def users_delete():
    user = models.get_user_by_id(request.args.get('id',0))
    id=user.get('id','')
    models.user_delete(id)
    return redirect('/users/')

@app.route('/users/modify/',methods=['POST'])
def users_modify():
    uid = request.form.get('id','')
    username = request.form.get('username','')
    age = request.form.get('age','')
    ok,error = models.validate_user_modify(uid,username,age)
    if ok:
        models.user_modify(uid,username,age)
        return redirect('/users/')
    else:
        return render_template('user_view.html',id=uid,username=username,age=age,error=error)

@app.route('/users/create/')
def users_create():
    return render_template('user_create.html')

@app.route('/users/')
def users():
    return render_template('users.html',users=models.get_users())

@app.route('/')
def index():
    return  render_template('index.html')

@app.route('/login/',methods=['post','get'])
def login():
    username = ''
    password = ''
    params = request.form if 'POST' == request.method  else request.args
    username = params.get('username','')
    password = params.get('password','')
    user = models.validate_login(username,password)
    if user:
        return redirect('/users/')
    else:
        return render_template('index.html',username=username,password=password,error="username or password is error")            

@app.route('/log/')
def log():
    topn= request.args.get('topn',10)
    topn= int(topn) if str(topn).isdigit() else 10
    log_file = '/opt/nginx/logs/access.log'
    result=models.nginxlog(log_file,topn)
    return  render_template('log.html',logs=result)


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
        return  redirect('/machine/')
    else:
        return render_template('machine_create.html',name=name,addr=addr,error=error)

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

if __name__ == '__main__':
    #启动
    print app.url_map
    app.run(host='0.0.0.0',debug=True)
