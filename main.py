from fastapi import FastAPI 

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to My First FastAPI Application"}

@app.get("/user/{user}")
def getuser(user:str):
    return {"username":user}    