from machine import UART
from umqtt.robust import MQTTClient
import uos
from time import sleep

MQTT_HOST = "192.168.1.8"
UART_ID = 0


def fetch_standard_data():
    device = UART(UART_ID, baudrate=300, bits=7,
                  parity=0, stop=2, timeout=3000)
    device.write("/#1".encode("utf-8"))
    sleep(1)

    # Kamstrup Multical 66C docs specify stopbits = 2, however on ESP8266 this results into gibberish
    device.init(baudrate=1200, bits=7, parity=0, stop=1, timeout=3000)
    response = device.read(87)

    # whitespaces are discarded in some readings
    # nevertheless, ASCII numbers are always complete,
    # so we split it manually
    data = response.decode("utf-8").replace(" ", "")
    parts = [data[i:i+7] for i in range(0, len(data), 7)]
    return {
        "energy":   int(parts[0]) / 100,
        "volume":   int(parts[1]) / 100,
        "temp_in":  int(parts[3]) / 100,
        "temp_out": int(parts[4]) / 100
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
