from flask import (Blueprint,render_template,
                request, redirect, url_for,
                flash, session,
                g)

from web_app_new.db_utilities import *
import functools
from flask_cors import cross_origin

auth_bl = Blueprint('auth', __name__, template_folder='templates/auth', url_prefix='/')


def is_logged(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # Ако няма user_id в сесията, отива на /login
        if session.get('user_id') is not None:
            print("There is a cookie!")
            # return redirect(url_for('dashboard.main_dashboard'))
            return redirect('http://localhost:8000/')
        return view(**kwargs)
    return wrapped_view

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # Ако няма user_id в сесията, отива на /login
        if session.get('user_id') is None:
            print("THERE ISNT ANY COOKIE!")
            return redirect(url_for('dashboard.about'))
        return view(**kwargs)
    return wrapped_view


@auth_bl.route('login', methods=['GET', 'POST'])
@is_logged
@cross_origin(origin='*', supports_credentials=True)
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        db = PatientDB()
        user = db.get_user(username=username, password=password)
        print("Login:")
        print("Username:",username)
        print("password:",password)
        print("User:", user)
        if user != None:
            print("Successfully Logged in")
            session.clear()
            print("UserID:", user[0][0])
            session['user_id'] = list(user)[0][0]
            # return redirect(url_for('dashboard.main_dashboard'))
            return redirect('http://localhost:8000/')
        flash('Неправилно потребителско име или парола!', 'error')
    return render_template('login.html')

@auth_bl.route('signup', methods=['GET', 'POST'])
@is_logged
@cross_origin(origin='*', supports_credentials=True)
def signup():
    if request.method == "POST":
        name = request.form['name'].strip()
        speciality = request.form['speciality'].strip()
        username = request.form['username'].strip()
        password = request.form['password']
        print("sign up:")
        print("name:",name)
        print("seciality:",speciality)
        print("username: ",username)
        print("password: ", password)
        db = PatientDB()
        username_exists = db.get_user(username=username)
        password_exists = db.get_user(password=password)
        name_exits = db.get_user(name=name)
        print('username exists:', username_exists)
        print('password_exists:', password_exists)
        print('name exists:',name_exits)
        if username_exists is None and password_exists is None and name_exits is None:
            print("User is unique")
            user = db.create_user(name, speciality, username, password)
            session['user_id'] = user
            flash(f'Потребител {name} беше създаден успешно!', 'successfully_created')
            # return redirect(url_for('dashboard.main_dashboard'))
            return redirect('http://localhost:8000/')
        else:
            print("error message is flashed!")
            flash('Парола или потребителско име вече съществуват!')
        # # print(db.test)
        # print(dir(db))
        # # user = db.test()
        
        # user = db.create_user(name, speciality, username, password)
        # print(user)
        # if user != []:
        #     # user_id = db.add_user(name, speciality, username, password)
        #     session['user_id'] = user
        #     flash(f'Потребител {name} беше създаден успешно!', 'successfully_created')
        #     return redirect(url_for('dashboard.main_dashboard'))
    
    return render_template('signup.html')

@auth_bl.route('/logout')
@cross_origin(origin='*', supports_credentials=True)
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bl.route('/user/<int:id>')
@cross_origin(origin='*', supports_credentials=True)
def get_user(id):
    db = PatientDB()
    user = db.get_user(userID=id)
    if user is not None:
        return user
    else:
        return {'error':'user does not exist'}