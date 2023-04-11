from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.responses import JSONResponse
import os

from .database import SessionLocal, engine
from . import models, schemas, crud

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


@app.get("/user", response_model=schemas.User)
def get_current_user(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    """
    ## 获取当前用户的信息

    - 需要登录

    ### Returns

    - 当前用户信息
    """
    Authorize.jwt_required()
    db_user = crud.get_user(db=db, user_id=Authorize.get_jwt_subject())  # type: ignore
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/login", response_model=schemas.LoginResponse)
def login(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    db_user = crud.get_user_by_sdu_id(db, sdu_id=user.sdu_id)
    if not db_user:
        db_user = crud.create_user(db=db, user=user)

    access_token = Authorize.create_access_token(subject=db_user.id)  # type: ignore
    refresh_token = Authorize.create_refresh_token(subject=db_user.id)  # type: ignore
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": db_user,
    }


@app.get("/users", response_model=List[schemas.User])
def get_users(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.get_users(db=db, skip=skip, limit=limit)


@app.delete("/user", response_model=Optional[schemas.User])
def delete_current_user(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    user_id = Authorize.get_jwt_subject()
    return crud.delete_user(db=db, user_id=user_id)  # type: ignore


@app.put("/user", response_model=schemas.User)
def update_user(
    user: schemas.UserUpdate,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    user_id = Authorize.get_jwt_subject()
    return crud.update_user(db=db, user_id=user_id, user=user)  # type: ignore


@app.get("/campuses", response_model=List[schemas.Campus])
def get_campuses(skip: int = 0, limit: int = 0, db: Session = Depends(get_db)):
    return crud.get_campuses(db=db, skip=skip, limit=limit)


@app.get("/times", response_model=List[schemas.Time])
def get_times(
    skip: int = 0,
    limit: int = 20,
    campus_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return crud.get_times(db=db, skip=skip, limit=limit, campus_id=campus_id)
