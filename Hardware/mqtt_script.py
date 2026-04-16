import network
from utime import sleep
from umqtt.robust import MQTTClient
from machine import ADC, Pin

NODE_ID = '1'
INFO_TOPIC = b"devices/info"
TEMP_TOPIC = b"node/1/tmp"
BPM_TOPIC = b"node/1/bpm"
EMERGENCY_TOPIC = b"node/1/emg"
REQUEST_TOPIC = b"node/1/req"
# EMERGENCY_NOTICED_TOPIC = b"node/" + NODE_ID + b"/emergency_noticed"
REQUEST_NOTICED_TOPIC = b"node/" + NODE_ID + b"/request_noticed"
PATIENT_VISITED_TOPIC = b"node/" + NODE_ID + b"/patient_visited"
SUBSCRIBE_TOPICS = [REQUEST_NOTICED_TOPIC, PATIENT_VISITED_TOPIC]


TEMP_SENSOR_PIN = 28
EMERGENCY_LED_PIN = 0
BPM_SESNOR_PIN = 26
EMERGENCY_BTN_PIN = 2
REQUEST_BTN_PIN = 1
STAFF_CALLED_LED_PIN = 3



nic = network.WLAN(network.STA_IF)
nic.active(True)

tmp = ADC(TEMP_SENSOR_PIN)
emergency_led = Pin(EMERGENCY_LED_PIN, Pin.OUT)
bpm = ADC(BPM_SESNOR_PIN)
emergency_btn = Pin(EMERGENCY_BTN_PIN, Pin.IN, Pin.PULL_UP)
request_btn = Pin(REQUEST_BTN_PIN, Pin.IN, Pin.PULL_UP)
staff_called_led = Pin(STAFF_CALLED_LED_PIN, Pin.OUT)

medical_staff_called = False

def connectWIFI():
    if not nic.isconnected():
        nic.connect('VIVACOM_FiberNet','e01e3e54')
        while not nic.isconnected():
            print("waiting  for connnection...")
            sleep(1)
    print('network config: ', nic.ifconfig())

def handle_messages(topic, msg):
    print("Received:")
    print(f"Topic: {str(topic)}")
    print(f"Message: {str(msg)}")
    if topic == REQUEST_NOTICED_TOPIC:
        medical_staff_called = True
        staff_called_led.high()
    if topic == PATIENT_VISITED_TOPIC:
        medical_staff_called = False
        staff_called_led.low()
        
        
    

def connectBroker():
    global mqtt_con
    mqtt_con = MQTTClient(NODE_ID,server='192.168.1.6', port=6000, user = 'node2' , password = 'node2_pass')
    mqtt_con.set_last_will(INFO_TOPIC,"d_" + str(NODE_ID), retain=True, qos=1)
    mqtt_con.connect()
    mqtt_con.set_callback(handle_messages)
    for topic in SUBSCRIBE_TOPICS:
        print(topic)
        mqtt_con.subscribe(topic,qos=1)
    mqtt_con.publish(INFO_TOPIC,b"c_" + str(NODE_ID))
    
def notify_disconnection():
    mqtt_con.publish(INFO_TOPIC, "d_" + str(NODE_ID))

def tmp_read():
    #print("Here: ", str(round(tmp.read_u16() * (50 / 65535), 2)))
    return str(round(tmp.read_u16() * (50 / 65535), 2))

def bpm_read():
    #print("Bpm: ", bpm.read_u16() * (50 / 65535))
    return str(round(bpm.read_u16() * (50 / 65535), 2))

def emergency_handler(pin):
    print("EMERGENCY")
    mqtt_con.publish(EMERGENCY_TOPIC, b'emergency')
    
def request_handler(pin):
    print("REQUEST")
    mqtt_con.publish(REQUEST_TOPIC, b'request')
    
if __name__ == "__main__":
    try:
        connectWIFI()
        connectBroker()
        emergency_btn.irq(handler=emergency_handler, trigger=Pin.IRQ_FALLING)
        request_btn.irq(handler=request_handler, trigger=Pin.IRQ_FALLING)
        staff_called_led.low()
        while True:
            mqtt_con.check_msg()
            mqtt_con.publish(TEMP_TOPIC, tmp_read().encode())
            mqtt_con.publish(BPM_TOPIC, bpm_read().encode())
            #print("tmp")
            #print(type(tmp_read()))
            if float(tmp_read()) > 39.0:
                emergency_led.high()
            else:
                emergency_led.low()
            sleep(0.1)
    except KeyboardInterrupt:
        notify_disconnection()
        mqtt_con.disconnect()
        print("Exited successfully!")


