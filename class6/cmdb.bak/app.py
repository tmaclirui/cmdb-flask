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
   
if __name__ == '__main__':
    #启动
    print app.url_map
    app.run(host='0.0.0.0',debug=True)
