from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware, db
from dotenv import load_dotenv
import os

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
    db_user = UserModel(username=user_.username, password=user_.password)
    db.session.add(db_user)
    db.session.commit()
    return db_user
