from fastapi import APIRouter,Depends,HTTPException
from database import getdb
from sqlalchemy.orm import Session
from models.user import User
from models.product import Product
from pydantic import BaseModel
router = APIRouter()
class ProductSchema(BaseModel):
    name: str
    price: float
    description: str

@router.post("/product",status_code=201)
def create_product(product: ProductSchema,user_id:int,db:Session = Depends(getdb)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404,detail="user not found")
        products = Product(
            name = product.name,
            price = product.price,
            description = product.description,
            user_id = user.id
        )
        db.add(products)
        db.commit()
        return {"message":"product created successfully"}
    except Exception:
        db.rollback()
        return HTTPException(status_code=500,detail="internal server error")

@router.get("/product",status_code=200)
def get_product(db:Session = Depends(getdb)):
    products = db.query(Product).all()
    return products

@router.get("/product/{id}",status_code=200)
def get_product(id: int,db:Session = Depends(getdb)):
    products = db.query(Product).filter(Product.id == id).first()
    if products is None:
        raise HTTPException(status_code=404,detail="product not found")
    return products

@router.put("/product/{id}",status_code=200)
def update_product(id: int,update_product: ProductSchema,db:Session = Depends(getdb)):
    products = db.query(Product).filter(Product.id == id).first()
    if products is None:
        raise HTTPException(status_code= 404 , details= "product not found") 
    products.name = update_product.name
    products.price = update_product.price
    products.description = update_product.description
    db.commit()
    db.refresh(products) 
    return {"message":"product updated successfully"} 

@router.delete("/product/{id}",status_code=200)
def delete_product(id: int,db:Session = Depends(getdb)):
    products = db.query(Product).filter(Product.id == id).first()
    if products is None:
        raise HTTPException(status_code = 404,detail="product not found")
    db.delete(products)
    db.commit()
    return {"message":"product deleted successfully"}  
