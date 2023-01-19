from fastapi import Depends, FastAPI, APIRouter, Request, Form
from fastapi.responses import RedirectResponse


router = APIRouter(prefix='/operation')

