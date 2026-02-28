from pydantic import BaseModel, Field


class CartCreate(BaseModel):
    user_id: int = Field(..., description="The ID of the user", example=1)
    product_id: int = Field(..., description="The ID of the product", example=1)
    quantity: int = Field(..., description="The quantity of the product", example=1)


class AddToCartSchema(BaseModel):
    product_id: int = Field(..., description="The ID of the product", example=1)
    image_url: str | None = Field(..., description="The image URL of the product", example="https://example.com/product.jpg")
    user_id: int | None = None


class UserCartSchema(BaseModel):
    user_id: int = Field(..., description="The ID of the user", example=1)


class UpdateCartSchema(BaseModel):
    user_id: int | None = Field(..., description="The ID of the user", example=1)
    product_id: int = Field(..., description="The ID of the product", example=1)
    quantity: int = Field(..., description="The quantity of the product", example=1)


class CheckoutCodeSchema(BaseModel):
    code: str = Field(
        ...,
        description="Fake payment code used for checkout",
        example="4242 4242 4242 4242",
    )
