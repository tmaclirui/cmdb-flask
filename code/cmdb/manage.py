#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
from cmdb import app

if __name__ == '__main__':
    #启动
    print app.url_map
    app.run(host='0.0.0.0',debug=True)
