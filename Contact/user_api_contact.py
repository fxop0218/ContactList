import requests
from fastapi_sqlalchemy import db
from models import Contact as ContactModel

URL = "http://localhost:8000/"


def check_user(username: str, pwd: str):
    cu_url = URL + "check_user"
    headers = {"Content-Type": "application/json"}
    json_data = {"username": username, "password": pwd}

    resp = requests.get(cu_url, headers=headers, json=json_data)
    if resp.status_code != 200:
        return False
    rson = resp.json()
    print(rson)
    if rson["message"] == "True":
        return True
    return False


def get_user_inf(username: str):
    get_user_url = URL + "usr_info"
    headers = {"Content-Type": "application/json"}
    json_data = {"username": username}
    resp = requests.get(get_user_url, headers=headers, json=json_data)
    rson = resp.json()
    if rson["id"] == "False":
        return {"id": "False"}
    return {"id": rson["id"], "contacts": rson["contact_id"]}


# TODO solve error in this function
def add_contact_to_user(user_id: int, contact_id: int):
    msg = False
    print("jose")
    try:
        ac_user_url = URL + "add_contact"
        headers = {"Content-Type": "application/json"}
        json_data = {"user_id": user_id, "contact_id": contact_id}
        resp = requests.post(ac_user_url, headers=headers, json=json_data)
        rson = resp.json()
        print(rson)
        if rson["message"] == "True":
            msg = True
        return msg

    except Exception as e:
        print(f"Error: {e}")
        return False


def get_contact_info(c_name: str, telephone: int, owner: int):
    try:
        contact = (
            db.session.query(ContactModel)
            .filter_by(name=c_name)
            .filter_by(telephone=telephone)
            .filter_by(owner=owner)
            .first()
        )
        print(f"Contact: {contact.id}")
        return contact

    except Exception as e:
        print(f"get_contact_info error: {e}")
        return False


def delete_contact_to_user(user_list, contact_id: int):
    dctu_url = URL + "delete_contact"
    headers = {"Content-Type": "application/json"}
    count = 0

    try:
        if user_list.len() > 0:
            for u in user_list:
                json_data = {"id": u, "contact_id": contact_id}
                resp = requests.post(dctu_url, headers=headers, json=json_data)
                rson = resp.json()
                if rson["status"] == "True":
                    count = count + 1

            return count
    except Exception as e:
        print(f"get_contact_info Error: {e}")
