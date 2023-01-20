from fastapi import FastAPI, Request
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.responses import JSONResponse

from routs.users import router as user_router
from routs.companies import router as company_router
from routs.hashrates import router as hash_router
from routs.permissions import router as permission_router

app = FastAPI()
app.include_router(user_router)
app.include_router(company_router)
app.include_router(hash_router)
app.include_router(permission_router)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message})


# uvicorn.run(app)
