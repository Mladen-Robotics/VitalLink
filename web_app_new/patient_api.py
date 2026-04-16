from flask import (Blueprint,render_template,
                request,jsonify)

from web_app_new.db_utilities import *
from .auth import login_required
import functools
from . import request_noticed,patient_visited
from flask_cors import cross_origin
import json

from .device_utils import get_all_devices


papi_bl = Blueprint('patient_retrieval', __name__, template_folder='templates/patient_retrieval', url_prefix='/')

MAX_PIN_COUNT = 3

@papi_bl.route('/create_patient')
@login_required
@cross_origin(origin='*', supports_credentials=True)
def create_patient_api():
    nodeID = request.args.get('nodeID')
    name = request.args.get('name')
    description = request.args.get('description')
    room_num = request.args.get('room_num')
    db = PatientDB()
    new_patient = db.add_patient(nodeID=nodeID,name=name,description=description,room_num = room_num)
    if new_patient is not None:
        return {'message':'patient created successfully'}
    else:
        return {'error': 'patient already exists'}

@papi_bl.route('/remove_patient/<int:id>')
@login_required
@cross_origin(origin='*', supports_credentials=True)
def remove_patient_api(id):
    db = PatientDB()
    remove_patient = db.remove_patient(id)
    if remove_patient is not None:
        return {'message':'patient removed successfully'}
    else:
        return {'error':'patient does not exist'}
    

@papi_bl.route('/patient/<int:id>/edit')
@login_required
@cross_origin(origin='*', supports_credentials=True)
def edit_patient_api(id):
    name = request.args.get('name')
    description = request.args.get('description')
    room_num = request.args.get('room_num')
    pinned = request.args.get(('pinned'))

    db = PatientDB()
    editted_patient = db.edit_patient(id, name=name, description=description,room_num=room_num,pinned=pinned)
    if editted_patient is not None:
        return {'message':'patient editted successfully'}
    else:
        return {'error' : 'patient can not be editted'}
    
@papi_bl.route('/patient/info')
@login_required
@cross_origin(origin='*', supports_credentials=True)
def get_patient_api():
    patientID = request.args.get('patientID')
    nodeID = request.args.get('nodeID')
    name = request.args.get('name')
    description = request.args.get('description')
    room_num = request.args.get('room_num')
    pinned = request.args.get('pinned')
    provide_all = request.args.get('all')
    db = PatientDB()
    patients = db.get_patient(patientID=patientID,nodeID=nodeID,name=name, description= description, room_num = room_num, pinned=pinned, provide_all=provide_all)

    # patient = db.get_patient(patientID=patientID, nodeID=nodeID, name=name,description=description,room_num=room_num, pinned=pinned)
    
    if patients is not None:
        res = []
        for i in patients:
            # print(i)
            res.append(i)
        print(jsonify(res))
        return jsonify(res)
    else:
        return {'error':'patient does not exist'}


@papi_bl.route('/patients/pin_count')
@login_required
@cross_origin(origin='*', supports_credentials=True)
def pin_count_api():
    db = PatientDB()
    count = db.pin_count()
    return jsonify({'count':count})

@papi_bl.route('patients/consts/max_pin_count')
@login_required
@cross_origin(origin='*', supports_credentials=True)
def max_count_constant():
    return str(MAX_PIN_COUNT)


@papi_bl.route('/patient/<int:id>/request_noticed')
@cross_origin(origin='*', supports_credentials=True)
def request_noticed_api(id):
    db = PatientDB()
    patient = db.get_patient(patientID=id)
    if patient is not None:
        patientID = patient[0]['PatientID']
        nodeID = db.get_nodeID_by_patientID(patientID=patientID)

        request_noticed(nodeID=nodeID)
        return {'message':'sent'}
    return {'error':'patient does not exist'}

@papi_bl.route('/patient/<int:id>/temp')
@login_required
@cross_origin(origin='*', supports_credentials=True)
def get_temp_api(id):
    db = PatientDB()
    measurments = db.get_latest_measurement_records(patientID=id,measurement='temp',n=30)

# Sort the data by the `time` field in ascending order
    

# Print the result
# print(json.dumps(result, indent=4))
    if measurments is not None:
        # return measurments
        sorted_data = sorted(measurments, key=lambda x: x["time"])

        # Convert the sorted list into a dictionary with keys starting from 0
        result = {index: entry for index, entry in enumerate(sorted_data)}
        return jsonify(result)
    else:
        return {'error':'patient does not exist'}


@papi_bl.route('/patient/<int:id>/bpm')
@login_required
@cross_origin(origin='*', supports_credentials=True)
def get_bpm_api(id):
    db = PatientDB()
    measurments = db.get_latest_measurement_records(patientID=id,measurement='bpm',n=30)
    if measurments is not None:
        sorted_data = sorted(measurments, key=lambda x: x["time"])

        # Convert the sorted list into a dictionary with keys starting from 0
        result = {index: entry for index, entry in enumerate(sorted_data)}
        return jsonify(result)
    else:
        return {'error':'patient does not exist'}

@papi_bl.route('/patient/<int:id>/visited')
@cross_origin(origin='*', supports_credentials=True)
def patient_visited_api(id):
    db = PatientDB()
    patient = db.get_patient(patientID=id)
    if patient is not None:
        patientID = patient[0]['PatientID']
        nodeID = db.get_nodeID_by_patientID(patientID=patientID)
        patient_visited(nodeID=nodeID)
        db.confirm_notification(patientID)
        # db.con(patient)
        # print(type(patient[0]['PatientID']))
        return {'message':'patient_visited'}
    else:
        return {'error':'patient does not exist'}

@papi_bl.route('/patient/<int:id>/notifications')
@login_required
@cross_origin(origin='*', supports_credentials=True)
def get_notifications(id):
    type = request.args.get("type")
    year = request.args.get("year")
    month = request.args.get("month")
    day = request.args.get("day")
    minute = request.args.get("minute")
    db = PatientDB()
    notifications = db.get_notifications(patientID=id,type=type, year=year, month=month, day=day, minute=minute)
    if notifications is not None:
        return notifications
    else:
        return {'error':'notification does not exist'}

# Device info
@papi_bl.route('/devices/info/presence')
@login_required
@cross_origin(origin='*', supports_credentials=True)
def get_present_device():
    present_devices = get_all_devices()
    print(present_devices)
    if len(present_devices) == 0:
        return {'devices':'none'}
    else:
        return {'devices':present_devices}
    

# @pretr_bl.route('patient/info')
# def info():
#     name = request.args.get('name')
#     room = request.args.get('room')
#     description = request.args.get('description')
#     pinned= request.args.get('pinned')
#     db = PatientDB()
#     patients = db.search_patients(name, description, room, pinned)
#     print(name)
#     print(room)
#     print(description)
#     print(pinned)
#     return jsonify(patients)

# @pretr_bl.route('patient/<int:id>/metrics')
# def metrics(id):
#     db = PatientDB()
#     measurment = request.args.get('mes')
#     if measurment == 'temp' or measurment == 'bpm':
#         return db.get_latest_measurement_records(id, measurment,2)
#     else:
#         return "{'error':'wrong measurment type'}"

# @pretr_bl.route('patient/<int:id>/calls')
# def calls(id):
#     db = PatientDB()
#     notes = db.search_notification(id)
#     return notes

# @pretr_bl.route('patient/<int:id>/notes')
# def notes(id):
#     db = PatientDB()
#     notes = db.search_note(id)
#     return notes

# Add method to return the number of pinned elements
