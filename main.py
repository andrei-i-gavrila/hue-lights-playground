import json
import random
import threading
import time
from os import path

threading.Thread()

import urllib3

ip = "http://192.168.0.145"
http = urllib3.PoolManager()
username_filename = 'username.txt'


def make_request(route, json_body=None, method="GET"):
    complete_route = f"{ip}/{route}"
    if json_body is not None:
        encoded_data = json.dumps(json_body).encode('utf-8')
        request = http.request(method,
                               complete_route,
                               body=encoded_data,
                               headers={'Content-Type': 'application/json'})
    else:
        request = http.request(method, complete_route)

    response = request.data.decode('utf-8')
    print(response)
    return json.loads(response)


def get_username():
    if path.exists(username_filename):
        with open(username_filename, 'r') as f:
            return f.read()
    else:
        username = make_request("api", {'devicetype': 'andrei'}, "POST")['success']['username'][0]
        with open(username_filename, 'w') as f:
            f.write(username)
        return username


username = get_username()

lights = make_request(f"api/{username}/lights")

while True:
    # threads = []
    # for light_id, light in lights.items():
    #     threads.append(threading.Thread(args=(light_id,), target=lambda args: make_request(f"api/{username}/lights/{args[0]}/state", {'on': False, 'transitiontime': 0}, "PUT")))
    # for thread in threads:
    #     thread.start()'
    threads = []
    for light_id, light in lights.items():
        threads.append(
            threading.Thread(args=(light_id, random.randint(1, 65534)),
                             target=lambda lid, col: make_request(f"api/{username}/lights/{lid}/state", {'on': True, 'hue': col, 'sat': 254, 'bri': 254, 'transitiontime': 2}, "PUT")))
    for thread in threads:
        thread.start()
    time.sleep(0.4)
