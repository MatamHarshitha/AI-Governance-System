from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from app.database.db import session_part
from app.database import model
from app.schema.lead import Input,Output
from app.queue.producer import pushtask


router = APIRouter()


def db():
    db1=session_part()
    try:
        yield db1
    finally:
        db1.close()

@router.post("/leads", response_model=Output)
def create_lead(inputval: Input, db: Session = Depends(db)):

    if not inputval.email:
        raise HTTPException(status_code=400, detail="Email is required")

    lead = model.Lead(
        name=inputval.name,
        email=inputval.email,
        company=inputval.company
    )

    db.add(lead)
    db.commit()
    db.refresh(lead)

    task = model.Task(
        lead_id=lead.id,
        task_type="outreach",
        status="pending"
    )

    db.add(task)
    db.commit()
    print("Calling pushtask...")
    pushtask({
        "task_id": task.id,
        "lead_id": lead.id,
        "type": task.task_type
    })

    return lead

@router.get("/leads")
def list_leads(db: Session = Depends(db)):
    leads = db.query(model.Lead).all()
    return leads