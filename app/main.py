from fastapi import FastAPI
from app.routers import auth, users, products, cart, views
from app.core.database import init_db
from app.core.config import get_settings
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

init_db()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(views.router) #templates jeje