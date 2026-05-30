from sqlalchemy.orm import Session

from app.db.models import AuditLog


class AuditService:
    def __init__(self, db: Session):
        self.db = db

    def record(self, action: str, payload: dict, user_id: str | None = None) -> AuditLog:
        event = AuditLog(user_id=user_id, action=action, payload=payload)
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event
