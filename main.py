from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def read_root():
    return{"message":"uvicornTask Agent Backend is runing"}
