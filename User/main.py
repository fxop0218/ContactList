from fastapi import FastAPI, Request 
from fastapi_sqlalchemy import DBSessionMiddleware, db
from helpful_functions import encript_pwd
from schema import User as SchemaUser
from fastapi import FastAPI, Request 
from models import User as UserModel
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv(".env")

USER_DB = "postgres"
PASS_DB = os.environ["USER"]
URL_DB = "localhost"
NAME_DB = os.environ["DB_NAME"]
FULL_URL_DB = f"postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}" # Add this link to alembic.ini

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=FULL_URL_DB)

# FastAPI calls

# Test
@app.get("/")
async def index():
    return {"message": "True"}


# Create user
@app.post("/user")
async def create_user(user_: SchemaUser):
    try:
        db_user = UserModel(username=user_.username, password=encript_pwd(user_.password))
        db.session.add(db_user)
        db.session.commit()
        return ({"username": user_.username, 
                "validation": "True"})
    except Exception as e:
        return ({"username": user_.username, 
                "validation": "False"})    
    

# Login function
@app.get("/login")
async def login(user_: SchemaUser):
    try:
        user = db.session.query(UserModel).filter_by(username=user_.username).one()
        if encript_pwd(user_.password) == user.password:
            return ({"message": "True"})
        return ({"message": "False"})
    except Exception:
        return ({"message": "False"})

# Show all the information of the user, ONLY ADMIN AND TESTING FUNCTION
@app.get("/all_users_admin")
async def all_users(request: Request):
    req_info = await request.json()
    password = encript_pwd(req_info["password"])    # print(f"Password sended: {encript_pwd(password)} other password: {encript_pwd(os.environ['ADMIN_PWD'])}")
    if password == encript_pwd(os.environ["ADMIN_PWD"]):
        try:
            users = db.session.query(UserModel).all()
            data = {"UserId": [x.id for x in users], "username": [x.username for x in users], "passwords": [x.password for x in users]}
            df = pd.DataFrame(data=data)
            df.head()
            return df.to_csv()
        except Exception:
            return {"user": "admin"}
    else: 
        return {"user": "admin"}
        
    #req_info = await request.json()
    #password = encript_pwd(req_info["password"])