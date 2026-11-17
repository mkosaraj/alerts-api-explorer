from fastapi import FastAPI

import models  # noqa: F401  (registers models on Base.metadata)
from database import Base, engine
from routers import alerts

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Intelligence Layer -- Alert Explainer API")

app.include_router(alerts.router)


@app.get("/")
def root():
    return {"status": "ok", "message": "AI Intelligence Layer -- Alert Explainer API is running"}
