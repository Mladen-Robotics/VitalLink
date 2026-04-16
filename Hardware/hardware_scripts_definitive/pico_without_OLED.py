# green led = 0 red led = 1
# OLED: SCL = 9 SDA = 8
# temp sensor = 27
# request button = 16 emergency button = 17

from machine import Pin, ADC, I2C, soft_reset
from utime import sleep
import network
from umqtt.robust import MQTTClient
import uasyncio as asyncio
import json
import gc


NODE_ID = '3'
INFO_TOPIC = b"devices/info"
CONNECT_BROKER_TOPIC = b"devices/info/con"
DISCONNECT_BROKER_TOPIC = b"devices/info/discon"

TEMP_TOPIC = b"node/" + NODE_ID + b"/tmp"
BPM_TOPIC =  b"node/" + NODE_ID + b"/bpm"
EMERGENCY_TOPIC = b"node/" + NODE_ID +"/emg"
REQUEST_TOPIC = b"node/" + NODE_ID + "/req"
# EMERGENCY_NOTICED_TOPIC = b"node/" + NODE_ID + b"/emergency_noticed"
REQUEST_NOTICED_TOPIC = b"node/" + NODE_ID + b"/request_noticed"
PATIENT_VISITED_TOPIC = b"node/" + NODE_ID + b"/patient_visited"

ASSOCIATE_TOPIC = b"devices/info/associate"
DISCONNECT_TOPIC = b"devices/info/disconnect"

IDENTIFY_REQUEST_TOPIC = b"devices/info/all_dev_req"
IDENTIFY_RESPONSE_TOPIC = b"devices/info/all_dev_res"

SUBSCRIBE_TOPICS = [REQUEST_NOTICED_TOPIC, PATIENT_VISITED_TOPIC,ASSOCIATE_TOPIC, DISCONNECT_TOPIC, IDENTIFY_REQUEST_TOPIC]




temp_sensor_Pin = 26
#bpm_sensor_Pin = 28
emergency_btn_Pin = 17
request_btn_Pin = 16
emergency_led_Pin = 1
request_led_Pin = 0

emrg = True
req= False
displayed = False

medical_staff_called = False
staff_visited = True

is_associated = False
stop_await = True

nic = network.WLAN(network.STA_IF)
nic.active(True)

def connectWIFI():
    if not nic.isconnected():
        nic.connect('Velizar','velizarpass')
        while not nic.isconnected():
            print("waiting  for connnection...")
            sleep(1)
    print('network config: ', nic.ifconfig())

def handle_messages(topic, msg):
    global medical_staff_called, staff_visited, is_associated, stop_await
    print("Received:")
    print(f"Topic: {str(topic)}")
    print(f"msg: {msg.decode('utf-8')}")
    message = json.loads(msg.decode('utf-8'))['msg']
    #message = msg
    print(f"Message: {message}")
    if topic == REQUEST_NOTICED_TOPIC and medical_staff_called:
        medical_staff_called = True
        request_led.high()
    if topic == PATIENT_VISITED_TOPIC:
        medical_staff_called = False
        staff_visited = True
        request_led.low()
    if topic == ASSOCIATE_TOPIC and stop_await:
        print("HERE")
        if message == NODE_ID:
            print("Yes, it is associated")
            is_associated = True
            stop_await = False
    if topic == DISCONNECT_TOPIC and not stop_await:
        if message == NODE_ID:
            is_associated = False
            stop_await = True
    if topic == IDENTIFY_REQUEST_TOPIC and stop_await:
        print(f"NodeID = {NODE_ID}")
        mqtt_con.publish(IDENTIFY_RESPONSE_TOPIC, NODE_ID)

