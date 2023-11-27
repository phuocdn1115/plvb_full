from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated, List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
import models
from starlette import status
from fastapi.middleware.cors import CORSMiddleware
import auth
from auth import get_current_user

myapp = FastAPI()
myapp.include_router(auth.router)

origins = [
    'http://localhost:3001'
]

myapp.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

class LabelBase(BaseModel):
    label: str
    desc: str

class LabelModel(LabelBase):
    id: int
    
    class Config:
        orm_mode = True
        
class UserBase(BaseModel):
    username: str
    password: str

class UserModel(UserBase):
    id: int
    
    class Config:
        orm_mode = True
        
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

models.Base.metadata.create_all(bind=engine)

@myapp.post("/label/", response_model= LabelModel)
async def create_label(label: LabelBase, db: db_dependency):
    db_label = models.Label(**label.model_dump())
    db.add(db_label)
    db.commit()
    db.refresh(db_label)
    return db_label

@myapp.get("/get_label/", response_model=List[LabelModel])
async def get_label(db: db_dependency):
    query = db.query(models.Label).offset(0).limit(100).all()
    return query

@myapp.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return {"user": user}