from fastapi import FastAPI, Depends
from fastapi import HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from contextlib import asynccontextmanager
from database import get_db,init_db
from models import TaskDB
from schemas import TaskBase,TaskRead, TaskUpdate
from typing import Optional



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
def get_tasks(
    db:Session=Depends(get_db),
    done: Optional[bool]=Query(None,description="Filter by done status"),
    search: Optional[str]=Query(None, description="Case-insensitive search in title"),
    sort: str=Query("id", description="Sort by one of: id, title,done"),
    order:str=Query("asc", description="asc or desc"),
    limit: Optional[int]=Query(None,ge=1,le=100,description="Max rows"),
    offset:int=Query(0,ge=0,description="Skip first N rows")
):
    q=db.query(TaskDB)

    #filters
    if done is not None:
        q=q.filter(TaskDB.done==done)

    if search is not None:
        term = search.strip().lower()
        if term:
            # case-insensitive match: lower(title) LIKE lower(term)
            q = q.filter(func.lower(TaskDB.title).like(f"%{term.lower()}%"))

    sort_map={
        "id":TaskDB.id,
        "title":TaskDB.title,
        "done":TaskDB.done
    }
    col=sort_map.get(sort,TaskDB.id)

    q=q.order_by(col.asc() if order.lower()=="asc" else col.desc())
    # pagination
    if offset:
        q = q.offset(offset)
    if limit is not None:
        q = q.limit(limit)

    return q.all()

@app.post("/tasks", response_model=TaskRead)
def create_task(task: TaskBase, db: Session = Depends(get_db)):
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title cannot be empty")
    new_task = TaskDB(title=task.title.strip(), done=task.done)
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

@app.patch("/tasks/{task_id}", response_model=TaskRead)
def patch_task(task_id:int,data:TaskUpdate,db:Session=Depends(get_db)):
    task=db.get(TaskDB,task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    if data.title is not None:
        if not data.title.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title cannot be empty")
        task.title=data.title.strip()
    
    if data.done is not None:
        task.done=data.done

    db.commit()
    db.refresh(task)
    return task