def connectBroker():
    global mqtt_con
    mqtt_con = MQTTClient(NODE_ID,server='192.168.51.157', port=6000, user = 'node3' , password = 'node3_pass')
    mqtt_con.set_last_will(INFO_TOPIC,"d_" + str(NODE_ID), retain=False, qos=1)
    mqtt_con.connect(clean_session=True)
    print("Yay, it is connected")
    mqtt_con.set_callback(handle_messages)
    for topic in SUBSCRIBE_TOPICS:
        print(topic)
        mqtt_con.subscribe(topic,qos=1)
    mqtt_con.publish(CONNECT_BROKER_TOPIC,f'{{"msg": {str(NODE_ID)}}}')

def notify_disconnection():
    print("disconnection")
    mqtt_con.publish(DISCONNECT_BROKER_TOPIC, f'{{"msg": {str(NODE_ID)}}}')

def call_emergency():
    #print(f"Pin: {pin}")
    global medical_staff_called
    print("There was a EMERGENCY!")
    medical_staff_called = True
    mqtt_con.publish(EMERGENCY_TOPIC, b'emergency')
    sleep(0.3)

def emergency_btn_handle(pin):
    global medical_staff_called
    if not medical_staff_called:
        call_emergency()
        #emergency_led.high()
def request_btn_handle(pin):
    global medical_staff_called
    print("REQUEST:", medical_staff_called)
    if not medical_staff_called:
        print(f"Pin: {pin}")
        print("There was a REQUEST")
        medical_staff_called = True
        mqtt_con.publish(REQUEST_TOPIC, b'request')
        sleep(0.3)

async def wait_association():
    global is_associated

    while not is_associated and  stop_await:
        print(f"In wait: stop_wait: {stop_await}")
        mqtt_con.check_msg()
        request_led.value(1)
        await asyncio.sleep(0.5)
        request_led.value(0)
        await asyncio.sleep(0.5)
    request_led.value(0)
    print("Stopped await")
    return None


async def setup():
    global temp, emergency_btn ,request_btn, emergency_led,request_led,i2c,oled

    request_led = Pin(request_led_Pin, Pin. OUT)


    temp = ADC(temp_sensor_Pin)
    # bpm = ADC(bpm_sensor_Pin)
    emergency_btn = Pin(emergency_btn_Pin, Pin.IN, Pin.PULL_UP)
    request_btn = Pin(request_btn_Pin, Pin.IN, Pin.PULL_UP)
    emergency_led = Pin(emergency_led_Pin, Pin. OUT)


    emergency_led.low()
    request_led.low()
    connectWIFI()
    connectBroker()
    print(f"In setup: is_associated = {is_associated}")
    await wait_association()

    emergency_btn.irq(trigger = Pin.IRQ_FALLING, handler= emergency_btn_handle)
    request_btn.irq(trigger = Pin.IRQ_FALLING, handler= request_btn_handle)
    #gc.collect()
    print("Exiting the setup")
    return None

def read_temp():
    print("Temp: ", int(temp.read_u16() * (50 / 65535)))
    return int(temp.read_u16() * (50 / 65535))

def read_bpm():
    return 60



def loop():
    global emrg, displayed, medical_staff_called, staff_visited, stop_await
    # stop_await = True
    mqtt_con.check_msg()
    mqtt_con.publish(TEMP_TOPIC, str(read_temp()).encode())
    mqtt_con.publish(BPM_TOPIC, str(read_bpm()).encode())
    sleep(0.1)
    #print(read_temp())
    #print(read_bpm())
    if read_temp() > 40 or read_temp() < 30:
        emergency_led.high()
        if staff_visited:
            call_emergency()
            staff_visited = False
            #medical_staff_called = True
    else:
        emergency_led.low()
    sleep(1)

if __name__ == "__main__":
    while True:
        try:
            #stop_await = True
            sleep(1)
            asyncio.run(setup())
            print(f"is_associated: {is_associated}")
            while is_associated:
                loop()
        except KeyboardInterrupt:
            # print("HAAAAAAAA")
            emergency_led.low()
            request_led.low()
            notify_disconnection()
            mqtt_con.disconnect()
            stop_await = True
            print("Exit!")
            soft_reset()




