# DiabetesCare AI — Quick Navigation Guide

**Purpose:** Find code quickly without reading all 10,000+ lines  
**For:** New developers, cross-team coordination, quick debugging

---

## 🗺️ REPOSITORY STRUCTURE

```
diabetescare-ai/
├── backend/                                ← MAIN BACKEND CODE
│   ├── api/                                ← FastAPI application
│   │   ├── main.py                        ← Entry point (app factory, startup/shutdown)
│   │   ├── middleware.py                  ← JWT auth, token generation
│   │   └── routers/
│   │       ├── export.py                  ← Data export endpoint (Week 2-3)
│   │       ├── patients.py                ← PENDING (patient CRUD - Week 3)
│   │       ├── doctors.py                 ← PENDING (doctor CRUD - Week 3)
│   │       └── alerts.py                  ← PENDING (alert management - Week 3)
│   │
│   ├── database/
│   │   ├── models.py                      ← 26 SQLAlchemy ORM tables ✅ COMPLETE
│   │   ├── session.py                     ← Database connection (SessionLocal, get_db) ✅
│   │   ├── privacy.py                     ← Anonymisation engine (Week 2) ⏳ PENDING
│   │   └── erasure.py                     ← Deletion pipeline (Week 2) ⏳ PENDING
│   │
│   ├── utils/
│   │   ├── config.py                      ← Pydantic Settings (.env loading) ✅
│   │   ├── response.py                    ← Response schemas (SuccessResponse, etc) ✅
│   │   ├── logging.py                     ← AuditLogger (DPDP compliance) ✅
│   │   └── __init__.py
│   │
│   ├── legacy/                             ← FLASK OLD IMPLEMENTATION
│   │   ├── app.py                         ← Old Flask app entry point
│   │   ├── config.py                      ← Old Flask config
│   │   ├── models/                        ← SQLAlchemy models (same schema as new)
│   │   ├── routes/                        ← Flask routes (to be migrated to FastAPI)
│   │   │   ├── patients.py                ← Patient endpoints (TO MIGRATE)
│   │   │   ├── doctors.py                 ← Doctor endpoints (TO MIGRATE)
│   │   │   ├── alerts.py                  ← Alert endpoints (TO MIGRATE)
│   │   │   ├── auth.py                    ← Authentication (obsolete, use middleware.py)
│   │   │   ├── consultations.py           ← Consultation endpoints (Week 3B)
│   │   │   ├── screenings.py              ← Screening endpoints (Phase B/C)
│   │   │   └── ... (15+ other routes)
│   │   ├── utils/                         ← Helper functions (JWT, validation, etc)
│   │   ├── middleware/                    ← Old middleware (auth, rate limiting, logging)
│   │   ├── migrations/                    ← Alembic database migrations
│   │   │   └── 001_full_schema.sql        ← Initial 26-table schema ⭐ READ THIS
│   │   ├── tests/                         ← Old Flask tests
│   │   └── seeds.py                       ← Demo data generator
│   │
│   └── __init__.py
│
├── ml/                                     ← MACHINE LEARNING MODELS
│   ├── wound_severity/                    ← Diabetic foot wound grading
│   │   ├── model.py                       ← EfficientNet-B0 (Wagner 0-4)
│   │   ├── train.py                       ← Training script (with dataset path)
│   │   └── inference.py                   ← Inference wrapper (for API)
│   │
│   ├── skin_classifier/                   ← Skin disease classification
│   │   ├── model.py                       ← EfficientNet-B3 (8 diseases)
│   │   ├── train.py                       ← Training script
│   │   └── inference.py
│   │
│   └── eye_models/                        ← 3 eye disease models
│       ├── 3a_pallor_regression/          ← Conjunctival pallor (severity 0-5)
│       ├── 3b_dr_classification/          ← Diabetic retinopathy (5 stages)
│       ├── 3c_conjunctival/                ← Conjunctival diseases (classification)
│       └── ensemble.py                    ← Model combination + inference
│
├── cv/                                     ← COMPUTER VISION PREPROCESSING
│   ├── preprocessing/
│   │   ├── coin_detection.py              ← Detect reference coin for scale
│   │   ├── normalization.py               ← Image lighting/angle correction
│   │   └── __init__.py
│   │
│   ├── segmentation/
│   │   ├── sam2_wrapper.py                ← SAM2 for wound extraction
│   │   └── __init__.py
│   │
│   └── tests/
│       └── test_coin_detection.py
│
├── frontend/
│   ├── mobile-app/                        ← React Native (patient + ASHA)
│   │   ├── src/
│   │   │   ├── screens/
│   │   │   │   ├── PatientDashboard.tsx   ← Patient home screen
│   │   │   │   ├── UploadWound.tsx        ← Camera + wound upload
│   │   │   │   └── ViewResults.tsx        ← Wound classification results
│   │   │   ├── services/
│   │   │   │   └── api.js                 ← API client (calls /api/v1/*)
│   │   │   └── App.tsx                    ← App entry point
│   │   └── package.json
│   │
│   └── doctor-dashboard/                  ← React + Vite (doctor alert management)
│       ├── src/
│       │   ├── components/
│       │   │   ├── AlertInbox.tsx         ← Doctor's alert list
│       │   │   ├── PatientSummary.tsx     ← Patient details view
│       │   │   └── PrescribeModal.tsx     ← Doctor's prescription form
│       │   ├── services/
│       │   │   └── api.js                 ← API client
│       │   └── App.tsx
│       └── package.json
│
├── tests/                                  ← UNIT & INTEGRATION TESTS
│   ├── test_anonymisation.py              ← Privacy module tests (100+) ✅
│   ├── test_erasure.py                    ← Erasure pipeline tests ⏳
│   ├── test_week2_integration.py          ← End-to-end privacy workflows ✅
│   └── conftest.py                        ← Test fixtures (test DB, test data)
│
├── deployment/                             ← DOCKER & CLOUD CONFIG
│   ├── Dockerfile                         ← FastAPI container
│   ├── docker-compose.yml                 ← PostgreSQL + Redis local dev
│   └── cloud-run.yaml                     ← Google Cloud Run deployment
│
├── .env.local                              ← Development environment variables ✅
├── .env.example                            ← Environment template
├── README.md                               ← Project overview
├── requirements.txt                        ← Python dependencies
├── pyproject.toml                          ← Project metadata
├── DPDP_COMPLIANCE.md                      ← Privacy/compliance docs ✅
├── PII_FIELD_MAP.md                        ← All 26 tables + PII classification ✅
│
└── DOCUMENTATION/ (THIS SESSION)
    ├── CODEBASE_AUDIT.md                  ← Complete system understanding
    ├── TEAM_SYNC_MAP.md                   ← Team responsibilities + blockers
    ├── WEEK2_TASK_BREAKDOWN.md            ← Detailed privacy.py + erasure.py tasks
    ├── BACKEND_SYNC_AUDIT.md              ← Previous sync status
    ├── COMPLETE_PROJECT_SYNC_GUIDE.md     ← Architecture overview
    └── WEEK3A_PHASE1_COMPLETION_SUMMARY.md ← Phase 1 status

```

