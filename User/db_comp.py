from fastapi_sqlalchemy import db
from models import User as ModelUser
from helpful_functions import encript_pwd
async def check_user(user: str, password: str):
    try:
        user = db.session.query(ModelUser).filter_by(username=user).one()
        print(f"P1: {user.password}\nP2: {encript_pwd(password)}")
        if user.password == encript_pwd(password):
            return True
        return False
    except Exception as e:
        print(f"Error:  {e}")
        return False
