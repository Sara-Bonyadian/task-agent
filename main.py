from fastapi import FastAPI, Depends
from fastapi import HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from database import get_db,init_db
from models import TaskDB
from schemas import TaskBase,TaskRead



@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
# Allow your frontend (Vue dev server) to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite (Vue 3 default)
        "http://127.0.0.1:5173",
        "http://localhost:3000"   # if you ever use React
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return{"status":"ok"}

@app.get("/")
def read_root():
    return {"message": "FastAPI with PostgreSQL is running"}


@app.get("/tasks",response_model=list[TaskRead])
def get_tasks(db:Session=Depends(get_db)):
    return db.query(TaskDB).all()

@app.post("/tasks", response_model=TaskRead)
def create_task(task: TaskBase, db: Session = Depends(get_db)):
    new_task = TaskDB(title=task.title, done=task.done)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get("/tasks/{task_id}",response_model=TaskRead)
def get_task(task_id:int,db:Session=Depends(get_db)):
    task=db.get(TaskDB,task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task not found")
    return task

@app.put("/tasks/{task_id}",response_model=TaskRead)
def update_task(task_id:int,data:TaskBase,db:Session=Depends(get_db)):
    task=db.get(TaskDB,task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task not found")
    task.title=data.title
    task.done=data.done
    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id:int,db:Session=Depends(get_db)):
    task=db.get(TaskDB,task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task not found")
    db.delete(task)
    db.commit()
    return  Response(status_code=status.HTTP_204_NO_CONTENT)