from fastapi import FastAPI, Request
from fastapi_sqlalchemy import DBSessionMiddleware, db
from fastapi.middleware.cors import CORSMiddleware
from schema import User as SchemaContact
from fastapi import FastAPI, Request
from models import Contact as ModelContract
from dotenv import load_dotenv
from helpful_functions import encript_pwd
from user_api_contact import (
    check_user,
    get_user_inf,
    add_contact_to_user,
    get_contact_info,
)
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


# FastAPI

# test


@app.get("/")
async def index():
    return {"message": "Test"}


@app.post("/create")
async def crate(contact: SchemaContact):
    try:
        db_contract = ModelContract(
            name=contact.name,
            email=contact.email,
            telephone=contact.telephone,
            owner=contact.owner,
        )
        db.session.add(db_contract)
        db.session.commit()
        created_contact = get_contact_info(
            c_name=contact.name, telephone=contact.telephone, owner=contact.owner
        )
        if add_contact_to_user(contact_id=created_contact.id, user_id=contact.owner):
            return {
                "owner": contact.owner,
                "contact_name": contact.name,
                "message": "True",
            }
        return {"message": "False"}
    except Exception as e:
        print(f"Exception : {e}")
        return {"message": "False"}


# username
# contact_id
@app.post("/add_user")
async def add_user(request: Request):
    msg = "False"
    try:
        req_json = await request.json()
        user_info = get_user_inf(req_json["username"])
        if req_json["contact"] not in user_info["contact_id"]:
            contact = (
                db.session.query(ModelContract).filter_by(id=req_json["contact"]).one()
            )
            contact.shaerd.append(user_info["id"])
            db.session.add(contact)
            db.session.commit()
            msg = "True"
        return {"message": msg}
    except Exception as e:
        print(f"Error: {e}")
        return {"message": msg}


@app.delete("/delete")
async def delete(request: Request):
    msg = "False"
    try:
        req_json = await request.json()
        owner = req_json["owner"]
        contact_id = req_json["contact_id"]
        password = encript_pwd(req_json["password"])
        if check_user(contact_id, password):
            contract = db.session.query(ModelContract).filter_by(id=contact_id).one()
            # TODO delete contact to all users with this contact
            if contract.owner == owner:
                msg = "True"
        return {"message": msg}

    except Exception as e:
        print(f"Error: {e}")
        return {"message": "False"}
