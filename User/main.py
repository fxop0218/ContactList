from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware, db
from helpful_functions import encript_pwd
from schema import User as SchemaUser
from fastapi import FastAPI, Request
from models import User as UserModel
from dotenv import load_dotenv
from db_comp import check_user
import pandas as pd
import json
import os

load_dotenv(".env")

USER_DB = "postgres"
PASS_DB = os.environ["USER"]
URL_DB = "localhost"
NAME_DB = os.environ["DB_NAME"]
FULL_URL_DB = f"postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}"  # Add this link to alembic.ini

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=FULL_URL_DB)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permisions
    allow_methods=["*"],  # Permisions
    allow_headers=["*"],
)

# FastAPI calls

# Test
@app.get("/")
async def index():
    return {"message": "True"}


# Create user
@app.post("/user")
async def create_user(user_: SchemaUser):
    try:
        db_user = UserModel(
            username=user_.username, password=encript_pwd(user_.password)
        )
        db.session.add(db_user)
        db.session.commit()
        return {"username": user_.username, "validation": "True"}
    except Exception as e:
        return {"username": user_.username, "validation": "False"}


# Login function
@app.get("/login")
async def login(user_: SchemaUser):
    try:
        user = db.session.query(UserModel).filter_by(username=user_.username).one()
        if encript_pwd(user_.password) == user.password:
            return {"message": "True"}
        return {"message": "False"}
    except Exception:
        return {"message": "False"}


# Show all the information of the user, ONLY ADMIN AND TESTING FUNCTION
@app.get("/all_users_admin")
async def all_users(request: Request):
    req_info = await request.json()
    password = encript_pwd(
        req_info["password"]
    )  # print(f"Password sended: {encript_pwd(password)} other password: {encript_pwd(os.environ['ADMIN_PWD'])}")
    if password == encript_pwd(os.environ["ADMIN_PWD"]):
        try:
            users = db.session.query(UserModel).all()
            data = {
                "UserId": [x.id for x in users],
                "username": [x.username for x in users],
                "passwords": [x.password for x in users],
            }
            df = pd.DataFrame(data=data)
            df.head()
            return df.to_csv()
        except Exception:
            return {"user": "admin"}
    else:
        return {"user": "admin"}


@app.post("/add_contact")
async def add_contact(request: Request):
    try:
        req_json = await request.json()
        user_id = req_json["user_id"]
        print(user_id)

        try:
            user = db.session.query(UserModel).filter_by(id=user_id).one()
            print(user.contact_id)
            if user.contact_id != None:
                if int(req_json["contact_id"]) in user.contact_id:
                    return {"message": "False", "Error2": "Duplicated field"}
                user.contact_id.append(req_json["contact_id"])
            else:
                user.contact_id = [req_json["contact_id"]]
            print(user.contact_id)
            db.session.add(user)
            db.session.commit()
            print("x")
            return {"message": "True"}
        except Exception as e:
            print(f"Error: {e}")
            return {"message": "False"}
    except Exception as e:
        print(f"add_contact api key error: {e}")
        return {"message": "False"}


@app.delete("/delete_contact")
async def delete_contact(request: Request):
    try:
        req_json = await request.json()
        user_id = req_json["id"]
        user = db.session.query(UserModel).filter_by(id=user_id).one()

        if req_json["contact_id"] in user.contact_id:
            return {
                "user": req_json["username"],
                "conctact": req_json["contact_id"],
                "status": "False",
            }

        user.contact_id.remove(int(req_json["contact_id"]))
        print(user.contact_id)

        db.session.add(user)
        db.session.commit()

        return {
            "user": req_json["username"],
            "conctact": req_json["contact_id"],
            "status": "True",
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "user": req_json["username"],
            "conctact": req_json["contact_id"],
            "status": "False",
        }


@app.get("/check_user")
async def check(request: Request):
    msg = "False"
    try:
        req_json = await request.json()
        if await check_user(req_json["username"], req_json["password"]):
            msg = "True"
        return {"message": msg}
    except Exception as e:
        print(f"Error {e}")
        return {"message": "False"}


@app.get("/user_info")
async def check(request: Request):
    try:
        req_json = await request.json()
        user = (
            db.session.query(UserModel).filter_by(username=req_json["username"]).one()
        )
        return user

    except Exception as e:
        print(f"Error: {e}")
        return {"id": "False"}

    # req_info = await request.json()
    # password = encript_pwd(req_info["password"])