---

## 🔍 "WHERE DO I FIND...?" QUICK REFERENCE

### Database & Schema
| What | Where | Status |
|------|-------|--------|
| All 26 table definitions | `backend/database/models.py` | ✅ Complete |
| SQL schema (migrations) | `backend/legacy/migrations/001_full_schema.sql` | ✅ |
| PII classification | `backend/database/privacy.py` (PII_FIELD_MAP dict) | ⏳ Pending |
| Database connection | `backend/database/session.py` | ✅ |
| ORM relationships | `backend/database/models.py` (back_populates, relationships) | ✅ |

### Authentication & Security
| What | Where |
|------|-------|
| JWT token creation | `backend/api/middleware.py::create_access_token()` |
| JWT verification | `backend/api/middleware.py::verify_jwt()` |
| User type dependencies | `backend/api/middleware.py::get_current_patient/doctor/asha()` |
| Old Flask auth | `backend/legacy/middleware/auth_middleware.py` (OBSOLETE) |
| Configuration (secrets) | `backend/utils/config.py` + `.env.local` |

### Privacy & Compliance
| What | Where | Status |
|------|-------|--------|
| Anonymisation engine | `backend/database/privacy.py` | ⏳ Week 2 |
| Erasure pipeline | `backend/database/erasure.py` | ⏳ Week 2 |
| k-anonymity verification | `backend/database/privacy.py::verify_k_anonymity()` | ⏳ Week 2 |
| Audit logging | `backend/utils/logging.py::AuditLogger` | ✅ |
| PII field map | `backend/database/privacy.py::PII_FIELD_MAP` dict | ⏳ Week 2 |
| Export endpoint | `backend/api/routers/export.py` | ⏳ Needs DB integration |
| DPDP compliance | `DPDP_COMPLIANCE.md` | ✅ |

