from fastapi import FastAPI, Request
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


from app.routs.users import router as user_router
from app.routs.companies import router as company_router
from app.routs.hashrates import router as hash_router
from app.routs.token import router as token_router
from app.routs.reports import router as report_router

app = FastAPI()
app.include_router(user_router)
app.include_router(company_router)
app.include_router(hash_router)
app.include_router(token_router)
app.include_router(report_router)


origins = [
    "https://localhost",
    "https://localhost:3000",
    "http://localhost:3000",
    "http://localhost",
    "https://www.razrab.digfarm.ru",
    "http://www.razrab.digfarm.ru",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(500)
def authjwt_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": 'DataBase Error'})


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message})


