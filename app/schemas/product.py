from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(..., description="The name of the product", example="Product Name")
    description: str = Field(..., description="The description of the product", example="Product Description")
    price: float = Field(..., description="The price of the product", example=100.0)
    image_url: str = Field(..., description="The image URL of the product", example="https://example.com/product.jpg")
    internal_cost: float = Field(..., description="The internal cost of the product", example=50.0)


class ProductUpdate(BaseModel):
    name: str | None = Field(..., description="The name of the product", example="Product Name")
    description: str | None = Field(..., description="The description of the product", example="Product Description")
    price: float | None = Field(..., description="The price of the product", example=100.0)
    image_url: str | None = Field(..., description="The image URL of the product", example="https://example.com/product.jpg")
    internal_cost: float | None = Field(..., description="The internal cost of the product", example=50.0)


class ProductResponse(BaseModel):
    id: int = Field(..., description="The ID of the product", example=1)
    name: str = Field(..., description="The name of the product", example="Product Name")           
    description: str = Field(..., description="The description of the product", example="Product Description")
    price: float = Field(..., description="The price of the product", example=100.0)
    image_url: str = Field(..., description="The image URL of the product", example="https://example.com/product.jpg")  
    internal_cost: float = Field(..., description="The internal cost of the product", example=50.0)
