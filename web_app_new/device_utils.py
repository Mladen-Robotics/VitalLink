# import asyncio
from .shared_state import present_devices, client,  ALL_DEV_REQ_TOPIC, ALL_DEV_RES_TOPIC, WAIT_TIME, ASSOCIATE_DEVICE_TOPIC, DISCONNECT_DEVICE_TOPIC
from time import sleep

# ALL_DEV_REQ_TOPIC = "devices/info/all_dev_req"
# ALL_DEV_RES_TOPIC = "devices/info/all_dev_res"

# ASSOCIATE_DEVICE_TOPIC = "devices/info/associate"
# WAIT_TIME = 4


# def handle_subscribe(client, userdata, mid, reason_code_list, properties):
#     print("THERE was a subscription")

# def handle_unsubscribe(client, userdata, mid, reason_code_list, properties):
#     print("THERE was an UNSUBSCRIBE")

# Set the callbacks on the client
# client.on_subscribe = handle_subscribe
# client.on_unsubscribe = handle_unsubscribe




def get_all_devices():
    present_devices.clear()
    print("I am here all healty!!!")
    print(f"The client is {client}")
    client.publish(ALL_DEV_REQ_TOPIC, '{"msg":"get_all"}')
    sleep(WAIT_TIME)
    # await asyncio.sleep(WAIT_TIME)
    return present_devices.copy()

def associate_device(nodeID):
    print(f"I am now associating device number {nodeID}")
    print(f"I use client: {client}")
    mesg = f'{{"msg":\"{nodeID}\"}}'
    print(f"This is the message: {mesg}")
    client.publish(ASSOCIATE_DEVICE_TOPIC, mesg)
    client.subscribe(f"node/{nodeID}/tmp")
    client.subscribe(f"node/{nodeID}/bpm")
    client.subscribe(f"node/{nodeID}/emg")
    client.subscribe(f"node/{nodeID}/req")
    print(" I subscibed!!! ")

def disconnect_device(nodeID):
    print(f"I am now DISCONNECTING device number {nodeID}")
    print(f"I use client: {client}")
    mesg = f'{{"msg":\"{nodeID}\"}}'
    print(f"This is the message: {mesg}")
    client.publish(DISCONNECT_DEVICE_TOPIC, mesg)
    client.unsubscribe(f"node/{nodeID}/tmp")
    client.unsubscribe(f"node/{nodeID}/bpm")
    client.unsubscribe(f"node/{nodeID}/emg")
    client.unsubscribe(f"node/{nodeID}/req")