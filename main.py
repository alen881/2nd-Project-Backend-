from fastapi import FastAPI
from src.utils.db import  engine, Base
from src.tasks.router import task_routes
from src.user.router import user_routes


##When you modify your SQLAlchemy models later—such as adding a new column, changing a data type, or deleting a field—create_all will ignore the existing tables and will not update your database to reflect those changes.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management App")
app.include_router(task_routes)
app.include_router(user_routes)




