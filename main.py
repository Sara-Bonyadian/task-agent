from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def read_root():
    return{"message":"uvicornTask Agent Backend is runing"}

@app.get("/tasks")
def get_tasks():
    return[
        {"id":1,"title":"Buy groceries","done":False},
        {"id":2,"title":"Finish homework","done":True},
        {"id":3,"title":"Call mom","done":False},
        ]