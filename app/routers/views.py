from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Home"})

@router.get("/login-view")
def login_view(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "title": "Login"})

@router.get("/products-view")
def products_view(request: Request):
    return templates.TemplateResponse("products.html", {"request": request, "title": "Products"})

@router.get("/cart-view")
def cart_view(request: Request):
    return templates.TemplateResponse("cart.html", {"request": request, "title": "Cart"})