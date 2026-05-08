from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.db import session_part
from app.database import model


router = APIRouter()


def db():

    database = session_part()

    try:
        yield database

    finally:
        database.close()


@router.get("/dashboard")
def dashboardstatus(db: Session = Depends(db)):

    total = db.query(func.count(model.Lead.id)).scalar()

    pendingtasks = (
        db.query(func.count(model.Task.id))
        .filter(model.Task.status == "pending")
        .scalar()
    )

    processingtasks = (
        db.query(func.count(model.Task.id))
        .filter(model.Task.status == "processing")
        .scalar()
    )

    completedtasks = (
        db.query(func.count(model.Task.id))
        .filter(model.Task.status == "done")
        .scalar()
    )

    failedtasks = (
        db.query(func.count(model.Task.id))
        .filter(model.Task.status == "failed")
        .scalar()
    )

    return {
        "total_leads": total,
        "pending_tasks": pendingtasks,
        "processing_tasks": processingtasks,
        "completed_tasks": completedtasks,
        "failed_tasks": failedtasks
    }