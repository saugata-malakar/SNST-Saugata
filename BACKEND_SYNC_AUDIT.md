# Backend Synchronization & Completion Audit

**Status:** Week 2 Privacy Complete | Week 3+ Backend Sync Required  
**Date:** 2024-11-15  
**Owner:** Saugata Malakar (Privacy/Wound Severity) + Sahil Kumar Gupta (API/DB)

---

## Executive Summary

The backend has a **critical gap**: Privacy module is complete (✓), but FastAPI infrastructure is **minimal** while a legacy Flask API exists. Frontends (mobile, doctor-dashboard) are built expecting FastAPI endpoints that don't exist yet.

**3 Critical Issues:**
1. **FastAPI not integrated with database models** → No session, no SQLAlchemy setup
2. **Missing inference routers** → wound.py, skin.py, eye.py (required by mobile + doctor-dashboard)
3. **Auth middleware not migrated** → Legacy Flask auth exists; FastAPI needs equivalents
4. **No utils layer** → Config, logging, image I/O missing

---

## Current State Analysis

### ✅ What Exists

#### Backend Database (COMPLETE)
- `backend/database/models.py` — 26 SQLAlchemy models (all tables mapped)
- `backend/database/privacy.py` — AnonymisationEngine, HMAC, k-anonymity (2507 lines)
- `backend/database/erasure.py` — ErasurePipeline, 72-hour deletion (400+ lines)
- `backend/database/README.md` — Privacy module guide

#### Backend API (MINIMAL)
- `backend/api/main.py` — FastAPI app factory (18 lines, health endpoint only)
- `backend/api/README.md` — Planned structure + endpoint specs
- `backend/api/routers/export.py` — Data export endpoint (privacy-gated)
- `backend/database/__init__.py`, `backend/api/__init__.py` — Empty imports

#### Frontend Expectations (Mobile + Doctor-Dashboard)
- **Mobile app:** [src/config/api.ts](mobile-app/src/config/api.ts) expects `API_BASE_URL` at `:8000`
- **Doctor dashboard:** [vite.config.js](doctor-dashboard/vite.config.js) proxies `/api` to `http://127.0.0.1:8000`
- **Routes expected:** `/api/v1/patients`, `/api/v1/doctors`, `/api/v1/wound/*`, `/api/v1/skin/*`, `/api/v1/eye/*`

#### ML Models (SCAFFOLDS)
- `ml/skin_classifier/` — README only, no implementation
- `ml/eye_models/` — README only, no implementation
- `ml/wound_severity/` — README only, no implementation

#### Legacy Flask API (EXISTS but separate)
- `backend/legacy/routes/patients.py` — Patient endpoints (Flask)
- `backend/legacy/routes/doctors.py` — Doctor endpoints (Flask)
- `backend/legacy/routes/asha.py` — ASHA worker endpoints (Flask)
- `backend/legacy/models.py` — Flask-SQLAlchemy models
- `backend/legacy/migrations/001_full_schema.py` — 26-table schema

---

### ❌ What's Missing

#### Critical (Blocking)

| Component | Purpose | Impact | Priority |
|-----------|---------|--------|----------|
| **Database session** | SQLAlchemy engine + SessionLocal | FastAPI can't connect to DB | **CRITICAL** |
| **Pydantic schemas** | Request/response models | No type validation | **CRITICAL** |
| **Auth middleware** | JWT verification (migrate from Flask) | No authentication | **CRITICAL** |
| **Config utils** | DATABASE_URL, settings loading | Can't configure app | **CRITICAL** |

#### High Priority (Blocking Inference)

