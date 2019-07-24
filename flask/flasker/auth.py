# -*- coding: utf-8 -*-

"""
    @author: xiaoshihu
    @file: auth.py
    @time: 2019/7/24 11:19
    @desc: 
"""
import functools
from flask import Blueprint,flash,g,redirect,render_template,request,session,url_for
from werkzeug.security import check_password_hash,generate_password_hash
from .db import get_db

# it is convenient but amazing like magic.
bp = Blueprint('auth',__name__,url_prefix='/auth')

# use blueprint can decouple code structure because when i want change things i can only attention to one file
# only pay attention to one blueprint is convenint
@bp.route('/register',methods=('GET','POST'))
def register():
    # check post form
    if request.method == 'POST':
        # get data from form posted by user
        username = request.form['username']
        password = request.form['password']
        # connect db
        # when close the connect?
        # i always think it will get wrong?because
        db = get_db()
        error = None
        # check input data
        if not username:
            error = 'username is required'
        elif not password:
            error = 'password is required'
        elif db.execute('select id from user where username = ?',(username,)).fetchone() is not None:
            error = '{} is already register'.format(username)

        if error is None:
            # insert data into database
            # deal password can protect user's privacy
            db.execute('insert into user (username,password) values (?,?)',(username,generate_password_hash(password)))
            db.commit()
            # redirect to login url
            return redirect(url_for('auth.login'))
        # show error
        flash(error)
    # where the register.html?blew the folder named auth?
    return render_template('auth/register.html')

@bp.route('/login',methods=('GET','POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        user = db.execute('select * from user where username = ?', (username,)).fetchone()
        if user is None:
            error = 'Incorrect username.'
        # check hash value
        elif not check_password_hash(user['password'],password):
            error = 'Incorrect password.'

        if error is None:
            # store cookie in session
            # should notice the lifecycle of session,not only attention on one request
            session.clear()
            session['user_id'] = user['id']
            # the param mean?url point ?function?i think is url point
            return redirect(url_for('index'))
        flash(error)

    return render_template('auth/login.html')

# be called before every request,
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        # the data has keep in session,it is necessary for keep it in global var?
        # i know the reason keep the user information in g var,so can use in every templates?
        g.user = get_db().execute('select * from user where id = ?',(user_id,)).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

# do a lot of things to keep user's information and it will useful when user get information page.
# deal this things in auth module and then won't think this,decouple!!

# so when you analysis a doc,should think clear the param is send to which function?
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # i can check session,not g
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view