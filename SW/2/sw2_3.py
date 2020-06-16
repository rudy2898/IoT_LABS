import requests
import time

if __name__ == "__main__":
    device1={
        "Dispositici": "Dispositivo1", 
        "risorse": "tante", 
        "end_points":[0, 1, 2]
        }
    while True:
        requests.post("http://localhost:8080/devices", data = device1)
        time.sleep(60)