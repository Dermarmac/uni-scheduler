from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import models, database
from ..schemas.instructor import InstructorCreate, InstructorOut
from typing import List

router = APIRouter()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/instructors", response_model=InstructorOut)
def create_instructor(instructor: InstructorCreate, db: Session = Depends(get_db)):
    db_instructor = models.Instructor(**instructor.dict())
    db.add(db_instructor)
    db.commit()
    db.refresh(db_instructor)
    return db_instructor


@router.get("/instructors", response_model=List[InstructorOut])
def list_instructors(db: Session = Depends(get_db)):
    return db.query(models.Instructor).all()


@router.put("/instructors/{instructor_id}", response_model=InstructorOut)
def update_instructor(
    instructor_id: int, instructor: InstructorCreate, db: Session = Depends(get_db)
):
    db_instructor = (
        db.query(models.Instructor)
        .filter(models.Instructor.id == instructor_id)
        .first()
    )
    db_instructor.name = instructor.name
    db.commit()
    db.refresh(db_instructor)
    return db_instructor


@router.delete("/instructors/{instructor_id}")
def delete_instructor(instructor_id: int, db: Session = Depends(get_db)):
    db_instructor = (
        db.query(models.Instructor)
        .filter(models.Instructor.id == instructor_id)
        .first()
    )
    db.delete(db_instructor)
    db.commit()
    return {"status": "Instructor deleted"}
