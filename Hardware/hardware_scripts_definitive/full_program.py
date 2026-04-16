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
import _thread
import framebuf
from ssd1306 import SSD1306_I2C

NODE_ID = '1'
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



termometerData = bytearray([
# Stem
0b00001100, 0b00000000, # Row 1: ----##----------
0b00010010, 0b00000000, # Row 2: ---#--#---------
0b00010010, 0b00000000, # Row 3: ---#--#---------
0b00011110, 0b00000000, # Row 4: ---####---------
0b00011110, 0b00000000, # Row 5: ---####---------
0b00010010, 0b00000000, # Row 6: ---#--#---------
0b00010010, 0b00000000, # Row 7: ---#--#---------
0b00011110, 0b00000000, # Row 8: ---####---------
# Circle
0b00011110, 0b00000000, # Row 9: ---####---------
0b00010010, 0b00000000, # Row 10: ---#--#--------
0b00100001, 0b00000000, # Row 11: --#----#-------
0b01000000, 0b10000000, # Row 12: -#------#------
0b01000000, 0b10000000, # Row 13: -#------#------
0b01000000, 0b10000000, # Row 14: -#------#------
0b00100001, 0b00000000, # Row 15: --#----#-------
0b00011110, 0b00000000, # Row 16: ---####--------
])

heartData = bytearray([
    0b00001100, 0b00110000,  # Row 1: ....##....##....
    0b00011110, 0b01111000,  # Row 2: ...####..####...
    0b00111111, 0b11111100,  # Row 3: ..############..
    0b01111111, 0b11111110,  # Row 4: .##############.
    0b01111111, 0b11111110,  # Row 5: .##############.
    0b01111111, 0b11111110,  # Row 6: .##############.
    0b00111111, 0b11111100,  # Row 7: ..############..
    0b00011111, 0b11111000,  # Row 8: ...##########...
    0b00001111, 0b11110000,  # Row 9: ....########....
    0b00000111, 0b11100000,  # Row 10: .....######.....
    0b00000011, 0b11000000,  # Row 11: ......####......
    0b00000001, 0b10000000,  # Row 12: .......##.......
    0b00000000, 0b00000000,  # Row 13: ................
    0b00000000, 0b00000000,  # Row 14: ................
    0b00000000, 0b00000000,  # Row 15: ................
    0b00000000, 0b00000000   # Row 16: ................
    ])

circleData = bytearray([
 0b011110,  # Row 1: .####.
    0b111111,  # Row 2: ######
    0b110011,  # Row 3: ##..##
    0b110011,  # Row 4: ##..##
    0b111111,  # Row 5: ######
    0b011110   # Row 6: .####.
    ])

warning_sign = bytearray([
    0b00000111, 0b11000000,  # Row 1: ....##....##....
    0b00000111, 0b11000000,  # Row 2: ...####..####...
    0b00000111, 0b11000000,  # Row 3: ..############..
    0b00000111, 0b11000010,  # Row 4: .##############.
    0b00000111, 0b11000000,  # Row 5: .##############.
    0b00000111, 0b11000000,  # Row 6: .##############.
    0b00000111, 0b11000000,  # Row 7: ..############..
    0b00000111, 0b11000000,  # Row 8: ...##########...
    0b00000111, 0b11000000,  # Row 9: ....########....
    0b00000111, 0b11000000,  # Row 10: .....######.....
    0b00000000, 0b00000000,  # Row 11: ......####......
    0b00000000, 0b00000000,  # Row 12: .......##.......
    0b00000000, 0b00000000,  # Row 13: ................
    0b00000000, 0b00000000,  # Row 14: ................
    0b00000000, 0b00000000,  # Row 15: ................
    0b00000000, 0b00000000   # Row 16: ................

    ])

termometer = framebuf.FrameBuffer(termometerData, 16, 16, framebuf.MONO_HLSB)
heart = framebuf.FrameBuffer(heartData, 16, 16, framebuf.MONO_HLSB)
circle = framebuf.FrameBuffer(circleData, 8, 6, framebuf.MONO_HLSB)
warning = framebuf.FrameBuffer(warning_sign,16,16, framebuf.MONO_HLSB)


def clear_area(x, y, width, height):
    oled.fill_rect(x, y, width, height, 0)

def display_message(message):
    print(message)
    oled.blit(warning, 0,45)
    oled.blit(circle,2,57)
    oled.text(message,12, 50)
    oled.blit(warning,93,45)
    oled.blit(circle,95, 57)
    oled.show()




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
        nic.connect('MartiSmarti','martismarti110908')
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
        clear_area(0,45,130,90)
        display_message("REQ/EMG APR")
    if topic == PATIENT_VISITED_TOPIC:
        medical_staff_called = False
        staff_visited = True
        request_led.low()
        clear_area(0,45,130,90)
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
    oled.show()

def connectBroker():
    global mqtt_con
    mqtt_con = MQTTClient(NODE_ID,server='192.168.169.157', port=6000, user = 'node1' , password = 'node1_pass')
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
    clear_area(0,45,130,90)
    display_message("EMG SENT")
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
        clear_area(0,45,130,90)
        display_message("  REQ SENT")
        sleep(0.3)

async def wait_association():
    global is_associated
    clear_area(0,45,130,90)
    while not is_associated and  stop_await:
        print(f"In wait: stop_wait: {stop_await}")
        mqtt_con.check_msg()
        request_led.value(1)
        oled.text("Attatch to ", 20, 30)
        oled.text("patient ..." , 20, 45)
        oled.show()
        await asyncio.sleep(0.5)
        request_led.value(0)
        clear_area(0,45,130,90)
        oled.show()
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
    i2c = I2C(0, scl=Pin(9), sda=Pin(8))
    oled = SSD1306_I2C(128, 64, i2c)
    oled.fill(0)
    oled.show()
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

def display_temp(temp):
      oled.blit(termometer, 0, 24)
      oled.blit(circle, 47, 28)
      clear_area(20,28,20,20)
      oled.text (f"{temp}", 20, 28)
      oled.text('C',55,28)

def display_bpm(bpm):
     oled.blit(heart, 0, 0)
     clear_area(20,4,20,20)
     oled.text (f"{bpm} BPM", 20, 4)



def loop():
    global emrg, displayed, medical_staff_called, staff_visited, stop_await
    # stop_await = True
    mqtt_con.check_msg()
    mqtt_con.publish(TEMP_TOPIC, str(read_temp()).encode())
    mqtt_con.publish(BPM_TOPIC, str(read_bpm()).encode())
    display_bpm(read_bpm())
    display_temp(read_temp())
    sleep(0.1)
    #print(read_temp())
    #print(read_bpm())
    if read_temp() > 40 or read_temp() < 30:
        emergency_led.high()
        if staff_visited:
            call_emergency()
            staff_visited = False
        clear_area(0,45,130,90)
        display_message(" EMERGENCY")

            #medical_staff_called = True
    else:
        emergency_led.low()
        if not medical_staff_called:
            clear_area(0,45,130,90)
    oled.show()
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
            oled.fill(0)
            oled.show()
            print("Exit!")
            soft_reset()





