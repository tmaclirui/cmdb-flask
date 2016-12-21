#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
from flask import Flask
#创建Flask对象
app = Flask(__name__)
app.secret_key = '\xdcG\x9bD\xa4\x19p\x1b9\xb0\xd2\xa0yw\xdb\x8c'

import views
