from pydantic import BaseModel


class CartCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int


class AddToCartSchema(BaseModel):
    product_id: int
    user_id: int


class UserCartSchema(BaseModel):
    user_id: int


class UpdateCartSchema(BaseModel):
    user_id: int
    product_id: int
    quantity: int
