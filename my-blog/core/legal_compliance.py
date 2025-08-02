"""
Legal Compliance Extensions for GDPR Stack

Advanced models and API endpoints for full legal compliance.
"""
from sqlalchemy import Column, String, DateTime, Text, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum
import uuid
from datetime import datetime, timedelta
import json
from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from core.database import DatabaseFactory, BaseModel
from core.config import settings

# --- 1. Legal Basis Tracking ---
class LegalBasis(Enum):
    CONSENT = "consent"
    CONTRACT = "contract"
    LEGAL_OBLIGATION = "legal_obligation"
    VITAL_INTERESTS = "vital_interests"
    PUBLIC_TASK = "public_task"
    LEGITIMATE_INTERESTS = "legitimate_interests"

class DataProcessingRecord(BaseModel):
    """Article 30 GDPR - Records of Processing Activities"""
    __tablename__ = "data_processing_records"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data_type = Column(String, nullable=False)
    legal_basis = Column(String, nullable=False)
    purpose = Column(Text, nullable=False)
    retention_period = Column(String)
    recipients = Column(Text)
    cross_border_transfers = Column(Text)
    technical_measures = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

# --- 2. Data Protection Impact Assessment (DPIA) ---
class DPIA(BaseModel):
    """Data Protection Impact Assessment - Article 35 GDPR"""
    __tablename__ = "dpia_assessments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_name = Column(String, nullable=False)
    processing_description = Column(Text, nullable=False)
    necessity_justification = Column(Text, nullable=False)
    risk_assessment = Column(Text, nullable=False)
    mitigation_measures = Column(Text, nullable=False)
    dpo_consultation = Column(Boolean, default=False)
    supervisory_authority_consultation = Column(Boolean, default=False)
    status = Column(String, default="draft")
    created_by = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    approved_at = Column(DateTime, nullable=True)

# --- 3. Minor Consent Handling ---
class MinorConsentVerification(BaseModel):
    """Special handling for minors under 16 (Article 8 GDPR)"""
    __tablename__ = "minor_consents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    claimed_age = Column(Integer)
    age_verification_method = Column(String)
    parent_guardian_email = Column(String)
    parent_consent_given = Column(Boolean, default=False)
    parent_consent_token = Column(String)
    verification_status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    verified_at = Column(DateTime, nullable=True)

# --- 4. Cross-Border Transfer Controls ---
class CrossBorderTransfer(BaseModel):
    """Article 44-49 GDPR - International Data Transfers"""
    __tablename__ = "cross_border_transfers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data_type = Column(String, nullable=False)
    destination_country = Column(String, nullable=False)
    recipient_organization = Column(String, nullable=False)
    legal_mechanism = Column(String, nullable=False)
    safeguards_description = Column(Text)
    transfer_date = Column(DateTime, default=datetime.utcnow)
    data_subject_id = Column(UUID(as_uuid=True), nullable=False)
    purpose = Column(Text, nullable=False)

# --- 5. Enhanced Consent Management ---
class ConsentRecord(BaseModel):
    """Enhanced consent with legal basis tracking"""
    __tablename__ = "consent_records"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    consent_type = Column(String, nullable=False)
    legal_basis = Column(String, nullable=False)
    purpose_description = Column(Text, nullable=False)
    given = Column(Boolean, default=True)
    consent_method = Column(String)
    consent_text_shown = Column(Text)
    ip_address = Column(String)
    user_agent = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime)
    withdrawal_date = Column(DateTime, nullable=True)
    last_confirmed = Column(DateTime)

# --- 6. DPO Communication System ---
class DPORequest(BaseModel):
    """Data Protection Officer Request Tracking"""
    __tablename__ = "dpo_requests"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_type = Column(String, nullable=False)
    data_subject_id = Column(UUID(as_uuid=True), nullable=True)
    subject = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    contact_email = Column(String, nullable=False)
    status = Column(String, default="open")
    priority = Column(String, default="medium")
    assigned_to = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    resolution_notes = Column(Text, nullable=True)

