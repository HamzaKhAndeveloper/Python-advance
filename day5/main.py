from fastapi import FastAPI ,Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from database import Base,engine
from routes import order , product , user
import traceback
class Apperror(Exception):
    def __init__(self,message: str,status_code: int):
        self.message = message
        self.status_code = status_code



app = FastAPI()
Base.metadata.create_all(bind=engine)


app.include_router(product.router)
app.include_router(user.router)
app.include_router(order.router)

@app.exception_handler(Apperror)
def hanlde_except(request: Request,exc: Apperror):
    print(traceback.format_exc()) 
    return JSONResponse(
        status_code = exc.status_code,
        content={
            "success": False,
            "message": exc.message
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation Error",
            "errors": exc.errors()
        }
    )



@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error"
        }
    )



@app.middleware("http")
async def logs(request: Request,callnext):
    print(f"method: {request.method} url: {request.url}")
    protected_route = ["/order"]
    if any(request.url.path.startswith(path) for path in protected_route):
        token = request.headers.get("Authorization")
        if not token:
            return JSONResponse(
                status_code = 401,
                content = {"message": "unauthorized"}
            )

    response = await callnext(request)
    return response


@app.get("/")
def root():
    return {"message": "hello world"}
