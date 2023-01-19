from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from core.db import User
from users.backauth import current_active_user, fastapi_users

router = APIRouter()

templates = Jinja2Templates(directory="services/templates")

current_user = fastapi_users.current_user(True)


@router.get('/')
def index(request: Request, user: User = Depends(current_user)):
    if not user:
        return templates.TemplateResponse("index_auth.html", {"request": request})


