from sqlalchemy import Column, Integer, String, Boolean, DateTime
from src.utils.db import Base

class UserModel(Base):
    __tablename__ = "user_table"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255))
    hash_password = Column(String(255), nullable=False)
    