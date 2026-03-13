# MCU for sensor box

# Notes for myself
# MCU is client-side, sends HTTPS request to server over local network
# MCU POST to server and get data/instructions from server and other pico

import os # access environmental variables stored on board in settings.toml file
import wifi
import socketpool
import ssl
import json # encode/decode json data
import adafruit_requests as requests
import time


SSID, PASSWORD = os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD")
BASE_URL = "https://active-fire-monitoring-esc204.onrender.com"


def main() -> None:
    wifi.radio.connect(SSID, PASSWORD)
    print("Connected:", wifi.radio.ipv4_address)

    # reads pem file and stores it as string in cert_data variable
    with open("/render.pem", "r") as f:
        cert_data = f.read()

    # creates network session
    pool = socketpool.SocketPool(wifi.radio)
    ssl_context = ssl.create_default_context()
    ssl_context.load_verify_locations(cadata=cert_data)
    http = requests.Session(pool, ssl_context)

    last_time = time.time()

    while True:
        current_time = time.time()
        if current_time > last_time + 5:
            last_time = time.time()
            post_server(http)
            post_mcu_arm(http)
            get_server(http)
            get_mcu_arm(http)
    

def post_server(http) -> None:
    data = {
            "temperature": 0,
            "humidity": 0,
            "battery": 0,
        }
    sensor_readings = {
                        "to": "server",
                        "data": data,
                    }
    
    response = http.post(f"{BASE_URL}/receive", json=sensor_readings)
    response_dictionary = response.json()
    print(response_dictionary["status_code"])
    print(response_dictionary["message"])

    response.close()

def post_mcu_arm(http) -> None:
    data = {
            "temperature": 0,
            "humidity": 0,
            "battery": 0,
        }
    sensor_readings = {
                        "to": "mcu_arm",
                        "data": data,
                    }
    
    response = http.post(f"{BASE_URL}/receive", json=sensor_readings)
    response_dictionary = response.json()
    print(response_dictionary["status_code"])
    print(response_dictionary["message"])

    response.close()

def get_server(http) -> None:
    response = http.get(f"{BASE_URL}/get_server_data")
    response_dictionary = response.json()
    print(response_dictionary["status_code"])
    print(response_dictionary["message"])
    print(response_dictionary["data"])

    response.close()

def get_mcu_arm(http) -> None:
    target_dictionary = {
                            "target": "mcu_arm",
                    }
    response = http.post(f"{BASE_URL}/get_mcu_data", json=target_dictionary)
    response_dictionary = response.json()
    print(response_dictionary["status_code"])
    print(response_dictionary["message"])
    print(response_dictionary["data"])

    response.close()

if __name__ == "__main__":
    main()