### API Endpoints (Current)
| Endpoint | File | Status | Method |
|----------|------|--------|--------|
| `/health` | `backend/api/main.py` | ✅ | GET |
| `/api/v1/export` | `backend/api/routers/export.py` | ⏳ (no DB yet) | POST |
| `/api/v1/patients/me` | `backend/legacy/routes/patients.py` | ⏳ (Flask, needs migration) | GET |
| `/api/v1/doctors/me` | `backend/legacy/routes/doctors.py` | ⏳ (Flask, needs migration) | GET |
| `/api/v1/alerts` | `backend/legacy/routes/alerts.py` | ⏳ (Flask, needs migration) | GET |
| `/api/v1/wound/classify` | `backend/api/routers/wound.py` (PENDING) | ⏳ | POST |
| `/api/v1/skin/classify` | `backend/api/routers/skin.py` (PENDING) | ⏳ | POST |

### ML Models
| Model | Location | Status | Type |
|-------|----------|--------|------|
| Wound severity | `ml/wound_severity/` | ⏳ Training | EfficientNet-B0 |
| Skin classifier | `ml/skin_classifier/` | ⏳ Training | EfficientNet-B3 |
| Eye - Pallor | `ml/eye_models/3a_pallor_regression/` | ⏳ Training | Regression |
| Eye - Retinopathy | `ml/eye_models/3b_dr_classification/` | ⏳ Training | Classification |
| Eye - Conjunctival | `ml/eye_models/3c_conjunctival/` | ⏳ Training | Classification |

### Computer Vision
| Component | Location | Status |
|-----------|----------|--------|
| Coin detection | `cv/preprocessing/coin_detection.py` | ⏳ Scaffold |
| Image normalization | `cv/preprocessing/normalization.py` | ⏳ Scaffold |
| SAM2 segmentation | `cv/segmentation/sam2_wrapper.py` | ⏳ Scaffold |

### Frontend (Mobile & Dashboard)
| App | Location | Status |
|-----|----------|--------|
| React Native mobile | `frontend/mobile-app/src/` | ✅ Ready (waiting for API) |
| Doctor dashboard | `frontend/doctor-dashboard/src/` | ✅ Ready (waiting for API) |
| API client (mobile) | `frontend/mobile-app/src/services/api.js` | ✅ |
| API client (dashboard) | `frontend/doctor-dashboard/src/services/api.js` | ✅ |

### Testing
| Test Suite | Location | Status |
|------------|----------|--------|
| Anonymisation tests | `tests/test_anonymisation.py` | ✅ 100+ passing |
| Erasure tests | `tests/test_erasure.py` | ⏳ Pending |
| Integration tests | `tests/test_week2_integration.py` | ✅ 8+ passing |
| Legacy Flask tests | `backend/legacy/tests/` | ✅ (old) |
| FastAPI tests | `tests/test_api.py` | ⏳ Pending |

