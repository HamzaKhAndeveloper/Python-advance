from fastapi import FastAPI 
from database import Base,engine
from routes import order , product , user
app = FastAPI()
Base.metadata.create_all(bind=engine)


app.include_router(product.router)
app.include_router(user.router)
app.include_router(order.router)

@app.get("/")
def root():
    return {"message": "hello world"}
