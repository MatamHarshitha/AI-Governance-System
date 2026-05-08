import json
import time
import traceback

import redis
from sqlalchemy.orm import Session

from app.database.db import session_part
from app.database import model
from app.workers.ratelimiter import RateLimiter
from app.services.aiservice import classification
from app.workers.retry import retry
from app.services.webhook import webhook

redisclient = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

limiter = RateLimiter(interval=5)

Queuename = "taskqueue"
MaxTries = 3


def taskstatus(task, status: str, db: Session):

    task.status = status
    db.commit()


def processmessage(load: dict, db: Session):

    task = (
        db.query(model.Task)
        .filter(model.Task.id == load["task_id"])
        .first()
    )

    if not task:
        print("Task not found")
        return

    taskstatus(task, "processing", db)

    result = None

    for attempt in range(1, MaxTries + 1):
        try:

            limiter.wait()

            lead = (
            db.query(model.Lead)
            .filter(model.Lead.id == task.lead_id)
            .first()
        )

            if not lead:
                print("Lead not found")
                return

            print(f"[AI] Processing lead {lead.id}")

            result = classification(
            name=lead.name,
            company=lead.company
        )

            break

        except Exception as error:

            print(f"[RETRY] Attempt {attempt} failed")
            print(f"[RETRY] Reason: {error}")

            if attempt == MaxTries:
                break

            retry(attempt)

    if not result:

        task.status = "failed"

        db.commit()

        print(f"[FAILED] Task {task.id} permanently failed")

        return

    lead = (
        db.query(model.Lead)
        .filter(model.Lead.id == task.lead_id)
        .first()
    )

    if lead:
        lead.status = result

    task.status = "done"

    db.commit()
    webhook({
    "lead_id": lead.id,
    "name": lead.name,
    "company": lead.company,
    "status": lead.status
})


    print(f"[DONE] Task {task.id} completed")

    if lead:
        print(f"[DONE] Lead {lead.id} updated to '{lead.status}'")


def start_worker():

    print("Worker started...")

    while True:

        rawtask = redisclient.lpop(Queuename)

        if not rawtask:
            time.sleep(1)
            continue

        db = session_part()

        try:

            load = json.loads(rawtask)

            processmessage(load, db)

        except Exception:
            traceback.print_exc()

        finally:
            db.close()


if __name__ == "__main__":
    start_worker()


