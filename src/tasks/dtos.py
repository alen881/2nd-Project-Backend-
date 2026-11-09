from pydantic import BaseModel
import datetime
class TaskSchema(BaseModel):
    id: int
    title: str
    description: str
    is_completed: bool = False
    deadline: datetime.datetime = None

class TaskResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    is_completed: bool
    deadline: datetime.datetime 
    user_id : int | None

    