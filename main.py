from fastapi import FastAPI, Request
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.responses import JSONResponse

from services.users.routs import router as user_router
from services.companies.routs import router as company_router
from services.hashs.routs import router as hash_router
from services.permissions.routs import router as permission_router

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
