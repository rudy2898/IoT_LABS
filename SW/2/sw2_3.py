import requests
import time

if __name__ == "__main__":
    device1={
        "Devices": "ID01",
        "risorse": ["bene", "ciao"],
        "end_points": ["mqtt", "rest"]
        }
    while True:
        r = requests.put("http://localhost:8080/devices/devices", json = device1)
        time.sleep(60)
