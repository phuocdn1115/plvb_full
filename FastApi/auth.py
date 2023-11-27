from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status
from sqlalchemy.orm import Session
from database import SessionLocal
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from models import User

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
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    user = db.query(User).filter(User.username == create_user_request.username).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username is existed")
    create_user_model = User(
        username=create_user_request.username,
        password=bcrypt_context.hash(create_user_request.password)
    )
    db.add(create_user_model)
    db.commit()
    
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Email or password is wrong')
    
    token = create_user_token(user.username, user.id, timedelta(minutes=60))
    return {'access_token': token, 'token_type': 'bearer'}
    
    
def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    print(type(user))
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user

def create_user_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
        

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload =  jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        id: str = payload.get('id')
        
        if username is None or id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not have validate user')
        return {'username': username, 'id': id}
        
    except JWTError:
        pass