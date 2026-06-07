"""
SQLAlchemy ORM Models for DiabetesCare AI

Defines all 26 database tables for DPDP Act 2023 compliance.
Integrated with privacy.py for anonymisation and erasure.

Owner: Sahil Kumar Gupta (schema), Saugata Malakar (privacy fields)
"""

from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Float, DateTime, Boolean, Text, UUID, 
    ForeignKey, Index, CheckConstraint, UniqueConstraint, JSON
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()


# Core Patient Management

class Patient(Base):
    __tablename__ = "patients"
    
    patient_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)  # Direct ID - remove on export
    phone = Column(String(20), nullable=False)  # Direct ID - remove on export
    age = Column(Integer, nullable=False)  # Quasi-ID - generalise to 5-year bands
    gender = Column(String(10), nullable=False)  # Quasi-ID - retain
    village = Column(String(255), nullable=True)  # Quasi-ID - strip on export
    district = Column(String(255), nullable=False)  # Quasi-ID - retain
    aadhar_id = Column(String(12), nullable=True)  # Direct ID - remove on export
    consent_given_at = Column(DateTime, nullable=False)  # Quasi-ID - generalise to month
    consent_version = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    medical_history = relationship("PatientMedicalHistory", back_populates="patient")
    wound_sites = relationship("WoundSite", back_populates="patient")
    consents = relationship("Consent", back_populates="patient")
    sessions = relationship("MonitoringSession", back_populates="patient")
    alerts = relationship("Alert", back_populates="patient")
    subscriptions = relationship("Subscription", back_populates="patient")
    assignments_doctor = relationship("DoctorPatientAssignment", back_populates="patient")
    assignments_asha = relationship("AshaPatientAssignment", back_populates="patient")
    teleconsults = relationship("TeleconsultRequest", foreign_keys="TeleconsultRequest.patient_id", back_populates="patient")
    prescriptions = relationship("Prescription", foreign_keys="Prescription.patient_id", back_populates="patient")
    transactions = relationship("PaymentTransaction", back_populates="patient")
    
    __table_args__ = (
        Index("idx_patient_district", "district"),
        Index("idx_patient_created_at", "created_at"),
    )


class PatientMedicalHistory(Base):
    __tablename__ = "patient_medical_history"
    
    history_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"), nullable=False)
    hba1c = Column(Float, nullable=True)  # Non-sensitive - retain
    diabetes_duration_years = Column(Integer, nullable=True)  # Quasi-ID - generalise to 2-year bands
    blood_pressure = Column(String(50), nullable=True)  # Non-sensitive - retain
    prior_foot_problems = Column(Text, nullable=True)  # Non-sensitive - retain
    current_medications = Column(Text, nullable=True)  # Non-sensitive - retain
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="medical_history")
    
    __table_args__ = (
        Index("idx_med_history_patient", "patient_id"),
    )


class WoundSite(Base):
    __tablename__ = "wound_sites"
    
    wound_site_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"), nullable=False)
    location_code = Column(String(50), nullable=False)  # Non-sensitive - retain (left foot, etc.)
    initial_date = Column(DateTime, nullable=False)  # Quasi-ID - generalise to year-month
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="wound_sites")
    sessions = relationship("MonitoringSession", back_populates="wound_site")
    
    __table_args__ = (
        Index("idx_wound_site_patient", "patient_id"),
    )


class MonitoringSession(Base):
    __tablename__ = "monitoring_sessions"
    
    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"), nullable=False)
    wound_site_id = Column(UUID(as_uuid=True), ForeignKey("wound_sites.wound_site_id"), nullable=False)
    session_date = Column(DateTime, nullable=False)  # Quasi-ID - generalise to year-month
    asha_worker_id = Column(String(50), ForeignKey("asha_workers.worker_id"), nullable=True)  # Direct ID
    notes = Column(Text, nullable=True)  # Non-sensitive - retain
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="sessions")
    wound_site = relationship("WoundSite", back_populates="sessions")
    photographs = relationship("Photograph", back_populates="session")
    ai_results = relationship("AIResult", back_populates="session")
    
    __table_args__ = (
        Index("idx_session_patient", "patient_id"),
        Index("idx_session_date", "session_date"),
    )


class Photograph(Base):
    __tablename__ = "photographs"
    
    photo_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("monitoring_sessions.session_id"), nullable=False)
    file_path = Column(String(500), nullable=False)  # Quasi-ID - anonymise filename
    file_hash = Column(String(64), nullable=False)  # Non-sensitive - retain (for dedup)
    encrypted = Column(Boolean, default=True, nullable=False)  # Non-sensitive - must be True
    taken_at = Column(DateTime, nullable=False)  # Quasi-ID - generalise to hour
    created_at = Column(DateTime, default=datetime.utcnow)
    
    session = relationship("MonitoringSession", back_populates="photographs")
    
    __table_args__ = (
        Index("idx_photo_session", "session_id"),
        CheckConstraint("encrypted = true", name="check_photos_encrypted"),
    )


