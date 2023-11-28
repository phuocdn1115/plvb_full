from datetime import timedelta, datetime
from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status
from sqlalchemy.orm import Session
from database import SessionLocal
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from models import User
import json

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = "vdc2023vdi2024re9e0rwer9ew0rwe9rwe0"
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(username: str, password: str, db: db_dependency):
    user = db.query(User).filter(User.username == username).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username is existed")
    create_user_model = User(
        username=username,
        password=bcrypt_context.hash(password)
    )
    db.add(create_user_model)
    db.commit()
@router.post("/token")
async def login_for_access_token( db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    username = form_data.username
    password = form_data.password
    user = authenticate_user(username, password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Email or password is wrong')
    return {"id":user.id, 'username': user.username,'password': user.password}
    
    
def authenticate_user(username: str, password: str, db: Session): 
    user = db.query(User).filter(User.username == username).first()
    print(user.password)
    print(type(user))
    if not user:
        return False
    if not user.password == password:
        return False
    return user