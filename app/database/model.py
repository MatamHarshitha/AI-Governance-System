
from app.database.db import Base
from sqlalchemy import Integer,String,DateTime,ForeignKey,Column
from datetime import datetime,timezone


class Lead(Base):
    __tablename__="leads"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(255),nullable=False)
    email=Column(String(255),nullable=False)
    company = Column(String(255), nullable=True)
    status = Column(String(255), default="new")
  
    dob = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    task_type = Column(String(255)) 
    status = Column(String(255), default="pending")  
    retries = Column(Integer, default=0)
    dob = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))









