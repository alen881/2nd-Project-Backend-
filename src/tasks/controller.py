
from sqlalchemy.orm import Session
from src.tasks.dtos import TaskSchema
from src.tasks.models import TaskModel
from fastapi import HTTPException
from src.user.models import UserModel



def create_task(body: TaskSchema, db: Session, user: UserModel):
    new_task = TaskModel(
        title=body.title,  
        description=body.description,
        is_completed=body.is_completed,
        deadline=body.deadline,
        user_id=user.id
    )
    db.add(new_task)
    db.commit()

    ## Refresh the instance to get the updated values (like auto-generated ID)
    db.refresh(new_task)

    return new_task
    
def get_tasks(db: Session, user: UserModel):
    tasks = db.query(TaskModel).filter(TaskModel.user_id == user.id).all()
    return tasks

def get_task_by_id(task_id: int, db: Session, user: UserModel):
    task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

def update_task(task_id: int, body: TaskSchema, db: Session, user: UserModel):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user.id:
        raise HTTPException(status_code=401, detail="You are not authorized to update this task")

# Update the task attributes with the new values from the request body
    for key, value in body.model_dump().items():
        setattr(task, key, value)
    

    db.commit()
    db.refresh(task)

    return task

def delete_task(task_id: int, db: Session, user: UserModel):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user.id:
            raise HTTPException(status_code=401, detail="You are not authorized to delete this task")

    db.delete(task)
    db.commit() 

    return None