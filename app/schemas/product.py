from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    internal_cost: float 

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    internal_cost: float  #data exposure