from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal 
from models import TaskDB
from schemas import TaskBase,TaskRead


#Base.metadata.create_all(bind=engine)

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


@app.get("/tasks",response_model=list[TaskRead])
def get_tasks(db:Session=Depends(get_db)):
    return db.query(TaskDB).all()

@app.post("/tasks", response_model=list[TaskRead])
def create_task(task: TaskBase, db: Session = Depends(get_db)):
    new_task = TaskDB(title=task.title, done=task.done)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task