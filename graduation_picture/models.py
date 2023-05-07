from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm.base import Mapped
from .database import Base
import uuid


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    sdu_id = Column(String, nullable=False, unique=True, index=True)
    name = Column(String, nullable=False, unique=False)
    signed_up = Column(Boolean, nullable=False, default=False)
    phone_number = Column(String, nullable=True)
    qq = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    multi_person = Column(Boolean, nullable=True)
    time_id = Column(String, ForeignKey("times.id"), nullable=True)
    time: Mapped[Optional["Time"]] = relationship()


class Campus(Base):
    __tablename__ = "campuses"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    times = relationship("Time", back_populates="campus")


class Time(Base):
    __tablename__ = "times"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    campus = relationship("Campus", back_populates="times")
    campus_id = Column(String, ForeignKey("campuses.id"))
    capacity = Column(Integer, nullable=False, default=0)
    users = relationship("User", back_populates="time")
