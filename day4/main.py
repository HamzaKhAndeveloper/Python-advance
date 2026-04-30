from fastapi import FastAPI
from routes import product
from database import engine,Base
Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(product.router)

@app.get("/",status_code=200)
def hello():
    return {"message":"Hello World"}