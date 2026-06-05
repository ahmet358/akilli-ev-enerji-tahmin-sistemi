from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app import crud
from app.config import BASE_DIR
from app.database import get_db
from app.schemas import UserCreate


router = APIRouter(prefix="/users", tags=["Kullanıcılar"])
templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))


@router.get("/register")
def register_page(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "register.html",
        {"request": request, "users": crud.list_users(db), "active_page": "users", "error": None},
    )


@router.post("/register")
def register_user(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        user_data = UserCreate(full_name=full_name, email=email)
        existing_user = crud.get_user_by_email(db, user_data.email)
        if existing_user:
            return RedirectResponse(url=f"/prediction?user_id={existing_user.id}", status_code=303)
        user = crud.create_user(db, user_data)
    except ValidationError as exc:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "users": crud.list_users(db),
                "active_page": "users",
                "error": "Lütfen ad soyad ve e-posta alanlarını geçerli biçimde doldurun.",
            },
            status_code=422,
        )
    except IntegrityError:
        db.rollback()
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "users": crud.list_users(db),
                "active_page": "users",
                "error": "Bu e-posta adresiyle daha önce kullanıcı oluşturulmuş.",
            },
            status_code=409,
        )
    return RedirectResponse(url=f"/prediction?user_id={user.id}", status_code=303)