class AIResult(Base):
    __tablename__ = "ai_results"
    
    result_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("monitoring_sessions.session_id"), nullable=False)
    model_name = Column(String(100), nullable=False)  # Non-sensitive - retain
    model_version = Column(String(50), nullable=False)  # Non-sensitive - retain
    wagner_grade = Column(Integer, nullable=True)  # Non-sensitive - retain
    tissue_type = Column(String(50), nullable=True)  # Non-sensitive - retain
    infection_probability = Column(Float, nullable=True)  # Non-sensitive - retain
    created_at = Column(DateTime, default=datetime.utcnow)
    
    session = relationship("MonitoringSession", back_populates="ai_results")
    
    __table_args__ = (
        Index("idx_ai_result_session", "session_id"),
    )


class Alert(Base):
    __tablename__ = "alerts"
    
    alert_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"), nullable=False)
    severity = Column(String(20), nullable=False)  # Non-sensitive - retain
    message = Column(Text, nullable=False)  # Non-sensitive - retain
    acknowledged_at = Column(DateTime, nullable=True)  # Quasi-ID - generalise to day
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="alerts")
    
    __table_args__ = (
        Index("idx_alert_patient", "patient_id"),
    )


# ASHA Worker & Clinical

class AshaWorker(Base):
    __tablename__ = "asha_workers"
    
    worker_id = Column(String(50), primary_key=True)  # Direct ID - pseudonymise
    name = Column(String(255), nullable=False)  # Direct ID - remove on export
    phone = Column(String(20), nullable=False)  # Direct ID - remove on export
    pin_hash = Column(String(128), nullable=False)  # Direct ID - remove on export
    village = Column(String(255), nullable=True)  # Quasi-ID - strip on export
    district = Column(String(255), nullable=False)  # Quasi-ID - retain
    created_at = Column(DateTime, default=datetime.utcnow)
    
    assignments = relationship("AshaPatientAssignment", back_populates="worker")
    commissions = relationship("AshaCommission", back_populates="worker")
    
    __table_args__ = (
        Index("idx_asha_district", "district"),
    )


class AshaPatientAssignment(Base):
    __tablename__ = "asha_patient_assignments"
    
    assignment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asha_worker_id = Column(String(50), ForeignKey("asha_workers.worker_id"), nullable=False)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"), nullable=False)
    assigned_at = Column(DateTime, default=datetime.utcnow)  # Quasi-ID - generalise to month
    created_at = Column(DateTime, default=datetime.utcnow)
    
    worker = relationship("AshaWorker", back_populates="assignments")
    patient = relationship("Patient", back_populates="assignments_asha")
    
    __table_args__ = (
        Index("idx_asha_assignment", "asha_worker_id", "patient_id"),
    )


class AshaCommission(Base):
    __tablename__ = "asha_commissions"
    
    commission_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asha_worker_id = Column(String(50), ForeignKey("asha_workers.worker_id"), nullable=False)
    amount = Column(Float, nullable=False)  # Non-sensitive - retain
    period = Column(String(50), nullable=False)  # Non-sensitive - retain
    created_at = Column(DateTime, default=datetime.utcnow)
    
    worker = relationship("AshaWorker", back_populates="commissions")
    
    __table_args__ = (
        Index("idx_commission_worker", "asha_worker_id"),
    )


class AshaTrainingModule(Base):
    __tablename__ = "asha_training_modules"
    
    module_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)  # Non-sensitive - retain
    content = Column(Text, nullable=False)  # Non-sensitive - retain
    created_at = Column(DateTime, default=datetime.utcnow)


class Doctor(Base):
    __tablename__ = "doctors"
    
    doctor_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)  # Direct ID - remove on export
    email = Column(String(255), nullable=False)  # Direct ID - remove on export
    nmc_number = Column(String(50), nullable=False)  # Direct ID - remove on export
    specialisation = Column(String(100), nullable=False)  # Non-sensitive - retain
    languages = Column(String(255), nullable=False)  # Non-sensitive - retain
    fee_per_consult = Column(Float, nullable=False)  # Non-sensitive - retain
    created_at = Column(DateTime, default=datetime.utcnow)
    
    assignments = relationship("DoctorPatientAssignment", back_populates="doctor")
    teleconsults = relationship("TeleconsultRequest", foreign_keys="TeleconsultRequest.doctor_id", back_populates="doctor")
    prescriptions = relationship("Prescription", foreign_keys="Prescription.doctor_id", back_populates="doctor")


