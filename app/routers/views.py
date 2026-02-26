from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException

from app.core.security import get_current_user
from app.services.product import get_product
from app.services.user import get_user_by_id

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Home"})


@router.get("/login")
def login_view(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "title": "Login"})

@router.get("/register")
def login_view(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "title": "Register"})


@router.get("/shop")
def products_view(request: Request):
    return templates.TemplateResponse("products.html", {"request": request, "title": "Shop"})


@router.get("/bag")
def cart_view(request: Request):
    return templates.TemplateResponse("cart.html", {"request": request, "title": "Cart"})

@router.get("/product/{product_id}", response_class=HTMLResponse)
async def product_detail(request: Request, product_id: int):
    product = get_product(product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return templates.TemplateResponse(
        "detail.html",
        {
            "request": request,
            "p": dict(product)
        }
    )
    
@router.get("/profile/{user_id}")
def profile_view(request: Request, user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("profile.html", {"request": request, "title": "Profile", "user": user})    


@router.get("/contact")
def cart_view(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request, "title": "Contact Us"})

@router.get("/about-us")
def cart_view(request: Request):
    return templates.TemplateResponse("about.html", {"request": request, "title": "About Us"})