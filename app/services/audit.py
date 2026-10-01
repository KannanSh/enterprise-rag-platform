from sqlalchemy.orm import Session
from app.models.entities import AuditEvent

def record_audit(db: Session, user_id: str, action: str, resource: str, detail: str = ""):
    db.add(AuditEvent(user_id=user_id, action=action, resource=resource, detail=detail))
    db.commit()