class DoctorPatientAssignment(Base):
    __tablename__ = "doctor_patient_assignments"
    
    assignment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("doctors.doctor_id"), nullable=False)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"), nullable=False)
    assigned_at = Column(DateTime, default=datetime.utcnow)  # Quasi-ID - generalise to month
    created_at = Column(DateTime, default=datetime.utcnow)
    
    doctor = relationship("Doctor", back_populates="assignments")
    patient = relationship("Patient", back_populates="assignments_doctor")


class TeleconsultRequest(Base):
    __tablename__ = "teleconsult_requests"
    
    request_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"), nullable=False)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("doctors.doctor_id"), nullable=False)
    requested_at = Column(DateTime, nullable=False)  # Quasi-ID - generalise to hour
    completed_at = Column(DateTime, nullable=True)  # Quasi-ID - generalise to hour
    notes = Column(Text, nullable=True)  # Non-sensitive - retain
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", foreign_keys=[patient_id], back_populates="teleconsults")
    doctor = relationship("Doctor", foreign_keys=[doctor_id], back_populates="teleconsults")


class Prescription(Base):
    __tablename__ = "prescriptions"
    
    prescription_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"), nullable=False)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("doctors.doctor_id"), nullable=False)
    medicine = Column(String(255), nullable=False)  # Non-sensitive - retain
    dosage = Column(String(100), nullable=False)  # Non-sensitive - retain
    duration_days = Column(Integer, nullable=False)  # Non-sensitive - retain
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", foreign_keys=[patient_id], back_populates="prescriptions")
    doctor = relationship("Doctor", foreign_keys=[doctor_id], back_populates="prescriptions")


# Subscriptions & Payments

class SubscriptionTier(Base):
    __tablename__ = "subscription_tiers"
    
    tier_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)  # Non-sensitive - retain
    price = Column(Float, nullable=False)  # Non-sensitive - retain
    features = Column(Text, nullable=False)  # Non-sensitive - retain
    created_at = Column(DateTime, default=datetime.utcnow)
    
    subscriptions = relationship("Subscription", back_populates="tier")


class Subscription(Base):
    __tablename__ = "subscriptions"
    
    subscription_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"), nullable=False)
    tier_id = Column(UUID(as_uuid=True), ForeignKey("subscription_tiers.tier_id"), nullable=False)
    start_date = Column(DateTime, nullable=False)  # Quasi-ID - generalise to month
    end_date = Column(DateTime, nullable=True)  # Quasi-ID - generalise to month
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="subscriptions")
    tier = relationship("SubscriptionTier", back_populates="subscriptions")


class PaymentTransaction(Base):
    __tablename__ = "payment_transactions"
    
    transaction_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"), nullable=False)
    amount = Column(Float, nullable=False)  # Non-sensitive - retain
    transaction_date = Column(DateTime, nullable=False)  # Quasi-ID - generalise to month
    status = Column(String(50), nullable=False)  # Non-sensitive - retain
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="transactions")
    
    __table_args__ = (
        Index("idx_transaction_patient", "patient_id"),
    )


# Session Management & Notifications

class SessionSchedule(Base):
    __tablename__ = "session_schedule"
    
    schedule_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"), nullable=False)
    asha_worker_id = Column(String(50), ForeignKey("asha_workers.worker_id"), nullable=False)
    scheduled_date = Column(DateTime, nullable=False)  # Quasi-ID - generalise to week
    reminder_sent_at = Column(DateTime, nullable=True)  # Quasi-ID - generalise to day
    created_at = Column(DateTime, default=datetime.utcnow)


class Notification(Base):
    __tablename__ = "notifications"
    
    notification_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)  # Direct ID - pseudonymise
    message = Column(Text, nullable=False)  # Non-sensitive - retain
    read_at = Column(DateTime, nullable=True)  # Quasi-ID - generalise to day
    created_at = Column(DateTime, default=datetime.utcnow)


class NotificationPreference(Base):
    __tablename__ = "notification_preferences"
    
    pref_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)  # Direct ID - pseudonymise
    sms_enabled = Column(Boolean, default=True)  # Non-sensitive - retain
    email_enabled = Column(Boolean, default=True)  # Non-sensitive - retain
    push_enabled = Column(Boolean, default=True)  # Non-sensitive - retain
    created_at = Column(DateTime, default=datetime.utcnow)


