from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import models, database
from ..schemas.course import CourseCreate, CourseOut
from typing import List

router = APIRouter()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/courses", response_model=CourseOut)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = models.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@router.get("/courses", response_model=List[CourseOut])
def list_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).all()


@router.put("/courses/{course_id}", response_model=CourseOut)
def update_course(course_id: int, course: CourseCreate, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    db_course.name = course.name
    db_course.code = course.code
    db.commit()
    db.refresh(db_course)
    return db_course


@router.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    db.delete(db_course)
    db.commit()
    return {"status": "Course deleted"}
