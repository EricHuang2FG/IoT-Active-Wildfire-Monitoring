# MCU for arm

import os
import wifi
import socketpool
import json
import adafruit_requests as requests


SSID, PASSWORD = os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD")
BASE_URL = "http://172.20.10.5:8000"


# run the code on the CIRCUITPY thonny to get the MCU to connect to the hotspot


def main() -> None:
    wifi.radio.connect(SSID, PASSWORD)
    print("Connected:", wifi.radio.ipv4_address)

    pool = socketpool.SocketPool(wifi.radio)
    http = requests.Session(pool)

    data = {"testing": 0}

    response = http.post(f"{BASE_URL}/receive", json=data)

    print(response.json())


if __name__ == "__main__":
    main()
