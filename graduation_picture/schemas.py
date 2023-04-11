from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Campus(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True


class CampusCreate(BaseModel):
    name: str


class CampusUpdate(BaseModel):
    name: Optional[str]

    class Config:
        arbitrary_types_allowed = True


class CampusDelete(BaseModel):
    pass


class Time(BaseModel):
    id: str
    start: datetime
    end: datetime
    capacity: int
    campus_id: str

    class Config:
        orm_mode = True


class TimeCreate(BaseModel):
    start: datetime
    end: datetime
    capacity: Optional[int]
    campus_id: str

    class Config:
        arbitrary_types_allowed = True


class TimeUpdate(BaseModel):
    start: Optional[datetime]
    end: Optional[datetime]

    class Config:
        arbitrary_types_allowed = True


class TimeDelete(BaseModel):
    pass


class User(BaseModel):
    id: str
    sdu_id: str
    name: str
    signed_up: bool
    phone_number: Optional[str]
    gender: Optional[str]
    multi_person: Optional[bool]
    time_id: Optional[str]
    time: Optional[Time]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UserCreate(BaseModel):
    sdu_id: str
    password: str
    signed_up: Optional[bool]
    phone_number: Optional[str]
    gender: Optional[str]
    multi_person: Optional[bool]
    time_id: Optional[str]

    class Config:
        arbitrary_types_allowed = True


class UserUpdate(BaseModel):
    signed_up: bool
    phone_number: Optional[str]
    gender: Optional[str]
    multi_person: Optional[bool]
    time_id: Optional[str]

    class Config:
        arbitrary_types_allowed = True


class Login(BaseModel):
    sdu_id: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: User
