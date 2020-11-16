from machine import UART
from umqtt.robust import MQTTClient
import uos
from time import sleep

MQTT_HOST = "192.168.1.8"
UART_ID = 0


def fetch_standard_data():
    device = UART(UART_ID, baudrate=300, bits=7,
                  parity=0, stop=2, timeout=3000)
    device.write('/#1'.encode('utf-8'))
    sleep(1)
    device.init(baudrate=1200, bits=7, parity=0, stop=1, timeout=3000)
    response = device.read(87)
    data = response.split()
    return {
        "energy":   int((data[0]).decode('utf-8')) / 100,
        "volume":   int((data[1]).decode('utf-8')) / 100,
        "temp_in":  int((data[2]).decode('utf-8')[7:]) / 100,
        "temp_out": int((data[3]).decode('utf-8')[0:7]) / 100
    }


def update():
    c = MQTTClient("umqtt_client", MQTT_HOST)
    c.connect()
    standard_data = fetch_standard_data()
    print("Publishing: {}".format(standard_data))

    c.publish("mc66c/energy",   str(standard_data["energy"]), True)
    c.publish("mc66c/volume",   str(standard_data["volume"]), True)
    c.publish("mc66c/temp_in",  str(standard_data["temp_in"]), True)
    c.publish("mc66c/temp_out", str(standard_data["temp_out"]), True)
