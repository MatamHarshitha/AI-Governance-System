from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import session_part
from app.database import model
from app.queue.client import redisclient, QueueName


router = APIRouter()


def db():

    db1 = session_part()

    try:
        yield db1

    finally:
        db1.close()


@router.get("/metrics")
def metrics(db: Session = Depends(db)):

    total_leads = db.query(model.Lead).count()

    completedtasks = (
        db.query(model.Task)
        .filter(model.Task.status == "done")
        .count()
    )

    failedtasks = (
        db.query(model.Task)
        .filter(model.Task.status == "failed")
        .count()
    )

    processingtasks = (
        db.query(model.Task)
        .filter(model.Task.status == "processing")
        .count()
    )

    pendingtasks = (
        db.query(model.Task)
        .filter(model.Task.status == "pending")
        .count()
    )

    queue_size = redisclient.llen(QueueName)

    return {
        "queue_size": queue_size,
        "total_leads": total_leads,
        "completed_tasks": completedtasks,
        "failed_tasks": failedtasks,
        "processing_tasks": processingtasks,
        "pending_tasks": pendingtasks
    }