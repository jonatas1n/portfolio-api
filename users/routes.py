from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database.db import get_db

from .controller import create_user

router = APIRouter(prefix="/auth", tags=["Users"])
templates = Jinja2Templates(directory="templates")


@router.post("/register")
def register_user(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        create_user(name, email, password, db)
    except Exception as e:
        return templates.TemplateResponse(
            "register.html", {"request": request, "error": str(e)}
        )

    return RedirectResponse(url="/", status_code=303)


@router.get("/")
def register_user_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
