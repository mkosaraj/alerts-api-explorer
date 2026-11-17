from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from services.explainer import generate_explanation

router = APIRouter(prefix="/alerts", tags=["alerts"])


def _get_alert_or_404(alert_id: int, db: Session) -> models.Alert:
    alert = db.get(models.Alert, alert_id)
    if alert is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")
    return alert


@router.post("/", response_model=schemas.AlertOut, status_code=status.HTTP_201_CREATED)
def create_alert(alert_in: schemas.AlertCreate, db: Session = Depends(get_db)):
    alert = models.Alert(**alert_in.model_dump())
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


@router.get("/", response_model=list[schemas.AlertOut])
def list_alerts(db: Session = Depends(get_db)):
    return db.query(models.Alert).all()


@router.get("/{alert_id}", response_model=schemas.AlertOut)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    return _get_alert_or_404(alert_id, db)


@router.post("/{alert_id}/explain", response_model=schemas.ExplainResponse)
def explain_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = _get_alert_or_404(alert_id, db)
    return schemas.ExplainResponse(
        alert_id=alert.id,
        explanation=generate_explanation(alert),
        generated_at=datetime.now(timezone.utc),
    )
