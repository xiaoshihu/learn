# -*- coding: utf-8 -*-

"""
    @author: xiaoshihu
    @file: __init__.py.py
    @time: 2019/7/23 18:03
    @desc: 
"""
import os
from flask import Flask

def create_app(test_config=None):
    # the frist parm is packgname and second not know.
    app = Flask(__name__,instance_relative_config=True)