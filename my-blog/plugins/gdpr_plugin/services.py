from .models import Consent, PolicyVersion
from sqlalchemy.orm import Session

def create_consent(db: Session, user_id: int, type: str, accepted: bool):
    consent = Consent(user_id=user_id, type=type, accepted=accepted)
    db.add(consent)
    db.commit()
    db.refresh(consent)
    return consent

def revoke_consent(db: Session, user_id: int, type: str):
    consent = db.query(Consent).filter_by(user_id=user_id, type=type, accepted=True).first()
    if consent:
        consent.accepted = False
        consent.revoked_at = consent.revoked_at or consent.accepted_at
        db.commit()
        db.refresh(consent)
    return consent

def list_consents(db: Session, user_id: int):
    return db.query(Consent).filter_by(user_id=user_id).all()

def get_policy_versions(db: Session, policy_type: str = None):
    q = db.query(PolicyVersion)
    if policy_type:
        q = q.filter_by(policy_type=policy_type)
    return q.order_by(PolicyVersion.published_at.desc()).all()
