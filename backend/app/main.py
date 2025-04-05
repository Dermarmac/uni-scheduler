from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.database import engine
from .db import models

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

from .routes.courses import router as course_router
from .routes.instructors import router as instructor_router
from .routes.timeslots import router as timeslot_router
from .routes.scheduling import router as scheduling_router

app.include_router(course_router)
app.include_router(instructor_router)
app.include_router(timeslot_router)
app.include_router(scheduling_router)
