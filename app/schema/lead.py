from pydantic import BaseModel


class Input(BaseModel):   
    name: str
    email: str
    company: str | None = None


class Output(BaseModel):
    id: int
    name: str
    email: str
    company: str | None
    status: str

    class Config:
        from_attributes = True
