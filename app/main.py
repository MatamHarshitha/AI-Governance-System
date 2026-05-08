from fastapi import FastAPI

from app.database.db import engine, Base
from app.api.routes import leads,dashboard
from app.api.routes.metrics import router as metricsrouter

Base.metadata.create_all(bind=engine)






app = FastAPI(
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1
    }
)

app.include_router(leads.router)
app.include_router(dashboard.router)
app.include_router(metricsrouter)

@app.get("/")
def read_root():
    return {"message": "API is running"}


