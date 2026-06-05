from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.config import BASE_DIR
from app.ml.model_registry import get_active_model_name


router = APIRouter()
templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))


@router.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "active_page": "home", "active_model": get_active_model_name()},
    )


@router.get("/about")
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request, "active_page": "about"})

