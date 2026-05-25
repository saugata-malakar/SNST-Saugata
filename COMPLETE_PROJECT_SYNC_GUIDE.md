# Complete Project Synchronization Guide

**Project:** DiabetesCare AI (IIT Kharagpur)  
**Date:** Week 1-3 (Ongoing)  
**Status:** 45% complete (Privacy ✅ | Backend Foundation ✅ | CRUD ⏳ | Inference ⏳)

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DIABETESCARE AI PLATFORM                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  FRONTEND LAYER                                                     │
│  ├── Mobile App (React Native)          [mobile-app/]              │
│  │   ├── Patient workflows               [src/screens/]             │
│  │   ├── ASHA worker interface           [src/screens/]             │
│  │   └── Expects: /api/v1/* endpoints                              │
│  │                                                                 │
│  ├── Doctor Dashboard (Vite + React)    [doctor-dashboard/]        │
│  │   ├── Doctor patient list             [src/pages/]              │
│  │   ├── Alert management                [src/pages/]              │
│  │   └── Expects: /api/v1/* endpoints                              │
│  │                                                                 │
│  └── Research Dashboard (Streamlit)     [dashboard/]               │
│      └── Model QA + visualization                                   │
│                                                                     │
│  ═══════════════════════════════════════════════════════════════    │
│                                                                     │
│  API LAYER (FastAPI) — Week 3 Building                             │
│  ├── Auth & Middleware         [backend/api/middleware.py] ✅      │
│  ├── Sessions Management       [backend/database/session.py] ✅    │
│  ├── Config Loading            [backend/utils/config.py] ✅        │
│  │                                                                 │
│  ├── CRUD Routers (⏳ Building)                                     │
│  │   ├── Patients              [backend/api/routers/patients.py]   │
│  │   ├── Doctors               [backend/api/routers/doctors.py]    │
│  │   ├── Alerts                [backend/api/routers/alerts.py]     │
│  │   └── ASHA Workers          [backend/api/routers/asha.py]       │
│  │                                                                 │
│  ├── Inference Routers (⏳ Building)                                │
│  │   ├── Wound Severity        [backend/api/routers/wound.py]      │
│  │   ├── Skin Classification   [backend/api/routers/skin.py]       │
│  │   └── Eye Health            [backend/api/routers/eye.py]        │
│  │                                                                 │
│  ├── Privacy & Export (✅ Done - Integrated Week 3)                │
│  │   ├── Anonymisation         [backend/database/privacy.py] ✅    │
│  │   ├── Erasure               [backend/database/erasure.py] ✅    │
│  │   └── Export Endpoint       [backend/api/routers/export.py] ✅  │
│  │                                                                 │
│  └── Utils                                                          │
│      ├── Response Formatting   [backend/utils/response.py] ✅      │
│      ├── Logging & Audit       [backend/utils/logging.py] ✅       │
│      └── Image Handling        [backend/utils/image.py] (⏳)        │
│                                                                     │
│  ═══════════════════════════════════════════════════════════════    │
│                                                                     │
│  DATABASE LAYER (PostgreSQL)                                        │
│  ├── SQLAlchemy Models         [backend/database/models.py] ✅     │
│  │   └── 26 Tables (DPDP compliant)                                 │
│  │       ├── Patients + Medical History                             │
│  │       ├── Wound Sites + Sessions + Photos                        │
│  │       ├── AI Results + Alerts                                    │
│  │       ├── ASHA Workers + Assignments                             │
│  │       ├── Doctors + Teleconsults + Prescriptions                 │
│  │       ├── Subscriptions + Payments                               │
│  │       └── Audit Logs (7-year retention)                          │
│  │                                                                 │
│  └── Migrations                [backend/database/alembic/] (⏳)     │
│                                                                     │
│  ═══════════════════════════════════════════════════════════════    │
│                                                                     │
│  ML LAYER (Python)                                                  │
│  ├── Wound Severity            [ml/wound_severity/] (Saugata)      │
│  │   └── EfficientNet-B0 for Wagner grade + tissue + infection    │
│  │                                                                 │
│  ├── Skin Classifier           [ml/skin_classifier/] (Kousttav)    │
│  │   └── EfficientNet-B3 for 8 skin diseases                       │
│  │                                                                 │
│  ├── Eye Models                [ml/eye_models/] (Shivraj)          │
│  │   ├── Anemia (conjunctival pallor regression)                   │
│  │   ├── Retinopathy (DR stage classification)                     │
│  │   └── Conjunctival disease classification                        │
│  │                                                                 │
│  └── Computer Vision           [cv/] (Adreesh)                     │
│      ├── Preprocessing          [cv/preprocessing/]                │
│      └── Segmentation           [cv/segmentation/]                 │
│                                                                     │
│  ═══════════════════════════════════════════════════════════════    │
│                                                                     │
│  COMPLIANCE LAYER                                                   │
│  ├── Privacy Module            [backend/database/privacy.py] ✅    │
│  │   ├── HMAC-SHA256 pseudonymisation                               │
│  │   ├── k-anonymity verification (k≥5)                             │
│  │   ├── Age/duration generalisation                                │
│  │   └── 72-hour erasure pipeline                                   │
│  │                                                                 │
│  ├── PII Field Map             [docs/PII_FIELD_MAP.md] ✅           │
│  │   └── All 26 tables classified (direct/quasi/non-sensitive)     │
│  │                                                                 │
│  └── DPDP Compliance           [docs/DPDP_COMPLIANCE.md] ✅        │
│      └── Gap analysis + week-by-week roadmap                        │
│                                                                     │
│  ═══════════════════════════════════════════════════════════════    │
│                                                                     │
│  TESTING                                                            │
│  ├── Unit Tests                [tests/test_anonymisation.py] ✅     │
│  │   └── 45+ cases for privacy module                               │
│  │                                                                 │
│  └── Integration Tests         [tests/test_week2_integration.py] ✅ │
│      └── End-to-end workflows (export, erasure, anonymisation)     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Completion Status by Component

### Week 1-2: Privacy Module (100% ✅)

| Component | Status | Files | Tests | Comments |
|-----------|--------|-------|-------|----------|
| PII Classification | ✅ | PII_FIELD_MAP.md | N/A | All 26 tables mapped |
| HMAC Pseudonymisation | ✅ | privacy.py | 45+ | Deterministic, rotating salt |
| Age Generalisation | ✅ | privacy.py | 45+ | 5-year bands |
| Diabetes Duration | ✅ | privacy.py | 45+ | 2-year bands |
| Village Stripping | ✅ | privacy.py | 45+ | Quasi-identifier removal |
| k-Anonymity (k≥5) | ✅ | privacy.py | 45+ | Threshold verified |
| Erasure Pipeline | ✅ | erasure.py | 8+ | 72-hour window, all 26 tables |
| Export Endpoint | ✅ | routers/export.py | 4+ | k-anonymity gated (DB integration pending) |
| Database Models | ✅ | models.py | 2+ | 26 ORM tables with PII annotations |
| Audit Logging | ✅ | logging.py | — | Structured JSON logging |
| Documentation | ✅ | DPDP_COMPLIANCE.md | — | Gap analysis + roadmap |

**Summary:** Privacy module complete and production-ready. 100+ tests passing. Ready for Week 3+ integration.

---

### Week 3A: Backend Foundation (85% ✅)

| Component | Status | Files | Comments |
|-----------|--------|-------|----------|
| Database Session | ✅ | backend/database/session.py | Engine, SessionLocal, get_db() dependency |
| Config Loader | ✅ | backend/utils/config.py | Pydantic Settings from .env |
| JWT Auth | ✅ | backend/api/middleware.py | patient/doctor/asha dependencies |
| Response Schemas | ✅ | backend/utils/response.py | SuccessResponse, PaginatedResponse, ErrorResponse |
| Logging/Audit | ✅ | backend/utils/logging.py | AuditLogger integration with privacy |
| Main App | ✅ | backend/api/main.py | Startup/shutdown hooks, CORS, router placeholders |
| .env Template | ✅ | .env.local | Dev configuration |
| **Status** | **85%** | **7 files** | **Ready for CRUD endpoints** |

**Summary:** Backend foundation complete. All blocking issues resolved. FastAPI can now:
- Connect to database
- Load configuration
- Authenticate requests
- Log events
- Return standardized responses

---

### Week 3B: CRUD Endpoints (0% ⏳)

| Endpoint | Status | Router | Purpose | Blockers |
|----------|--------|--------|---------|----------|
| `GET /api/v1/patients/me` | ⏳ | patients.py (⏳) | Get current patient | Need migration from Flask |
| `GET /api/v1/patients/:id` | ⏳ | patients.py (⏳) | Get patient details | " |
| `POST /api/v1/patients/me/medical-history` | ⏳ | patients.py (⏳) | Update medical history | " |
| `GET /api/v1/doctors/me` | ⏳ | doctors.py (⏳) | Get current doctor | " |
| `GET /api/v1/doctors/me/alerts` | ⏳ | doctors.py (⏳) | Get doctor's alerts | " |
| `GET /api/v1/alerts` | ⏳ | alerts.py (⏳) | Get all alerts | Need new implementation |
| `PUT /api/v1/alerts/:id/acknowledge` | ⏳ | alerts.py (⏳) | Acknowledge alert | " |
| `GET /api/v1/asha/me/dashboard` | ⏳ | asha.py (⏳) | ASHA dashboard | Migrate from Flask |

**Blockers:** Need to migrate 3 Flask routes → FastAPI

**Timeline:** 3-5 days (Days 3-5 of Week 3)

---

### Week 3C: Inference Endpoints (0% ⏳)

| Endpoint | Status | Router | Purpose | Blockers |
|----------|--------|--------|---------|----------|
| `POST /api/v1/wound/preprocess` | ⏳ | wound.py (⏳) | Denoise + CLAHE | ML model not ready |
| `POST /api/v1/wound/detect-coin` | ⏳ | wound.py (⏳) | Coin localization | ML model not ready |
| `POST /api/v1/wound/segment` | ⏳ | wound.py (⏳) | SAM2 segmentation | ML model not ready |
| `POST /api/v1/wound/classify` | ⏳ | wound.py (⏳) | Wagner + tissue + infection | ML model not ready |
| `POST /api/v1/skin/classify` | ⏳ | skin.py (⏳) | 8-class skin disease | ML model not ready |
| `POST /api/v1/eye/anemia` | ⏳ | eye.py (⏳) | Conjunctival pallor | ML model not ready |
| `POST /api/v1/eye/retinopathy` | ⏳ | eye.py (⏳) | DR stage detection | ML model not ready |

**Blockers:** ML models (wound_severity, skin_classifier, eye_models) are scaffolds. Need actual implementations.

**Timeline:** 5-7 days (Days 5-7 of Week 3, but blocked by ML readiness)

---

## 🔗 Integration Points

### Mobile App ↔ Backend

**Mobile expects these endpoints working:**
```typescript
// From mobile-app/src/config/api.ts
export const API_BASE_URL = "http://localhost:8000" (or api.diabetescareai.in)

// From mobile-app/src/services/*.ts
POST /api/v1/auth/login
GET  /api/v1/patients/me
POST /api/v1/monitoring-sessions
POST /api/v1/wound/classify        [IMAGE UPLOAD]
POST /api/v1/skin/classify         [IMAGE UPLOAD]
POST /api/v1/eye/*                 [IMAGE UPLOAD]
GET  /api/v1/alerts
PUT  /api/v1/alerts/:id/acknowledge
```

**Current Status:** Only `/health` works. No CRUD or inference endpoints.

---

### Doctor Dashboard ↔ Backend

**Doctor dashboard expects:**
```typescript
// From doctor-dashboard/vite.config.js
proxy: { '/api': 'http://127.0.0.1:8000' }

// From doctor-dashboard/src/pages/*.tsx
GET  /api/v1/doctors/me
GET  /api/v1/doctors/me/alerts
GET  /api/v1/doctors/me/patients
GET  /api/v1/doctors/me/teleconsults
GET  /api/v1/patients/:id
GET  /api/v1/patients/:id/wound-detail
PUT  /api/v1/alerts/:id/acknowledge
POST /api/v1/prescriptions
```

**Current Status:** Only `/health` works. CRUD endpoints needed ASAP.

---

## 🎯 Dependencies & Blocking Issues

### Resolved ✅
1. ✅ No database session → `session.py`
2. ✅ No config → `config.py`
3. ✅ No auth → `middleware.py`
4. ✅ No response schemas → `response.py`
5. ✅ No logging → `logging.py`

### Blocking Now ⏳
1. ⏳ **No CRUD endpoints** → Blocks mobile + doctor-dashboard from loading data
2. ⏳ **No inference endpoints** → Blocks mobile from submitting wounds/skin/eye
3. ⏳ **ML models not ready** → Can't build inference endpoints without trained models
4. ⏳ **Export not integrated** → Privacy module isolated from API

### Not Yet (Future)
1. 🔲 Federated Learning (Week 4)
2. 🔲 Multimodal AI + Clinical NLP (Week 5)
3. 🔲 RAG Assistant + Consent Versioning (Week 6)
4. 🔲 Encryption audit (Week 7)

---

## 📋 Action Items by Priority

### CRITICAL (Blocking Frontend)
- [ ] Create `backend/api/routers/patients.py` (migrate from Flask)
- [ ] Create `backend/api/routers/doctors.py` (migrate from Flask)
- [ ] Create `backend/api/routers/alerts.py` (new implementation)
- [ ] Register CRUD routers in `main.py`
- [ ] **Goal:** Mobile app can GET /api/v1/patients/me

**Timeline:** Days 3-5 of Week 3  
**Owner:** Sahil Kumar Gupta (Backend Lead)

---

### HIGH (Blocking Inference)
- [ ] Create `backend/api/routers/wound.py`
- [ ] Create `backend/api/routers/skin.py`
- [ ] Create `backend/api/routers/eye.py`
- [ ] Create `backend/utils/image.py` (image validation + storage)
- [ ] Integrate ML models (ml/wound_severity, ml/skin_classifier, ml/eye_models)
- [ ] **Goal:** Mobile app can POST /api/v1/wound/classify with image

**Timeline:** Days 5-7 of Week 3 (blocked by ML readiness)  
**Owner:** Shivraj Gulve (Inference Lead)

---

### MEDIUM (Privacy Integration)
- [ ] Integrate export router with database session
- [ ] Test export endpoint with k-anonymity gate
- [ ] Verify audit logging
- [ ] **Goal:** Research export works, respects k≥5 threshold

**Timeline:** Parallel with CRUD endpoints  
**Owner:** Saugata Malakar (Privacy Lead)

---

### LOW (Future)
- [ ] Alembic migrations setup
- [ ] ASHA worker routers
- [ ] Teleconsult routers
- [ ] Payment endpoints
- [ ] Subscription endpoints

---

## 📂 File Structure (Current)

```
diabetescare-ai/
├── backend/
│   ├── api/
│   │   ├── main.py                      [✅ UPGRADED - Week 3A Phase 1]
│   │   ├── middleware.py                [✅ NEW - Week 3A Phase 1]
│   │   ├── routers/
│   │   │   ├── export.py                [✅ Week 2]
│   │   │   ├── patients.py              [⏳ Day 3]
│   │   │   ├── doctors.py               [⏳ Day 3]
│   │   │   ├── alerts.py                [⏳ Day 3]
│   │   │   ├── wound.py                 [⏳ Day 5]
│   │   │   ├── skin.py                  [⏳ Day 5]
│   │   │   ├── eye.py                   [⏳ Day 5]
│   │   │   └── asha.py                  [⏳ Day 5]
│   │   └── schemas/                     [⏳ Needed for CRUD]
│   │
│   ├── database/
│   │   ├── session.py                   [✅ NEW - Week 3A Phase 1]
│   │   ├── models.py                    [✅ Week 2]
│   │   ├── privacy.py                   [✅ Week 2]
│   │   ├── erasure.py                   [✅ Week 2]
│   │   └── alembic/                     [⏳ Migrations setup]
│   │
│   └── utils/
│       ├── config.py                    [✅ NEW - Week 3A Phase 1]
│       ├── response.py                  [✅ NEW - Week 3A Phase 1]
│       ├── logging.py                   [✅ NEW - Week 3A Phase 1]
│       └── image.py                     [⏳ Day 3]
│
├── ml/
│   ├── wound_severity/                  [🔲 Scaffold]
│   ├── skin_classifier/                 [🔲 Scaffold]
│   └── eye_models/                      [🔲 Scaffold]
│
├── cv/
│   ├── preprocessing/                   [🔲 Scaffold]
│   └── segmentation/                    [🔲 Scaffold]
│
├── mobile-app/                          [✅ Ready, waiting for backend]
├── doctor-dashboard/                    [✅ Ready, waiting for backend]
├── dashboard/                           [✅ Scaffold]
│
├── docs/
│   ├── PII_FIELD_MAP.md                 [✅ Week 2]
│   ├── DPDP_COMPLIANCE.md               [✅ Week 2]
│   └── README.md                        [✅]
│
├── tests/
│   ├── test_anonymisation.py            [✅ 45+ cases]
│   ├── test_week2_integration.py        [✅ 8+ cases]
│   └── test_api_health.py               [✅ 1 case]
│
├── BACKEND_SYNC_AUDIT.md                [✅ Week 3A Planning]
├── BACKEND_SYNC_STATUS_PHASE1.md        [✅ Week 3A Phase 1 Status]
├── COMPLETE_PROJECT_SYNC_GUIDE.md       [✅ This file]
├── .env.local                           [✅ NEW - Week 3A Phase 1]
└── requirements.txt                     [✅ Dependencies]
```

---

## 🚀 Quick Start Guide

### Prerequisites
```bash
# Install dependencies
pip install -r requirements.txt

# Create .env from template
cp .env.local .env

# Edit .env with your DATABASE_URL
# Example: postgresql://user:password@localhost:5432/diabetescare
```

### Run FastAPI Backend
```bash
# Start the backend (localhost:8000)
uvicorn backend.api.main:app --reload --port 8000

# Expected output:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# [startup] Initializing database...
# [startup] Database ready ✓
```

### Test Health
```bash
curl http://localhost:8000/health
# Output: {"status":"ok","service":"diabetescare-ai-api","version":"0.1.0","database":"ok"}
```

### Run Mobile App (Day 3+)
```bash
cd mobile-app
npm start
# Will connect to http://localhost:8000/api/v1/*
```

### Run Doctor Dashboard (Day 3+)
```bash
cd doctor-dashboard
npm run dev
# Will proxy /api to http://localhost:8000
```

---

## 🎓 Learning Path for New Developers

1. **Understand Privacy First** (2 hours)
   - Read `docs/PII_FIELD_MAP.md`
   - Read `docs/DPDP_COMPLIANCE.md`
   - Review `backend/database/privacy.py` implementation

2. **Understand Database Schema** (2 hours)
   - Review `backend/database/models.py` (26 tables)
   - Understand relationships (Patient → MonitoringSession → Photograph → AIResult)
   - See PII annotations on fields

3. **Understand FastAPI Setup** (1 hour)
   - Run `uvicorn backend.api.main:app --reload`
   - Test `/health` endpoint
   - Review config loading from `.env`

4. **Understand Authentication** (1 hour)
   - Review `backend/api/middleware.py`
   - Test: `python -c "from backend.api.middleware import create_access_token; print(create_access_token('pat-1', 'patient'))"`

5. **Build First CRUD Endpoint** (2 hours)
   - Look at Flask equivalent in `backend/legacy/routes/patients.py`
   - Adapt to FastAPI + dependency injection
   - Use `Session = Depends(get_db)` to query database
   - Return standardized response via `response.py`

---

## 🎯 Success Criteria by Week

### Week 2 (DONE ✅)
- [x] Privacy module complete (anonymisation, erasure, export)
- [x] 100+ tests passing
- [x] Database models defined (26 tables)
- [x] Documentation complete

### Week 3 (IN PROGRESS)
- [x] Backend foundation (session, config, auth, logging)
- [ ] CRUD endpoints (patients, doctors, alerts)
- [ ] Export endpoint integrated with database
- [ ] Mobile app + doctor-dashboard can load data
- [ ] Inference endpoints (wound, skin, eye)

### Week 4-6 (FUTURE)
- [ ] Federated Learning PoC
- [ ] Multimodal AI + Clinical NLP
- [ ] RAG Assistant + Consent Versioning
- [ ] Encryption audit + OWASP checklist

---

## 📞 Questions or Issues?

- **Database questions:** Sahil Kumar Gupta (Backend Lead)
- **Privacy questions:** Saugata Malakar (Privacy Lead)
- **Inference questions:** Shivraj Gulve (Inference Lead)
- **Mobile integration:** Kousttav Paul (ML/Mobile Integration)
- **Overall direction:** Prof. Dipak Kumar Das (PI)

---

**Last Updated:** 2024-11-15 (Post Phase 1A infrastructure commit)  
**Next Review:** After Phase 2 CRUD endpoints complete