---

## 🚀 QUICK START WORKFLOWS

### "I want to start the backend"
```bash
cd backend
uvicorn api.main:app --reload --port 8000
# Requires: DATABASE_URL in .env.local
# Starts: FastAPI at http://localhost:8000
```

### "I need to understand the database schema"
```
READ THESE IN ORDER:
1. backend/database/models.py (SQLAlchemy definitions)
2. backend/legacy/migrations/001_full_schema.sql (SQL version)
3. PII_FIELD_MAP.md (classification of each field)
4. CODEBASE_AUDIT.md (complete mapping)
```

### "I need to migrate a Flask route to FastAPI"
```
EXAMPLE: Migrate backend/legacy/routes/patients.py

1. Read: backend/legacy/routes/patients.py (Flask endpoints)
2. Check: backend/database/models.py (what tables you'll query)
3. Create: backend/api/routers/patients.py
   - Use: Session = Depends(get_db) for database
   - Return: response.success_response(data) from backend/utils/response.py
   - Auth: Use @router.get(... Depends(get_current_patient)) from middleware.py
4. Register: in backend/api/main.py app.include_router(patients_router)
5. Test: curl http://localhost:8000/api/v1/patients/me
```

### "I need to add privacy to an endpoint"
```
USE THIS PATTERN:

from backend.database.privacy import AnonymisationEngine, AuditLogger

@router.get("/api/v1/export")
async def export_data(...):
    # 1. Query data
    records = db.query(Patient).all()
    
    # 2. Anonymise
    anon_records, meta = AnonymisationEngine.anonymise_dataset(
        "Patient", records
    )
    
    # 3. Verify k-anonymity
    if not meta["k_anonymity_compliant"]:
        raise HTTPException(400, "k-anonymity failed")
    
    # 4. Log
    AuditLogger.log_data_export(...)
    
    # 5. Return
    return response.success_response(anon_records)
```

### "I need to understand team dependencies"
```
READ: TEAM_SYNC_MAP.md (who is doing what, blockers, timeline)
```

### "I need to run tests"
```bash
# Run privacy tests
cd backend
python -m pytest tests/test_anonymisation.py -v

# Run all tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_anonymisation.py::TestPseudonymisation -v
```

---

## 📞 "HOW DO I...?"

### How do I query a patient record?
```python
from backend.database.session import SessionLocal
from backend.database.models import Patient
import uuid

db = SessionLocal()
patient = db.query(Patient).filter(
    Patient.patient_id == uuid.UUID("pat-uuid-123")
).first()
print(patient.name)  # ⚠️ This is PII, gets anonymised on export
```

### How do I authenticate a user?
```python
from backend.api.middleware import create_access_token, verify_jwt

# Generate token
token = create_access_token("pat-uuid-123", "patient")
print(token)  # JWT string

# Verify token
payload = verify_jwt(token)
print(payload.user_id)  # "pat-uuid-123"
```

### How do I get the current logged-in user in an endpoint?
```python
from backend.api.middleware import get_current_patient
from fastapi import Depends

@router.get("/api/v1/patients/me")
async def get_my_info(current_patient = Depends(get_current_patient)):
    return response.success_response({
        "patient_id": current_patient.patient_id,
        "name": current_patient.name
    })
```

### How do I return a standardized response?
```python
from backend.utils.response import response

# Success response
return response.success_response(
    data={"patient_id": "123"},
    message="Patient retrieved"
)

# Paginated response
return response.paginated_response(
    data=patients,
    page=1,
    page_size=10,
    total=100,
    message="All patients"
)

# Error response
raise HTTPException(400, detail=response.error_response("Invalid input"))
```

