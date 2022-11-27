from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware, db
from dotenv import load_dotenv
import os
import uvicorn
from helpful_functions import encript_pwd
from schema import User as SchemaUser
from models import User as UserModel

load_dotenv(".env")

USER_DB = "postgres"
PASS_DB = os.environ["USER"]
URL_DB = "localhost"
NAME_DB = os.environ["DB_NAME"]
FULL_URL_DB = f"postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}" # Add this link to alembic.ini

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=FULL_URL_DB)

# FastAPI calls

@app.get("/")
async def index():
    return {"message": "True"}

@app.post("/user/", response_model=SchemaUser)
async def create_user(user_: SchemaUser):
    try:
        db_user = UserModel(username=user_.username, password=encript_pwd(user_.password))
        db.session.add(db_user)
        db.session.commit()
        return db_user
    except Exception as e:
        return ({"message": "Username also exists"})
    
@app.post("/login")
async def login(user_: SchemaUser):
    print(f"{user_.password}")
    try:
        user = db.session.query(UserModel).filter_by(username=user_.username).one()
        if encript_pwd(user_.password) == user.password:
            return ({"message": "True"})
        return ({"message": "False"})
    except Exception:
        return ({"message": "False"})
    
