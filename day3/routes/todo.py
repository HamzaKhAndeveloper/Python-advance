from fastapi import HTTPException
from pydantic import BaseModel
from fastapi import APIRouter

class Todo(BaseModel):
    id: int
    title: str
    description: str
    status: bool = False
todoss = []
router = APIRouter() 

@router.get("/todos", status_code=200)
def get_all_todos():
    return todoss

@router.post("/todos",status_code=201)
def create_todo(todo: Todo):
    todoss.append(todo)
    return {"message":"todo created successfully"}

@router.get("/todos/{id}",status_code=200)
def gettodo(id: int):
    for todo in todoss:
        if todo.id == id:
           return todo
    raise HTTPException(status_code=404,detail="todo not found")

@router.put("/todos/{id}",status_code=200)
def updatetodo(id:int,update_todo: Todo):
    for todo in todoss:
        if todo.id == id:
            todo.title = update_todo.title
            todo.description = update_todo.description
            todo.status = update_todo.status
            return {"message":"todo updated successfully"}
    raise HTTPException(status_code=404,detail="todo not found")
    

@router.delete("/todos/{id}",status_code=200)
def deltodo(id: int):
    for todo in todoss:
        if todo.id == id:
            todoss.remove(todo)
            return {"message":"todo deleted successfully"}
    raise HTTPException(status_code=404,detail="todo not found")
    
