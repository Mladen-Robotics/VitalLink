from flask import (Blueprint,render_template,
                request,jsonify, session)

from web_app_new.db_utilities import *
import functools
from .auth import login_required
from  datetime import datetime
from flask_cors import cross_origin
uapi_bl = Blueprint('user_actions', __name__, template_folder='templates/user_api', url_prefix='/')

@uapi_bl.route('/create_user')
@login_required
@cross_origin(origin='*', supports_credentials=True)
def create_user_api():
    name = request.args.get('name')
    speciality = request.args.get('speciality')
    username = request.args.get('username')
    password = request.args.get('password')
    
    db = PatientDB()
    name_exists = db.get_user(name=name)
    username_exists = db.get_user(username=username)
    password_exists = db.get_user(password=password)
    if name_exists is None and username_exists is None and password_exists is None:
        user = db.create_user(name=name,speciality=speciality,username=username,password=password)
        return {'message':'successfully created'}

    else:
        return {'error':'user already exists'}
    
@uapi_bl.route('/user/<int:id>/remove')
@login_required
@cross_origin(origin='*', supports_credentials=True)
def remove_user_api(id):
    db = PatientDB()
    user = db.get_user(userID = id)
    if user is not None:
        db.remove_user(id)
        session.clear()
        return {'message':'User is removed'}
    else:
        return {'error':'User does not exist'}

@uapi_bl.route('/user/<int:id>')
@login_required
@cross_origin(origin='*', supports_credentials=True)
def get_user_api(id):
    db = PatientDB()
    user = db.get_user(userID=id)
    if user is not None:
        return user
    else:
        return {'error':'User does not exist'}
    
@uapi_bl.route('/get_current_user')
@login_required
@cross_origin(origin='*', supports_credentials=True)
def get_current_user_api():
    user_id = session['user_id']
    return jsonify({'user_id' : user_id})