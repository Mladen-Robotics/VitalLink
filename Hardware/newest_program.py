# green led = 0 red led = 1
# OLED: SCL = 9 SDA = 8
# temp sensor = 27
# request button = 16 emergency button = 17

from machine import Pin, ADC, I2C
from utime import sleep
import network
from umqtt.robust import MQTTClient


NODE_ID = '1'
INFO_TOPIC = b"devices/info"
TEMP_TOPIC = b"node/" + NODE_ID + b"/tmp"
BPM_TOPIC =  b"node/" + NODE_ID + b"/bpm"
EMERGENCY_TOPIC = b"node/1/emg"
REQUEST_TOPIC = b"node/1/req"
# EMERGENCY_NOTICED_TOPIC = b"node/" + NODE_ID + b"/emergency_noticed"
REQUEST_NOTICED_TOPIC = b"node/" + NODE_ID + b"/request_noticed"
PATIENT_VISITED_TOPIC = b"node/" + NODE_ID + b"/patient_visited"

SUBSCRIBE_TOPICS = [REQUEST_NOTICED_TOPIC, PATIENT_VISITED_TOPIC]


temp_sensor_Pin = 26
#bpm_sensor_Pin = 28
emergency_btn_Pin = 17
request_btn_Pin = 16
emergency_led_Pin = 1
request_led_Pin = 0

stop_flag = False
emrg = True
req= False
displayed = False

medical_staff_called = False
staff_visited = True

nic = network.WLAN(network.STA_IF)
nic.active(True)

# Create and display bitmap
termometer = framebuf.FrameBuffer(termometerData, 16, 16, framebuf.MONO_HLSB)
heart = framebuf.FrameBuffer(heartData, 16, 16, framebuf.MONO_HLSB)
circle = framebuf.FrameBuffer(circleData, 8, 6, framebuf.MONO_HLSB)
warning = framebuf.FrameBuffer(warning_sign,16,16, framebuf.MONO_HLSB)



# def display_message(message):
#     print(message)
#     while not stop_flag:
#         oled.blit(warning, 0,45)
#         oled.blit(circle,2,57)
#         oled.text(message,12, 50)
#         oled.blit(warning,93,45)
#         oled.blit(circle,95, 57)
#         sleep(1)
#         clear_area(0,45,130,90)
#         sleep(1)


def connectWIFI():
    if not nic.isconnected():
        nic.connect('VIVACOM_FiberNet','e01e3e54')
        while not nic.isconnected():
            print("waiting  for connnection...")
            sleep(1)
    print('network config: ', nic.ifconfig())

def handle_messages(topic, msg):
    global medical_staff_called, staff_visited
    print("Received:")
    print(f"Topic: {str(topic)}")
    print(f"Message: {str(msg)}")
    if topic == REQUEST_NOTICED_TOPIC and medical_staff_called:
        medical_staff_called = True
        request_led.high()
    if topic == PATIENT_VISITED_TOPIC:
        medical_staff_called = False
        staff_visited = True
        request_led.low()


def connectBroker():
    global mqtt_con
    mqtt_con = MQTTClient(NODE_ID,server='192.168.1.6', port=6000, user = 'node1' , password = 'node1_pass')
    mqtt_con.set_last_will(INFO_TOPIC,"d_" + str(NODE_ID), retain=True, qos=1)
    mqtt_con.connect()
    print("Yay, it is connected")
    mqtt_con.set_callback(handle_messages)
    for topic in SUBSCRIBE_TOPICS:
        print(topic)
        mqtt_con.subscribe(topic,qos=1)
    mqtt_con.publish(INFO_TOPIC,b"c_" + str(NODE_ID))

def notify_disconnection():
    print("disconnection")
    mqtt_con.publish(INFO_TOPIC, "d_" + str(NODE_ID))

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

def setup():
    global temp, emergency_btn ,request_btn, emergency_led,request_led,i2c,oled
    temp = ADC(temp_sensor_Pin)
    # bpm = ADC(bpm_sensor_Pin)
    emergency_btn = Pin(emergency_btn_Pin, Pin.IN, Pin.PULL_UP)
    request_btn = Pin(request_btn_Pin, Pin.IN, Pin.PULL_UP)
    emergency_led = Pin(emergency_led_Pin, Pin. OUT)
    request_led = Pin(request_led_Pin, Pin. OUT)
    emergency_btn.irq(trigger = Pin.IRQ_FALLING, handler= emergency_btn_handle)
    request_btn.irq(trigger = Pin.IRQ_FALLING, handler= request_btn_handle)

    emergency_led.low()
    request_led.low()
    i2c = I2C(0, scl=Pin(21), sda=Pin(20))
    oled = SSD1306_I2C(128, 64, i2c)
    oled.fill(0)
    connectWIFI()
    connectBroker()

def read_temp():
    return int(temp.read_u16() * (50 / 65535))

def read_bpm():
    return 60
#     """Yield 60, then 0, then 60, … indefinitely."""
#     while True:
#         yield 60
#         yield 0


def loop():
    global emrg, displayed, medical_staff_called, staff_visited
    mqtt_con.check_msg()
    #print("Here")
    mqtt_con.publish(TEMP_TOPIC, str(read_temp()).encode())
    mqtt_con.publish(BPM_TOPIC, str(read_bpm()).encode())
    # if emrg==True and displayed == False:
      #      displayed = True
    #        _thread.start_new_thread(display_message, (" EMERGENCY",))
   # elif req==True and displayed == False:
     #       displayed = True
    #        _thread.start_new_thread(display_message, ("  REQUEST APR",))
    sleep(0.1)
    oled.show()
    #print(read_temp())
    #print(read_bpm())
    if read_temp() > 40 or read_temp() < 30:
        emergency_led.high()
        if staff_visited:
            call_emergency()
            staff_visited = False
            #medical_staff_called = True
        clear_area(0,45,130,90)
        display_message(" EMERGENCY")
    else:
        emergency_led.low()
        if not medical_staff_called:
            clear_area(0,45,130,90)
    sleep(1)

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except KeyboardInterrupt:
        emergency_led.low()
        request_led.low()
        notify_disconnection()
        mqtt_con.disconnect()
        stop_flag = True
        oled.fill(0)
        oled.show()
        print("Exit!")

