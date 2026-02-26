from pydantic import BaseModel


class CartCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int


class AddToCartSchema(BaseModel):
    product_id: int
    image_url: str | None = None
    user_id: int | None = None


class UserCartSchema(BaseModel):
    user_id: int


class UpdateCartSchema(BaseModel):
    user_id: int | None = None
    product_id: int
    quantity: int
