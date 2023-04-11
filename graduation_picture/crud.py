from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas


def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 20):
    return db.query(models.User).offset(skip).limit(0).all()


def get_user_by_sdu_id(db: Session, sdu_id: str):
    return db.query(models.User).filter(models.User.sdu_id == sdu_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: str):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    else:
        return None


def update_user(db: Session, user_id: str, user: schemas.UserUpdate):
    db_user = get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.dict(exclude_unset=True)
    for k, v in user_data.items():
        setattr(db_user, k, v)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_campus(db: Session, campus_id: str):
    return db.query(models.Campus).filter(models.Campus.id == campus_id).first()


def get_campuses(db: Session, skip: int = 0, limit: int = 0):
    return db.query(models.Campus).offset(skip).limit(limit).all()


def create_campus(db: Session, campus: schemas.Campus):
    db_campus = models.Campus(**campus.dict())
    db.add(db_campus)
    db.commit()
    db.refresh(db_campus)
    return db_campus


def delete_campus(db: Session, campus_id: str):
    db_campus = get_campus(db=db, campus_id=campus_id)
    if db_campus:
        db.delete(db_campus)
        db.commit()
        return db_campus
    else:
        return None


def update_campus(db: Session, campus_id: str, campus: schemas.CampusUpdate):
    db_campus = get_campus(db=db, campus_id=campus_id)
    if not db_campus:
        raise HTTPException(status_code=404, detail="Campus not found")
    campus_data = campus.dict(exclude_unset=True)
    for k, v in campus_data.items():
        setattr(db_campus, k, v)
    db.add(db_campus)
    db.commit()
    db.refresh(db_campus)
    return db_campus


def get_time(db: Session, time_id: str):
    return db.query(models.Time).filter(models.Time.id == time_id).first()


def get_times(db: Session, skip: int = 0, limit: int = 20):
    return db.query(models.Time).offset(skip).limit(limit).all()


def create_time(db: Session, time: schemas.TimeCreate):
    db_time = models.Time(**time.dict())
    db.add(db_time)
    db.commit()
    db.refresh(db_time)
    return db_time


def delete_time(db: Session, time_id: str):
    db_time = get_time(db=db, time_id=time_id)
    if db_time:
        db.delete(db_time)
        db.commit()
        return db_time
    else:
        return None


def update_time(db: Session, time_id: str, time: schemas.TimeUpdate):
    db_time = get_time(db=db, time_id=time_id)
    if not db_time:
        raise HTTPException(status_code=404, detail="Time not found")
    time_data = time.dict(exclude_unset=True)
    for k, v in time_data.items():
        setattr(db_time, k, v)
    db.add(db_time)
    db.commit()
    db.refresh(db_time)
    return db_time
