from fastapi import Request, Depends, HTTPException, status
from src.utils.settings import settings
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import  InvalidTokenError
from src.user.models import UserModel
from src.utils.db import get_db

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