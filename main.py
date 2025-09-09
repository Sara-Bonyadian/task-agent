from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
s
class TaskDB(Base):
    __tablename__ = "tasks"   # matches the table we created in Postgres

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    done = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)

class Task(BaseModel):
    title: str
    done: bool = False

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
#@app.get("/")
#def read_root():
#    return{"message":"uvicornTask Agent Backend is runing"}

#@app.get("/tasks")
#def get_tasks():
#    return tasks

#@app.post("/tasks")
#def create_task(task:Task):
#    new_task={"id":len(tasks)+1,"title": task.title, "done":task.done}
#    tasks.append(new_task)
#   return new_task

@app.get("/")
def read_root():
    return {"message": "FastAPI with PostgreSQL is running"}

@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(TaskDB).all()

@app.post("/tasks")
def create_task(task: Task, db: Session = Depends(get_db)):
    new_task = TaskDB(title=task.title, done=task.done)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task