### How do I log a privacy event?
```python
from backend.utils.logging import AuditLogger

# Log data export
AuditLogger.log_data_export(
    user_id="user-123",
    user_type="researcher",
    table="Patient",
    record_count=50,
    k_anonymity_verified=True
)

# Log patient deletion
AuditLogger.log_patient_deletion(
    patient_id="pat-123",
    user_id="admin-user",
    reason="Patient requested erasure",
    rows_deleted=47
)
```

### How do I handle transactions in SQLAlchemy?
```python
from backend.database.session import SessionLocal

db = SessionLocal()
try:
    # Make changes
    patient = db.query(Patient).filter(...).first()
    patient.age = 35
    db.add(patient)
    
    # Commit
    db.commit()
except Exception as e:
    # Rollback on error
    db.rollback()
    raise
finally:
    db.close()
```

### How do I load environment variables?
```python
from backend.utils.config import settings

print(settings.DATABASE_URL)  # From .env.local
print(settings.JWT_SECRET)   # From .env.local
print(settings.K_ANONYMITY_THRESHOLD)  # Default: 5
```

---

## 🧪 TESTING QUICKSTART

### Run one test file
```bash
python -m pytest tests/test_anonymisation.py -v
```

### Run one test class
```bash
python -m pytest tests/test_anonymisation.py::TestPseudonymisation -v
```

### Run one test method
```bash
python -m pytest tests/test_anonymisation.py::TestPseudonymisation::test_determinism -v
```

### Run with coverage
```bash
python -m pytest tests/ --cov=backend --cov-report=html
```

### Run in watch mode (requires pytest-watch)
```bash
ptw tests/
```

---

## 🐛 DEBUGGING TIPS

### Enable SQL logging
```python
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Now all SQL queries are printed
```

### Debug a query
```python
query = db.query(Patient).filter(Patient.age > 30)
print(query)  # Shows SQL before executing
print(query.all())  # Executes and shows results
```

### Check what's in a record
```python
patient = db.query(Patient).first()
print(patient.__dict__)  # All fields as dict
```

### Test an endpoint locally
```bash
curl http://localhost:8000/health
curl -H "Authorization: Bearer TOKEN" http://localhost:8000/api/v1/patients/me
```

---

## 📚 DOCUMENTATION MAP

| Document | Purpose | Audience |
|----------|---------|----------|
| `CODEBASE_AUDIT.md` | Complete system understanding | All developers |
| `TEAM_SYNC_MAP.md` | Who owns what, blockers, timeline | Project managers, all devs |
| `WEEK2_TASK_BREAKDOWN.md` | Exact tasks for privacy module | Saugata, backend team |
| `COMPLETE_PROJECT_SYNC_GUIDE.md` | Architecture, integration | New developers |
| `README.md` | Quick start, high-level overview | Everyone |
| `DPDP_COMPLIANCE.md` | Privacy/compliance details | Saugata, PI |
| `PII_FIELD_MAP.md` | Field classifications | Everyone |

---

## 🆘 IF SOMETHING BREAKS

1. **Backend won't start**
   - Check: DATABASE_URL in .env.local
   - Check: PostgreSQL/SQLite running
   - Check: `uvicorn backend.api.main:app --reload`

2. **Database query fails**
   - Check: backend/database/session.py (connection)
   - Check: backend/database/models.py (table definition)
   - Check: SQL syntax in query

3. **Authentication fails**
   - Check: backend/api/middleware.py (token creation)
   - Check: JWT_SECRET in .env.local
   - Check: Token format in request header

4. **Tests failing**
   - Check: conftest.py (test fixtures)
   - Check: test database exists
   - Check: import paths correct

5. **Endpoint returns wrong response**
   - Check: backend/utils/response.py (response format)
   - Check: endpoint returns `response.success_response(...)`

---

**Last Updated:** May 25, 2026  
**Maintained By:** Development Team  
**Use This To:** Navigate the codebase efficiently without reading all 10,000+ lines

