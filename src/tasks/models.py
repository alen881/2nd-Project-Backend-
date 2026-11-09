from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from src.utils.db import Base

class TaskModel(Base):
    __tablename__ = "user_tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    is_completed = Column(Boolean, default=False)
    deadline = Column(DateTime, nullable=True)
    ## entire row of table user_tasks containing user_id will be deleted if the user is deleted
    user_id=Column(Integer,ForeignKey("user_table.id", ondelete="CASCADE")) 