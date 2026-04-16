import os
from flask import Flask
from web_app_new.instance.conf import * 
import paho.mqtt.client  as mqtt
# from paho.mqtt.enums import CallbackAPIVersion 
import threading
import json
from .db_utilities import PatientDB
import re
from time import sleep
from datetime import datetime
from flask_cors import CORS
from .shared_state import present_devices, client, ALL_DEV_REQ_TOPIC, ALL_DEV_RES_TOPIC
# client = mqtt.Client(protocol=4)

db = PatientDB()
# unconfirmed_messages = []

# present_devices = list()


# PRESENCE_TOPIC = "devices/presence"
ALL_DEV_RES_TOPIC = "devices/info/all_dev_res"

CONNECT_DEVICE_TOPIC = "devices/info/con"
DISCONNECT_DEVICE_TOPIC = "devices/info/discon"

def store_temp(topic,messages):
    if 'tmp' in topic:
        node_id = int(re.search(r'\d', topic).group())
        print("NodeID: " + str(node_id))
        print(db.get_patient(nodeID=3))
        patientID = db.get_patient(nodeID=node_id)[0]['PatientID']
        # print(patientID)
        msg = int(json.loads(messages.payload.decode()))
        print('temp:',str(msg))
        db.add_temperature(patientID=patientID,temperature=float(msg))
        # print('Latest:',str(db.get_latest_measurement_records(patientID=patientID,measurement='temp',n=2)))

def store_bpm(topic,messages):
    if 'bpm' in topic:
        node_id = int(re.search(r'\d', topic).group())
        # print(node_id)
        patientID = db.get_patient(nodeID=node_id)[0]['PatientID']
        # print(patientID)
        msg = int(json.loads(messages.payload.decode()))
        print('bpm:',str(msg))
        db.add_bpm(patientID=patientID,bpm=msg)
        # print('Latest:',str(db.get_latest_measurement_records(patientID=patientID,measurement='bpm',n=1)))


def request_noticed(nodeID):
    topic = 'node/' + str(nodeID) + '/request_noticed'
    client.publish(topic,payload='{"msg":"noticed"')

def patient_visited(nodeID):
    topic = 'node/' + str(nodeID) + '/patient_visited'
    client.publish(topic,payload='{"msg":"visited"')


def handle_emergency(topic):
    # print(f"Topic: {topic}")
    if 'emg' in topic:
        print("EMERGENCYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYy")
        print("ADDING OTIFICATION")
        node_id = int(re.search(r'\d', topic).group())
        # print(node_id)
        patientID = db.get_patient(nodeID=node_id)[0]['PatientID']
        print(" adding notification")
        db.add_notification(patientID=patientID,n_type='emergency',confirmed=False)
        # all_notifications  = db.get_notifications(patientID=patientID)
        # latest_notification = max(
        #     all_notifications,
        #     key=lambda x: datetime.strptime(x['timestamp'], '%Y-%m-%d %H:%M:%S')
        # )
        # print(f"!!!!!!!! {latest_notification}  !!!!!!!")
        # unconfirmed_messages.append([node_id,latest_notification])
        # request_noticed(node_id)
        # patient_visited(node_id)
        # sleep(2)
        # client.publish(topic='node/2/request_noticed',payload="test")
        # sleep(2)
        # client.publish(topic="node/2/patient_visited",payload='test')


def handle_request(topic):
    if 'req' in topic:
        node_id = int(re.search(r'\d', topic).group())
        # print(node_id)
        patientID = db.get_patient(nodeID=node_id)[0]['PatientID']
        print("adding notification")
        db.add_notification(patientID=patientID,n_type='ordinary',confirmed=False)
        # request_noticed(node_id)
        # patient_visited(node_id)

def handle_present_devices_req(topic, messages):
    if ALL_DEV_RES_TOPIC == topic:
        msg = messages.payload.decode()
        


def on_message(client, userdata, messages):
    topic = messages.topic
    # print("New messaage")
    # print("---------------------------------")
    # print("Topic:", topic)
    # print("Payload:", json.loads(messages.payload.decode()))

    handle_present_devices_req(topic, messages)

    store_temp(topic,messages)
    store_bpm(topic, messages)

    handle_emergency(topic)
    handle_request(topic)

    if topic == ALL_DEV_RES_TOPIC:
        payload = messages.payload.decode()
        device_id = int(payload.strip())
        if device_id not in present_devices:
            present_devices.append(device_id)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #         print(f"Discovered device: {device_id}")
    # if topic == DISCONNECT_DEVICE_TOPIC:
    #     payload = messages.payload.decode()
    #     device_id = int(payload.strip())
    #     patient = get_patient(nodeID = device_id)
    #     print("Device with ID {device_id} was disconnected")
        

    # if topic == 'node/2/tmp':
    #     msg = int(json.loads(messages.payload.decode()))
    #     print("Temp:",str(msg))
    # if topic == 'node/2/bpm':
    #     msg = int(json.loads(messages.payload.decode()))
    #     print("Bpm:",str(msg))
    # print("---------------------------------")





# def handle_subscribe(client, userdata, mid, reason_code_list, properties):
#     print("THERE was a subscription")

# def handle_unsubscribe(client, userdata, mid, reason_code_list, properties):
#     print("THERE was an UNSUBSCRIBE")




def worker():
    # client.username = 'app'
    # client.password = 'app_pass'
    client.username_pw_set('app','app_pass')
    client.connect('192.168.169.157',6000)
    client.subscribe("devices/info")
    client.subscribe("devices/presence") # added new subscription
    client.subscribe("node/2/tmp")
    client.subscribe("node/2/bpm")
    client.subscribe("node/2/emg")
    client.subscribe("node/2/req")
    client.subscribe("node/1/tmp")
    client.subscribe("node/1/bpm")
    client.subscribe("node/1/emg")
    client.subscribe("node/1/req")
    client.subscribe("node/3/tmp")
    client.subscribe("node/3/bpm")
    client.subscribe("node/3/emg")
    client.subscribe("node/3/req")
    # client.subscribe("node/4/tmp")
    # client.subscribe("node/4/bpm")
    # client.subscribe("node/4/emg")
    # client.subscribe("node/4/req")
    client.subscribe("devices/info/con")
    client.subscribe("devices/info/discon")
    

    client.subscribe(ALL_DEV_RES_TOPIC)


    client.on_message=on_message
    # client.on_subscribe = handle_subscribe
    # client.on_unsubscribe = handle_unsubscribe
    client.loop_forever()

def create_app():
    app = Flask(__name__, instance_relative_config = True)
    app.config['DATABASE'] = os.path.join(app.instance_path, DATABASE_NAME)
    app.config['SECRET_KEY'] = "SECRET_KEY"
    from . import db_utilities
    db_utilities.init_app(app)

    from . import auth
    app.register_blueprint(auth.auth_bl)
    
    from . import dashboard
    app.register_blueprint(dashboard.dashboard_bl)

    from . import patient_api
    app.register_blueprint(patient_api.papi_bl)


    from . import note_api
    app.register_blueprint(note_api.napi_bl)

    # from . import patient_actions
    # app.register_blueprint(patient_actions.pact_bl)

    from . import patient_dashboard
    app.register_blueprint(patient_dashboard.pdashboard_bl)

    from . import user_api
    app.register_blueprint(user_api.uapi_bl)
    
    threading.Thread(target=worker, daemon=True).start()
    return app

