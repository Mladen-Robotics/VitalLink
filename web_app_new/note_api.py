from flask import (Blueprint,render_template,
                request,jsonify)

from web_app_new.db_utilities import *
from .auth import login_required

import functools
from flask_cors import cross_origin

napi_bl = Blueprint('note_api', __name__, template_folder='templates/note_api', url_prefix='/')

@napi_bl.route('/patient/<int:id>/add_note')
@login_required
@cross_origin(origin='*', supports_credentials=True)
def  add_note_api(id):
    description = request.args.get('description')

    db = PatientDB()
    note = db.add_note(id,description)
    if note is not None:
        return {'message':'note successfully added'}
    else:
        return {'error' : 'patient does not exist'}

@napi_bl.route('/note/<int:id>/remove')
@login_required
@cross_origin(origin='*', supports_credentials=True)
def remove_note_api(id):
    db = PatientDB()
    note = db.remove_note(id)
    if note is  not None:
        return {'message':'note removed successfully'}
    else:
        return {'error' : 'notification does not exist'}

@napi_bl.route('/note/<int:id>/edit')
@login_required
@cross_origin(origin='*', supports_credentials=True)
def edit_note_api(id):
    description = request.args.get('description')
    db = PatientDB()
    note = db.edit_note(id, description)
    if note is not None:
        return {'message':'note editted successfully'}
    else:
        return jsonify("{'error':'note does not exist'}")

@napi_bl.route('/patient/<int:id>/notes')
@login_required
@cross_origin(origin='*', supports_credentials=True)
def get_notes_api(id):
    db = PatientDB()
    notes = db.get_notes(patientID=id)
    if notes is not None:
        return jsonify(notes)
    else:
        return {'error':'patient does not exist'}