# --- 7. Automated Compliance Reporting ---
class ComplianceReport(BaseModel):
    """Automated GDPR Compliance Reports"""
    __tablename__ = "compliance_reports"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_type = Column(String, nullable=False)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    metrics = Column(Text)
    generated_at = Column(DateTime, default=datetime.utcnow)
    generated_by = Column(String, default="system")

# --- 8. API Extensions for Legal Compliance ---
router = APIRouter(prefix="/api/gdpr/legal", tags=["GDPR Legal"])

def get_admin_user():
    # Dummy admin user fetcher for example
    return uuid.uuid4()

def get_db():
    engine = DatabaseFactory.create_engine(settings.DATABASE_URL)
    SessionLocal = DatabaseFactory.create_session_factory(engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/dpia/create", tags=["GDPR Legal"], summary="Create new DPIA assessment", response_description="DPIA assessment created")
async def create_dpia(dpia_data: dict, admin_id: str = Depends(get_admin_user), db=Depends(get_db)):
    dpia = DPIA(
        project_name=dpia_data["project_name"],
        processing_description=dpia_data["processing_description"],
        necessity_justification=dpia_data["necessity_justification"],
        risk_assessment=json.dumps(dpia_data["risks"]),
        mitigation_measures=json.dumps(dpia_data["mitigations"]),
        created_by=admin_id
    )
    db.add(dpia)
    db.commit()
    return {"status": "created", "dpia_id": str(dpia.id)}

@router.get("/legal-basis/{data_type}", tags=["GDPR Legal"], summary="Get legal basis for specific data type", response_description="Legal basis details")
async def get_legal_basis(data_type: str, db=Depends(get_db)):
    record = db.query(DataProcessingRecord).filter_by(data_type=data_type).first()
    if not record:
        raise HTTPException(404, "Data processing record not found")
    return {
        "data_type": record.data_type,
        "legal_basis": record.legal_basis,
        "purpose": record.purpose,
        "retention_period": record.retention_period
    }

@router.post("/minor-consent/verify", tags=["GDPR Legal"], summary="Verify parent consent for minor", response_description="Minor consent verified")
async def verify_minor_consent(user_id: str, parent_token: str, db=Depends(get_db)):
    verification = db.query(MinorConsentVerification).filter_by(user_id=user_id, parent_consent_token=parent_token).first()
    if not verification:
        raise HTTPException(404, "Verification record not found")
    verification.parent_consent_given = True
    verification.verification_status = "verified"
    verification.verified_at = datetime.utcnow()
    db.commit()
    return {"status": "verified", "user_id": user_id}

@router.get("/compliance-report/{report_type}", tags=["GDPR Legal"], summary="Generate compliance report", response_description="Compliance report generated")
async def generate_compliance_report(report_type: str, admin_id: str = Depends(get_admin_user), db=Depends(get_db)):
    if report_type not in ["monthly", "quarterly", "annual"]:
        raise HTTPException(400, "Invalid report type")
    metrics = {
        "total_data_subjects": db.query(ConsentRecord).count(),
        "active_consents": db.query(ConsentRecord).filter_by(given=True).count(),
        "data_export_requests": db.query(DataProcessingRecord).count(),
        "deletion_requests": db.query(DataProcessingRecord).count(),
        "breach_incidents": 0,
        "dpo_requests": db.query(DPORequest).count(),
        "cross_border_transfers": db.query(CrossBorderTransfer).count()
    }
    report = ComplianceReport(
        report_type=report_type,
        period_start=datetime.now() - timedelta(days=30),
        period_end=datetime.now(),
        metrics=json.dumps(metrics)
    )
    db.add(report)
    db.commit()
    return {"status": "generated", "report_id": str(report.id), "metrics": metrics}
