

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, Request
from src.user.dtos import UserSchema, LoginSchema
from src.utils.db import get_db
from src.user.models import UserModel
from pwdlib import PasswordHash
import jwt
from src.utils.settings import settings
from datetime import datetime, timedelta
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

## Pass Hasher
password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

##Pass verifier
def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

## Registration

def register(body: UserSchema, db: Session = Depends(get_db)):

    ##Username validation
    is_user=db.query(UserModel).filter(UserModel.username == body.username).first()
    if is_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    ##Email validation

    is_email=db.query(UserModel).filter(UserModel.email == body.email).first()
    if is_email:
        raise HTTPException(status_code=400, detail="Email already exists")


    hash_password = get_password_hash(body.password)

    new_user = UserModel(
        name=body.name,
        username=body.username,
        email=body.email,
        hash_password=hash_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(body: LoginSchema, db: Session = Depends(get_db)):

    
    user=db.query(UserModel).filter(UserModel.username == body.username).first()
    
    ##validating user
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    ##validating password
    if not verify_password(body.password, user.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

    
    exp_time = datetime.now() + timedelta(minutes=settings.exp_time)

    token= jwt.encode({"user_id": user.id, "username": user.username, "exp":exp_time.timestamp()}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return {"access_token": token}


def is_authenticated(request: Request,db: Session = Depends(get_db)):
   
   try:
    token = request.headers.get("authorization")
    if not token :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are Unauthorized")

    token = token.split(" ")[-1]
    ## Timeout error already handled by jwt library, so no need to handle it here
    data = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM) 
    id=data.get("user_id")
    
    


    user=db.query(UserModel).filter(UserModel.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are Unauthorized")

    
    return user

   except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are Unauthorized")