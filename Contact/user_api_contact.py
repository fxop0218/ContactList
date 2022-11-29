import requests
import json

URL = "http://localhost:8000/"

def check_user(username: str, pwd: str):
    cu_url = URL + "check_user"
    headers = {"Content-Type" : "application/json"}
    json_data = {"username": username, "password": pwd}

    resp = requests.get(cu_url, headers=headers, json=json_data)
    rson = resp.json()
    print(rson)
    if (rson["message"] == "True"): 
        return True
    return False
    