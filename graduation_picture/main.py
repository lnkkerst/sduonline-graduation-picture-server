from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.responses import JSONResponse
import os

from .database import SessionLocal, engine
from . import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Settings(BaseModel):
    if "JWT_SECRET" in os.environ:
        secret = os.environ["JWT_SECRET"]
    else:
        secret = "114514"
    authjwt_secret_key: str = secret
    authjwt_access_token_expires: int = 60 * 60 * 24 * 15


@AuthJWT.load_config  # type: ignore
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(_: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})  # type: ignore


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def get_root():
    return "hello world"