# Audit & Research

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)  # Direct ID - pseudonymise for audit
    action = Column(String(100), nullable=False)  # Non-sensitive - retain
    table_name = Column(String(100), nullable=False)  # Non-sensitive - retain
    record_id = Column(UUID(as_uuid=True), nullable=False)  # Direct ID - pseudonymise
    timestamp = Column(DateTime, default=datetime.utcnow)  # Non-sensitive - retain
    meta_data = Column(JSON, nullable=True)  # Non-sensitive - retain (renamed from metadata)
    
    __table_args__ = (
        Index("idx_audit_timestamp", "timestamp"),
        Index("idx_audit_action", "action"),
    )


class ResearchExport(Base):
    __tablename__ = "research_exports"
    
    export_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exported_by = Column(UUID(as_uuid=True), nullable=False)  # Direct ID - pseudonymise
    table_name = Column(String(100), nullable=False)  # Non-sensitive - retain
    row_count = Column(Integer, nullable=False)  # Non-sensitive - retain
    k_anonymity_verified = Column(Boolean, default=False)  # Non-sensitive - must be True
    export_date = Column(DateTime, default=datetime.utcnow)  # Quasi-ID - generalise to month
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        CheckConstraint("k_anonymity_verified = true", name="check_k_anonymity_verified"),
    )


class Consent(Base):
    __tablename__ = "consents"
    
    consent_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"), nullable=False)
    consent_version = Column(Integer, nullable=False)  # Non-sensitive - retain
    data_use_category = Column(String(100), nullable=False)  # Non-sensitive - retain
    given_at = Column(DateTime, nullable=False)  # Quasi-ID - generalise to month
    expires_at = Column(DateTime, nullable=True)  # Quasi-ID - generalise to month
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="consents")


class AppConfig(Base):
    __tablename__ = "app_config"
    
    config_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = Column(String(255), nullable=False, unique=True)  # Non-sensitive - retain
    value = Column(Text, nullable=False)  # Non-sensitive - retain
    created_at = Column(DateTime, default=datetime.utcnow)


# Week 4 - Clinical NLP (Saugata Malakar)

class ClinicalNote(Base):
    """
    Stores doctor's free-text consultation notes and structured NLP output.
    Week 4 - Saugata Malakar
    """
    __tablename__ = "clinical_notes"
    
    note_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"), nullable=False)
    session_id = Column(UUID(as_uuid=True), ForeignKey("monitoring_sessions.session_id"), nullable=True)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("doctors.doctor_id"), nullable=True)
    
    # Original free-text note
    original_text = Column(Text, nullable=False)  # Non-sensitive - retain
    
    # Structured NLP extracted entities
    wound_locations = Column(JSON, nullable=True)  # List of wound locations
    infection_signs = Column(JSON, nullable=True)  # List of infection signs
    treatment_recommendations = Column(JSON, nullable=True)  # List of treatments
    
    # Metadata
    extracted_at = Column(DateTime, nullable=True)  # When NLP was run
    nlp_model_version = Column(String(50), nullable=True)  # spaCy model version
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_clinical_note_patient", "patient_id"),
        Index("idx_clinical_note_session", "session_id"),
    )


class MultimodalAnalysis(Base):
    """
    Stores multimodal Gemini AI analysis results.
    Combines photograph + clinical data (HbA1c, diabetes duration, BP).
    Week 4 - Saugata Malakar
    """
    __tablename__ = "multimodal_analyses"
    
    analysis_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"), nullable=False)
    session_id = Column(UUID(as_uuid=True), ForeignKey("monitoring_sessions.session_id"), nullable=False)
    
    # Clinical data input
    hba1c = Column(Float, nullable=False)
    diabetes_duration_years = Column(Integer, nullable=False)
    systolic_bp = Column(Integer, nullable=False)
    diastolic_bp = Column(Integer, nullable=False)
    
    # Gemini output
    severity_grade = Column(Integer, nullable=False)  # 0-5 Wagner grade
    severity_label = Column(String(255), nullable=False)
    confidence = Column(Float, nullable=False)
    tissue_assessment = Column(Text, nullable=False)
    infection_risk = Column(String(50), nullable=False)  # low/moderate/high/critical
    healing_prognosis = Column(String(50), nullable=False)  # excellent/good/fair/poor/very_poor
    
    # Structured insights
    clinical_insights = Column(JSON, nullable=True)  # List of insights
    risk_factors = Column(JSON, nullable=True)  # List of risk factors
    immediate_actions = Column(JSON, nullable=True)  # List of actions
    
    follow_up_days = Column(Integer, nullable=False)
    specialist_referral = Column(Boolean, nullable=False)
    
    # Metadata
    raw_response = Column(Text, nullable=True)  # Full Gemini response
    model_name = Column(String(100), default="gemini-1.5-pro")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_multimodal_patient", "patient_id"),
        Index("idx_multimodal_session", "session_id"),
    )