| Component | Purpose | Impact | Priority |
|-----------|---------|--------|----------|
| `backend/api/routers/wound.py` | POST /v1/wound/* endpoints | Mobile can't submit wounds | **HIGH** |
| `backend/api/routers/skin.py` | POST /v1/skin/classify | Mobile can't classify skin | **HIGH** |
| `backend/api/routers/eye.py` | POST /v1/eye/* endpoints | Mobile can't submit eye data | **HIGH** |
| **Image I/O utils** | Save, retrieve, validate images | Can't handle photo uploads | **HIGH** |
| **Logging utils** | Structured logging for audit trail | No observability | **HIGH** |

#### Medium Priority (Blocking Dashboard)

| Component | Purpose | Impact | Priority |
|-----------|---------|--------|----------|
| `backend/api/routers/patients.py` | GET /v1/patients, POST, PUT | Doctor dashboard can't load data | **MEDIUM** |
| `backend/api/routers/doctors.py` | GET /v1/doctors/me, alerts | Doctor UI incomplete | **MEDIUM** |
| `backend/api/routers/alerts.py` | Alert CRUD | Doctor dashboard alerts | **MEDIUM** |
| **Database migrations** | Alembic setup | No schema versioning | **MEDIUM** |

---

## Synchronization Gaps

### 1. Database Layer Disconnect

**Issue:** Models exist, but FastAPI can't use them.

**Current:**
```python
# backend/database/models.py exists
class Patient(Base):
    __tablename__ = "patients"
    # ... all fields defined
```

**Missing:**
```python
# backend/database/session.py DOES NOT EXIST
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")  # Not loaded
engine = create_engine(DATABASE_URL)  # Not created
SessionLocal = sessionmaker(bind=engine)  # Not created
```

**Impact:** FastAPI routers can't access database.

---

### 2. FastAPI-Flask Endpoint Mismatch

**Flask API exists** (backend/legacy/routes/):
- `/v1/patients/me` → Returns patient data
- `/v1/doctors/me/alerts` → Returns alerts
- `/v1/wound/sessions` → Returns wound sessions

**FastAPI expecting** (per frontend):
- `/api/v1/patients` → Patient CRUD
- `/api/v1/doctors` → Doctor CRUD
- `/v1/wound/preprocess` → Preprocessing
- `/v1/skin/classify` → Skin classification
- `/v1/eye/*` → Eye predictions

**Issue:** Two different APIs. Mobile+dashboard built for FastAPI, but it doesn't have the endpoints.

**Solution:** Migrate Flask endpoints to FastAPI, add inference endpoints.

---

### 3. Privacy Module Not Integrated into Export

**Privacy module done:**
```python
# backend/database/privacy.py
engine = get_anonymisation_engine()
anonymised = engine.anonymise_record("patients", record)
```

**Export router exists:**
```python
# backend/api/routers/export.py
@router.post("/export")
async def export_data(query: ExportFilterQuery):
    # Calls anonymisation engine
```

**Missing:**
- Export router not registered in `main.py`
- No database session passed to export endpoint
- Export needs to query database, not just receive JSON

**Fix required:** Integrate export router into app, pass database session.

---

### 4. Auth Not Migrated

**Flask has:**
```python
# backend/legacy/middleware/auth_middleware.py
@require_auth  # Decorator
@require_patient  # Decorator
@require_doctor  # Decorator
@require_asha  # Decorator
```

**FastAPI needs:**
```python
# backend/api/middleware/auth.py (MISSING)
async def verify_jwt(token: str) -> dict:
    # Verify JWT
    return payload

async def get_current_user():
    # Dependency injection
    return user

# Usage in routers:
@router.get("/me")
async def get_me(user = Depends(get_current_user)):
    return user
```

**Impact:** No way to authenticate FastAPI requests.

---

### 5. Missing Utils

| Util | Location | Purpose |
|------|----------|---------|
| **Config** | `backend/utils/config.py` | Load DATABASE_URL, JWT_SECRET, etc. |
| **Image I/O** | `backend/utils/image.py` | Save, validate, retrieve photos |
| **Logging** | `backend/utils/logging.py` | Structured logs for audit |
| **Response formatting** | `backend/utils/response.py` | Consistent error/success responses |

---

## Files to Create/Update

### CRITICAL (Must Do First)

#### 1. `backend/database/session.py` (NEW)
```python
"""Database connection setup for FastAPI."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://...")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Blocks:** Everything that needs DB access

---

#### 2. `backend/utils/config.py` (NEW)
```python
"""Configuration loading from environment."""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    API_BASE_URL: str
    class Config:
        env_file = ".env"

settings = Settings()
```

**Blocks:** app initialization

---

#### 3. `backend/api/middleware/auth.py` (NEW)
Migrate JWT verification from Flask → FastAPI dependency.

**Blocks:** Protected routes (patients, doctors, etc.)

---

#### 4. `backend/api/routers/patients.py` (NEW)
```python
"""Patient endpoints (migrate from Flask legacy)."""
@router.get("/me")
async def get_patient_me(patient_id: str = Depends(get_current_patient)):
    # Query database using session
    return patient
```

**Used by:** Mobile app, doctor dashboard

---

#### 5. `backend/api/routers/doctors.py` (NEW)
```python
"""Doctor endpoints (migrate from Flask legacy)."""
@router.get("/me")
async def get_doctor_me(doctor_id: str = Depends(get_current_doctor)):
    return doctor
```

**Used by:** Doctor dashboard

---

#### 6. `backend/api/routers/alerts.py` (NEW)
```python
"""Alert management endpoints."""
@router.get("/")
async def get_alerts(patient_id: str):
    return alerts
```

**Used by:** Mobile app, doctor dashboard

---

### HIGH PRIORITY (Inference)

#### 7. `backend/api/routers/wound.py` (NEW)
```python
"""Wound inference endpoints."""
@router.post("/preprocess")
async def preprocess_wound(image: UploadFile):
    # Call ml/wound_severity for preprocessing

@router.post("/detect-coin")
async def detect_coin(image: UploadFile):
    # Call ml/wound_severity for coin detection

@router.post("/segment")
async def segment_wound(image: UploadFile):
    # Call SAM2 segmentation

@router.post("/classify")
async def classify_wound(image: UploadFile):
    # Call ml/wound_severity for Wagner grade + tissue + infection
```

**Used by:** Mobile app

---

#### 8. `backend/api/routers/skin.py` (NEW)
```python
"""Skin classification endpoint."""
@router.post("/classify")
async def classify_skin(image: UploadFile):
    # Call ml/skin_classifier
    return {"class": "tinea_pedis", "confidence": 0.92}
```

**Used by:** Mobile app

---

#### 9. `backend/api/routers/eye.py` (NEW)
```python
"""Eye health endpoints."""
@router.post("/detect-anemia")
async def detect_anemia(image: UploadFile):
    # Conjunctival pallor regression

@router.post("/detect-retinopathy")
async def detect_retinopathy(image: UploadFile):
    # DR stage classification

@router.post("/detect-conjunctival")
async def detect_conjunctival(image: UploadFile):
    # Conjunctival disease classification
```

**Used by:** Mobile app

---

#### 10. `backend/utils/image.py` (NEW)
Image validation, preprocessing, storage.

---

### MEDIUM PRIORITY

#### 11. `backend/utils/logging.py` (NEW)
Structured logging for audit trail integration with privacy module.

---

#### 12. `backend/utils/response.py` (NEW)
Consistent response formatting across all endpoints.

---

#### 13. Database Migrations (Alembic setup)
```
backend/database/alembic/
├── env.py
├── script.py.mako
└── versions/
    └── 001_initial_schema.py
```

---

## Integration Checklist

### Phase 1: Database + Config (Days 1-2)

- [ ] Create `backend/database/session.py` with SQLAlchemy setup
- [ ] Create `backend/utils/config.py` with Settings
- [ ] Update `backend/api/main.py` to:
  - [ ] Load config
  - [ ] Create engine
  - [ ] Include routers
- [ ] Create `.env` file with DATABASE_URL

**Deliverable:** `python -c "from backend.database.session import SessionLocal; print(SessionLocal())"` works

---

### Phase 2: Auth + Utils (Days 2-3)

- [ ] Create `backend/api/middleware/auth.py` (JWT verification)
- [ ] Create `backend/utils/image.py` (image validation)
- [ ] Create `backend/utils/response.py` (response formatting)
- [ ] Create `backend/utils/logging.py` (structured logging)

**Deliverable:** Can authenticate FastAPI requests; middleware passes tests

---

### Phase 3: CRUD Endpoints (Days 3-5)

- [ ] Migrate `backend/api/routers/patients.py` from Flask
- [ ] Migrate `backend/api/routers/doctors.py` from Flask
- [ ] Migrate `backend/api/routers/alerts.py` from Flask
- [ ] Integrate export router with database session
- [ ] Register all routers in `main.py`

**Deliverable:** `GET /api/v1/patients/me` returns patient data (authenticated)

---

### Phase 4: Inference Endpoints (Days 5-7)

- [ ] Create `backend/api/routers/wound.py` (call ml/wound_severity)
- [ ] Create `backend/api/routers/skin.py` (call ml/skin_classifier)
- [ ] Create `backend/api/routers/eye.py` (call ml/eye_models)
- [ ] Add image upload handling

**Deliverable:** `POST /api/v1/wound/classify` accepts image, returns Wagner grade

---

### Phase 5: Integration Testing (Days 7-8)

- [ ] Start FastAPI app: `uvicorn backend.api.main:app --reload`
- [ ] Test endpoints with mobile-app/doctor-dashboard
- [ ] Verify privacy module integration (export endpoint with k-anonymity gate)
- [ ] Run full test suite

**Deliverable:** Mobile app can connect; doctor dashboard loads; export is k-anonymity gated

---

## Required Environment Variables

Create `.env`:
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/diabetescare
JWT_SECRET=your-secret-key-here
API_BASE_URL=http://localhost:8000
LOG_LEVEL=INFO
```

---

## Testing Commands

### Once Session Setup Complete
```bash
python -c "from backend.database.session import SessionLocal, engine; from backend.database.models import Base; Base.metadata.create_all(engine)"
```

### Once FastAPI Configured
```bash
uvicorn backend.api.main:app --reload --port 8000
```

### Test Health Endpoint
```bash
curl http://localhost:8000/health
```

### Test Protected Endpoint (after auth added)
```bash
curl -H "Authorization: Bearer TOKEN" http://localhost:8000/api/v1/patients/me
```

---

## Synchronization Issues Summary

| Issue | Impact | Fix | Effort |
|-------|--------|-----|--------|
| No database session | FastAPI can't query DB | Create session.py | 1 hour |
| No config loader | Can't load DATABASE_URL | Create config.py | 30 min |
| No auth middleware | Requests not authenticated | Create auth.py | 2 hours |
| No CRUD endpoints | Frontend can't get data | Migrate from Flask | 8 hours |
| No inference endpoints | Mobile can't submit wounds | Create wound/skin/eye.py | 10 hours |
| No utils | Image/logging missing | Create utils | 4 hours |
| Export not integrated | Privacy module unused | Connect export to DB | 1 hour |
| **TOTAL** | **Blocks all frontend** | **All of above** | **~27 hours** |

---

## Priority Roadmap

### **WEEK 3A: Backend Foundation (Days 1-2)**
- ✓ Session setup
- ✓ Config loader
- ✓ Auth middleware
- Deliverable: Authenticated requests work

### **WEEK 3B: CRUD Endpoints (Days 3-5)**
- ✓ Patients CRUD (from Flask)
- ✓ Doctors CRUD (from Flask)
- ✓ Alerts CRUD
- ✓ Export integration
- Deliverable: Doctor-dashboard loads; export works

### **WEEK 3C: Inference Endpoints (Days 5-7)**
- ✓ Wound preprocessing
- ✓ Skin classification
- ✓ Eye predictions
- Deliverable: Mobile app can submit wounds, classify skin, predict eye health

### **WEEK 4: Integration + Polish**
- ✓ Full integration testing
- ✓ Error handling
- ✓ Rate limiting
- ✓ Documentation

---

## Next Immediate Action

**USER DECISION REQUIRED:**

1. **Should I build FastAPI from scratch** (recommended for clean architecture)?
   - Pros: Type-safe, async, modern
   - Time: ~27 hours
   - Use: This roadmap

2. **Should I migrate Flask app to FastAPI** (use existing Flask routes)?
   - Pros: Faster initial migration
   - Time: ~15 hours
   - Use: Adapt legacy code

**RECOMMENDATION:** Option 1 (clean build). Flask is legacy; FastAPI is better for async inference + privacy integration.

---

## Files Checklist for Week 3 Start

After Week 2 Privacy complete, **create these first:**

- [ ] `backend/database/session.py`
- [ ] `backend/utils/config.py`
- [ ] `backend/api/middleware/auth.py`
- [ ] Update `backend/api/main.py` (add session, config, middleware)
- [ ] Create `.env` (DATABASE_URL, JWT_SECRET)
- [ ] Run tests: `pytest tests/test_api_health.py -v`

**Then proceed:** CRUD endpoints → Inference endpoints → Integration tests

---

**Status After Completion:** FastAPI fully integrated, all frontends connected, privacy module live, inference endpoints available.

