from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import models, database
from ..schemas.timeslot import TimeslotCreate, TimeslotOut
from typing import List

router = APIRouter()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/timeslots", response_model=TimeslotOut)
def create_timeslot(timeslot: TimeslotCreate, db: Session = Depends(get_db)):
    db_timeslot = models.Timeslot(**timeslot.dict())
    db.add(db_timeslot)
    db.commit()
    db.refresh(db_timeslot)
    return db_timeslot


@router.get("/timeslots", response_model=List[TimeslotOut])
def list_timeslots(db: Session = Depends(get_db)):
    return db.query(models.Timeslot).all()


@router.put("/timeslots/{timeslot_id}", response_model=TimeslotOut)
def update_timeslot(
    timeslot_id: int, timeslot: TimeslotCreate, db: Session = Depends(get_db)
):
    db_timeslot = (
        db.query(models.Timeslot).filter(models.Timeslot.id == timeslot_id).first()
    )
    db_timeslot.day = timeslot.day
    db_timeslot.time = timeslot.time
    db.commit()
    db.refresh(db_timeslot)
    return db_timeslot


@router.delete("/timeslots/{timeslot_id}")
def delete_timeslot(timeslot_id: int, db: Session = Depends(get_db)):
    db_timeslot = (
        db.query(models.Timeslot).filter(models.Timeslot.id == timeslot_id).first()
    )
    db.delete(db_timeslot)
    db.commit()
    return {"status": "Timeslot deleted"}
