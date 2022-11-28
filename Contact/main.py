from fastapi import FastAPI, Request 
from fastapi_sqlalchemy import DBSessionMiddleware, db
from schema import User as SchemaUser
from fastapi import FastAPI, Request 
from models import Contact as UserContract
from dotenv import load_dotenv
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