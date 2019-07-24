# -*- coding: utf-8 -*-

"""
    @author: xiaoshihu
    @file: __init__.py.py
    @time: 2019/7/23 18:03
    @desc: 
"""
import os
from flask import Flask

# so this function is factory function,and it will return app,but where and when call this function?
# this function will be called by flask,and create app auto
# and will create instance dir auto,app.instance mean the dir named instance?
# but when you dev,tha app instance not exists,how to add view to it?
def create_app(test_config=None):
    # the frist pamrm is package name and second not know.
    app = Flask(__name__,instance_relative_config=True)
    # conf app,other module will use it
    # DATABASE link also in config
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path,'flaskr.sqlite')
    )
    # also update config
    if test_config is None:
        # update config data from a python file,and if the file is not exits will nor raise error
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)

    # why this path maybe not exists
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass

    # print(app.instance_path)

    # exe this,and the view function will bing to app
    # @app.route('/')
    # def hello():
    #     return 'hello,world!'

    # init function nor call,app is special.
    from . import db
    db.init_app(app)

    # register blueprint to app.amazing!!
    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    # so i can use url_for('index') equal url_for('blog.index')
    app.add_url_rule('/', endpoint='index')

    return app