from fastapi import FastAPI, Request 
from fastapi_sqlalchemy import DBSessionMiddleware, db
from schema import User as SchemaContact
from fastapi import FastAPI, Request 
from models import Contact as ModelContract
from dotenv import load_dotenv
from helpful_functions import encript_pwd
import os

load_dotenv(".env")

USER_DB = "postgres"
PASS_DB = os.environ["USER"]
URL_DB = "localhost"
NAME_DB = os.environ["DB_NAME"]
FULL_URL_DB = f"postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}" # Add this link to alembic.ini

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=FULL_URL_DB)


# FastAPI

#test

@app.get("/")
async def index():
    return {"message":"Test"}

@app.post("/create")
async def crate(contact: SchemaContact):
    try:
        db_contract = ModelContract(name=contact.name, email=contact.email,
              telephone=contact.telephone, owner=contact.owner)
        db.session.add(db_contract)
        db.session.commit()
        return {"owner":contact.owner, "contact_name": contact.name, "message": "True"}
    except:
        return {"message": "False"}
    
@app.delete("/delete")
async def delete(request: Request):
    try:
        req_json = await request.json()
        owner = req_json["owner"]
        contact_id = req_json["contact_id"]
        contract =  db.session.query(ModelContract).filter_by(id=contact_id).one()
        if contract.owner == owner:
            return {"message": "True"}
        else:
            return {"message":"False"}


    except Exception as e:
        print(f"Error: {e}")
        return {"message": "False"}
