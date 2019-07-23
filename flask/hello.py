# -*- coding: utf-8 -*-

"""
    @author: xiaoshihu
    @file: hello.py.py
    @time: 2019/7/23 14:10
    @desc: 
"""
from flask import Flask,escape,url_for,abort,redirect
from flask import request
app = Flask(__name__)

# @app.route('/')
# def hello():
#     return '<h1>Hello Flask!</h1>'

@app.route('/<name>')
def greet(name):
    return f'<h1>Hello {escape(name)}</h1>'

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

# @app.route('/login')
# def login():
#     return 'login'

@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(escape(username))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    abort(404)
    return 'login'

# 这里会自动加载之后，自动去请求这几个链接，并且是可以传递参数进去的
# 而且是在每一次加载之后就进行，所以可以比较方便的进行测试，而且这个 url_for 函数可以比较好的解决绝对路径和相对
# 路径的问题
with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    # 多余的参数会当作查询参数
    print(url_for('login', next='/'))
    # 也可以直接传递参数给视图函数
    print(url_for('profile', username='John Doe'))