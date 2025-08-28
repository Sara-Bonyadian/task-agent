from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()
tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Finish homework", "done": True},
]

class Task(BaseModel):
    title:str
    done:bool=False

@app.get("/")
def read_root():
    return{"message":"uvicornTask Agent Backend is runing"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def create_task(task:Task):
    new_task={"id":len(tasks)+1,"title": task.title, "done":task.done}
    tasks.append(new_task)
    return new_task