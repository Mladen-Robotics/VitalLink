import paho.mqtt.client as mqtt

# Create shared state variables
present_devices = list()

# Create MQTT client
client = mqtt.Client(protocol=4)

# MQTT Topics
ALL_DEV_REQ_TOPIC = "devices/info/all_dev_req"
ALL_DEV_RES_TOPIC = "devices/info/all_dev_res"
ASSOCIATE_DEVICE_TOPIC = "devices/info/associate"
DISCONNECT_DEVICE_TOPIC = "devices/info/disconnect"
WAIT_TIME = 4