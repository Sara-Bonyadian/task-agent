from pydantic import BaseModel

# What fields a client must/can send to create/update a task
class TaskBase(BaseModel):
    title:str
    done:bool=False

# Response schema (what we send back) includes the DB id
class TaskRead(TaskBase):
    id:int

    # Pydantic v2: read data from ORM objects (SQLAlchemy) via attributes
    model_config={"from_attributes": True}