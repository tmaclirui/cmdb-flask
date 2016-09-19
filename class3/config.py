#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
port = 80
server_name = 'cmdb'
access_log = '/var/log/access.log'
root = '/home/wwwroot'
proxy_pass = 'http://127.0.0.1'

file_nginx = open('cmdb.tmp','r')
tp1 = file_nginx.read()
file_nginx.close()

cxt = tp1.format(PORT=port,\
                 SERVER_NAME=server_name,\
                 ACCESS_LOG=access_log,\
                 ROOT=root,\
                 PROXY_PASS=proxy_pass)
fh = open('nginx.conf','w')
fh.write(cxt)
fh.close()
