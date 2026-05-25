# DiabetesCare AI — Team Synchronization Map

**Purpose:** Understand who is working on what, when, and how their work connects.  
**Date:** May 25, 2026  
**Team Size:** 5 developers + 1 PI

---

## 🧭 TEAM MEMBERS & RESPONSIBILITIES

### 1. **Sahil Kumar Gupta** — Backend Infrastructure Lead
**Focus:** FastAPI migration, database connection, API routes

**Week Deliverables:**
- Week 3A Phase 1: ✅ COMPLETE
  - Database session (SQLAlchemy engine, SessionLocal, get_db())
  - Configuration system (Pydantic Settings from .env)
  - JWT authentication (4 dependency types)
  - Response schemas (SuccessResponse, ErrorResponse, PaginatedResponse)
  - Enhanced FastAPI main app with startup/shutdown hooks
  - Health endpoint with database status check

- Week 3A Phase 2: ⏳ IN PROGRESS
  - CRUD routers: patients.py, doctors.py, alerts.py
  - Expected by: End of Week 3 (Days 3-5)
  - Migrating from `backend/legacy/routes/*.py`

- Week 3B Phase 3: ⏳ PLANNED
  - Inference routers: wound.py, skin.py, eye.py
  - Teleconsult routers: consultations.py, sessions.py
  - Expected by: Week 3B Days 5-7

**Current Code Locations:**
```
backend/api/main.py ...................... Enhanced FastAPI factory
backend/database/session.py .............. Database connection
backend/utils/config.py .................. Environment configuration
backend/api/middleware.py ................ JWT authentication + dependencies
backend/utils/response.py ................ Response schemas
backend/utils/logging.py ................. Structured audit logging
.env.local ............................. Development configuration
```

**Blocks:** ⏳ Waiting for Saugata's Week 2 anonymisation module before building export router integration  
**Blocked By:** None — Phase 1 ✅ complete

**Dependencies:**
- Uses Saugata's models.py (26 SQLAlchemy tables)
- Awaits Saugata's privacy.py (anonymisation engine) before integrating export endpoint
- Coordinates with Shivraj on ML model inference endpoint signatures

---

### 2. **Saugata Malakar** — Privacy + Wound ML Lead
**Focus:** Anonymisation implementation, k-anonymity verification, erasure pipeline, wound model

**Week 1 Deliverables:** ✅ COMPLETE
- ✅ PII Field Map (Excel sheet with all 26 tables classified)
- ✅ DPDP Gap Analysis (10 compliance gaps mapped to Act sections)
- ✅ Architecture design doc (pseudonymisation flows, k-anon logic, erasure order)

**Week 2 Deliverables:** ⏳ IN PROGRESS
- **PRIORITY 1:** Build `backend/database/privacy.py` (anonymisation engine)
  - HMAC-SHA256 pseudonymisation with 90-day rotating salt
  - Age generalization (age → "30-34" bands)
  - Diabetes duration generalization (years → "2-3 years" bands)
  - Village stripping (quasi-identifier removal)
  - k-anonymity verification (k ≥ 5 threshold with group report)
  - Data export pipeline
  - Status: **🔴 BLOCKED** — Waiting for database schema confirmation

- **PRIORITY 2:** Build `backend/database/erasure.py` (72-hour deletion pipeline)
  - Request creation (72-hour pending window)
  - Cascade deletion across all 26 tables respecting foreign keys
  - Verification that all patient records deleted
  - Audit logging
  - Status: **🔴 BLOCKED** — Depends on privacy.py completion

- **PRIORITY 3:** Wound severity model training & integration
  - EfficientNet-B0 trained on wound images
  - Wagner severity scoring (0-4 levels)
  - Inference endpoint ready for integration with Sahil's wound.py router
  - Status: **🔴 BLOCKED** — Awaits ML training resources

**Current Code Locations:**
```
backend/database/privacy.py .............. Anonymisation engine (PRIORITY 1 - PENDING)
backend/database/erasure.py ............. Erasure pipeline (PRIORITY 2 - PENDING)
ml/wound_severity/ ...................... Wound model (PRIORITY 3 - BLOCKED)
tests/test_anonymisation.py ............. 100+ tests for privacy module
```

**Critical Blockers:**
- 🔴 **DATABASE SCHEMA VERIFICATION** — Needs real schema from PostgreSQL (or migration files)
  - Currently using inferred schema from Week 1 analysis
  - Must confirm actual column names, data types, relationships
  - Once confirmed → can build privacy.py with exact field mappings

- 🔴 **HMAC SECRET KEY MANAGEMENT** — Needs policy decision
  - Where to store rotating salt for 90-day epochs?
  - KMS integration with Google Cloud?
  - Stored in database table with audit trail?

**Blocks:** 
- Blocks Sahil from integrating export endpoint (needs privacy.py complete)
- Blocks all data export functionality
- Blocks compliance verification (DPDP Act Section 8 right to erasure untested)

**Expected Completion:**
- privacy.py: 2-3 days once schema confirmed
- erasure.py: 1-2 days after privacy.py
- Wound model: Depends on training data availability (external blocker)

**Status:** ⏳ WAITING for schema confirmation from repo/database access

---

### 3. **Adreesh Mitra** — Computer Vision (Preprocessing Lead)
**Focus:** Image normalization, coin detection, segmentation

**Week Deliverables:** ⏳ PENDING
- Coin detection pipeline (reference marker for scale)
- SAM2 segmentation (wound region extraction)
- Image normalization (lighting, angle correction)
- Status: **🔴 BLOCKED** — Scaffolds exist, implementation pending

**Current Code Locations:**
```
cv/preprocessing/coin_detection.py ....... Coin detection (stub)
cv/segmentation/ ......................... SAM2 integration (stub)
cv/tests/ ............................... CV tests (partial)
```

**Dependencies:**
- Awaits Saugata's wound severity model for training data
- Coordinates with Shivraj on preprocessing pipeline integration

**Blocks:** Blocks Shivraj from finalizing inference pipeline

**Expected Completion:** Week 3B-4 (depends on GPU resources)

**Status:** ⏳ PENDING implementation

---

### 4. **Kousttav Paul** — Skin Classifier Lead
**Focus:** EfficientNet-B3 skin disease classification

**Week Deliverables:** ⏳ PENDING
- Skin disease classifier (8 categories with leprosy ×5 weight)
- Training on MIMIC/proprietary dataset
- Inference endpoint ready for Sahil's skin.py router
- Status: **🔴 BLOCKED** — Model training pending

**Current Code Locations:**
```
ml/skin_classifier/ ...................... Model (stub/training)
```

**Dependencies:**
- Awaits GPU/training resources
- Provides inference for Sahil's skin.py router

**Blocks:** Blocks Sahil from completing skin inference endpoint

**Expected Completion:** Week 4-5 (depends on training time)

**Status:** ⏳ PENDING training

---

### 5. **Shivraj Gulve** — Eye Models + Deployment Lead
**Focus:** 3 eye disease models, ML ops, containerization

**Week Deliverables:** ⏳ PENDING
- Pallor detection (regression model)
- Diabetic retinopathy classification
- Conjunctival disease classification
- Model ensemble & inference optimization
- Docker containerization for deployment
- Status: **🔴 BLOCKED** — Model training pending

**Current Code Locations:**
```
ml/eye_models/
  - 3a_pallor_regression/ ............... Pallor model (stub)
  - 3b_dr_classification/ .............. DR model (stub)
  - 3c_conjunctival/ ................... Conjunctival model (stub)
deployment/ ............................ Docker setup (pending)
```

**Dependencies:**
- Awaits training resources
- Coordinates with Adreesh on preprocessing pipeline
- Provides inference for Sahil's eye.py router

**Blocks:** Blocks inference endpoints

**Expected Completion:** Week 4-5 (depends on training time)

**Status:** ⏳ PENDING training

---

### 6. **Prof. Dipak Kumar Das** — Project Lead (PI)
**Focus:** Architecture decisions, compliance review, phase sign-offs

**Key Reviews:**
- ✅ Week 1: PII Field Map + Gap Analysis (APPROVED)
- ✅ Week 2: Privacy module architecture (APPROVED)
- ⏳ Week 3: CRUD routers + export integration (AWAITING SUBMISSION)
- ⏳ Week 3B: Inference endpoints (AWAITING)
- ⏳ Week 4+: Federated learning, consent versioning, RAG assistant (PLANNED)

**Critical Decisions Needed:**
1. **Database Location Policy** (G-02 from DPDP Gap Analysis)
   - Must confirm: Asia-South1 (India) or other?
   - Required for compliance documentation

2. **HMAC Secret Key Management** (G-09)
   - Where to store rotating salt for pseudonymisation?
   - KMS setup needed?

3. **Telecom Gateway Approval** (G-04)
   - SMS/WhatsApp integration for alerts
   - Vendor selection pending

4. **Federated Learning Consent** (Week 4+)
   - Patient consent model for FL training
   - Data contribution incentives?

**Blocks:** Critical compliance decisions needed from PI before privacy.py implementation can finalize

**Status:** ✅ Responsive, reviews within 1-2 days

---

## 🔗 WORK DEPENDENCY GRAPH

```
Week 1 (COMPLETE)
└─ PII Field Map ✅
   └─ DPDP Gap Analysis ✅

Week 2 (CURRENT)
├─ Saugata: Privacy Module (BLOCKED ON SCHEMA)
│  ├─ HMAC Pseudonymisation ⏳
│  ├─ k-Anonymity Verification ⏳
│  └─ Erasure Pipeline ⏳
│     └─ BLOCKS: Sahil's export router integration ⏳
│
├─ Kousttav: Skin Classifier Training ⏳
│  └─ BLOCKS: Sahil's skin.py router ⏳
│
└─ Shivraj: Eye Models Training ⏳
   └─ BLOCKS: Sahil's eye.py router ⏳

Week 3A (CURRENT)
├─ Phase 1: Sahil ✅ COMPLETE
│  ├─ Database session ✅
│  ├─ Config system ✅
│  ├─ JWT auth ✅
│  ├─ Response schemas ✅
│  └─ Main app ✅
│
└─ Phase 2-3: (BLOCKED ON SAUGATA & ML)
   ├─ CRUD routers (Sahil) ⏳ CAN START (no blocker)
   ├─ Export integration (Sahil) ⏳ BLOCKED on Saugata's privacy.py
   ├─ Wound router (Sahil) ⏳ BLOCKED on Saugata's wound model
   ├─ Skin router (Sahil) ⏳ BLOCKED on Kousttav's skin model
   └─ Eye router (Sahil) ⏳ BLOCKED on Shivraj's eye models

Week 3B+ (PLANNED)
├─ Inference optimization (Shivraj) ⏳
├─ CV preprocessing (Adreesh) ⏳
├─ Federated learning (Saugata) ⏳
├─ Consent versioning (TBD) ⏳
├─ RAG assistant (TBD) ⏳
└─ Teleconsult scheduling (Sahil) ⏳
```

---

## 📋 CRITICAL PATH (What Must Happen Next)

### IMMEDIATE (This Week)

1. **Saugata: Get Real Database Schema**
   - Source: Migration files OR PostgreSQL database
   - Task: Share with Saugata ASAP
   - Impact: Unblocks privacy.py implementation
   - Time: ~1 hour of research

2. **Saugata: Finalize HMAC Key Management Policy**
   - Consult with Prof. Das on KMS integration
   - Decision: Cloud KMS vs database-stored vs .env
   - Impact: Unblocks HMAC-SHA256 implementation
   - Time: ~30 min discussion

3. **Sahil: Start CRUD Router Migration**
   - Can start immediately (no blocker)
   - Migrate: backend/legacy/routes/patients.py → backend/api/routers/patients.py
   - Use Session = Depends(get_db), return standardized responses
   - Timeline: 3-5 days
   - Output: patients, doctors, alerts routers ready

### WITHIN THIS WEEK

4. **Saugata: Build privacy.py (2-3 days)**
   - Once schema confirmed, implement anonymisation engine
   - HMAC-SHA256 + rotating salt
   - Age/duration generalization
   - k-anonymity verification
   - Unit tests (100+)

5. **Saugata: Build erasure.py (1-2 days)**
   - 72-hour deletion pipeline
   - Cascade delete across 26 tables
   - Audit logging
   - Integration tests

### END OF WEEK

6. **Sahil: Export Router Integration (1 day)**
   - Once privacy.py complete, integrate with database session
   - Query actual records, apply anonymisation
   - Verify k-anonymity before exporting
   - Return standardized response with verification report

7. **Sahil: Register All Routers in main.py**
   - CRUD routers (patients, doctors, alerts)
   - Export router (with privacy module integration)
   - Test health endpoint still responds

---

## 🚨 KNOWN BLOCKERS

| Blocker | Affected Team | Impact | Solution | Timeline |
|---------|---------------|--------|----------|----------|
| **No real DB schema** | Saugata | Can't implement privacy.py | Share migration files/schema | TODAY |
| **HMAC key policy** | Saugata | Can't implement rotating salt | PI decision on KMS setup | TODAY |
| **ML training resources** | Kousttav, Shivraj, Adreesh | Can't train models | Allocate GPU/TPU | This week |
| **Inference endpoint signatures** | Sahil + ML team | Can't integrate inference | Agree on request/response format | TODAY |
| **Telecom vendor** | Future (SMS alerts) | Can't deploy alerts to field | Select SMS/WhatsApp provider | Week 4 |
| **Federated learning infrastructure** | Saugata | Can't start FL | Set up flower server | Week 4 |

---

## 📞 HOW TO ESCALATE

**Quick Questions:**
- Backend architecture: Ask Sahil (synchronous response ~2hrs)
- Privacy implementation: Ask Saugata (responds in 1 hr)
- ML model format: Ask Shivraj (responds in 3 hrs)
- CV pipeline: Ask Adreesh (responds in 4 hrs)

**Blockers (needs PI decision):**
- DPDP compliance questions → Email Prof. Das (24-48 hr response)
- Resource allocation (GPU, storage) → Email Prof. Das
- Vendor selection (SMS, KMS) → Email Prof. Das

**GitHub Issues:**
- Create issue for each blocker
- Tag relevant person
- Use labels: `blocker`, `waiting-decision`, `research`, `implementation`

---

## 📊 PROGRESS TRACKING

### Completion Status by Week

| Week | Component | Status | Owner | EOW Target |
|------|-----------|--------|-------|-----------|
| **Week 1** | PII Field Map | ✅ 100% | Saugata | ✅ Done |
| **Week 1** | DPDP Gap Analysis | ✅ 100% | Saugata | ✅ Done |
| **Week 1** | Architecture Design | ✅ 100% | Saugata | ✅ Done |
| **Week 2** | privacy.py (HMAC + k-anon) | ⏳ 0% | Saugata | ⏳ BLOCKED |
| **Week 2** | erasure.py (deletion pipeline) | ⏳ 0% | Saugata | ⏳ BLOCKED |
| **Week 2** | Skin classifier training | ⏳ 10% | Kousttav | ⏳ TBD |
| **Week 2** | Eye models training | ⏳ 10% | Shivraj | ⏳ TBD |
| **Week 3A Phase 1** | Backend foundation | ✅ 100% | Sahil | ✅ Done |
| **Week 3A Phase 2** | CRUD routers | ⏳ 0% | Sahil | ⏳ 80% EOW |
| **Week 3A Phase 2** | Export integration | ⏳ 0% | Sahil | ⏳ BLOCKED on Saugata |
| **Week 3A Phase 3** | Inference routers | ⏳ 0% | Sahil | ⏳ BLOCKED on ML |

---

## 🎯 THIS WEEK'S ACTION ITEMS

### For Saugata (CRITICAL PATH)
- [ ] Day 1: Get real database schema from repo/migrations
- [ ] Day 1: Discuss HMAC key management with Prof. Das
- [ ] Day 2-4: Implement privacy.py with unit tests
- [ ] Day 5: Implement erasure.py with integration tests
- [ ] Day 5: Submit both to Sahil for export router integration

### For Sahil (PARALLEL TRACK)
- [ ] Day 1-2: Migrate patients.py from Flask
- [ ] Day 2-3: Migrate doctors.py from Flask
- [ ] Day 3: Create alerts.py router
- [ ] Day 4: Register all routers in main.py
- [ ] Day 5: Wait for Saugata → integrate export with privacy.py

### For Kousttav & Shivraj (ML TRAINING)
- [ ] Day 1: Confirm GPU/TPU availability with Prof. Das
- [ ] Day 1-5: Begin model training (in parallel)
- [ ] End of week: Report training progress

### For Adreesh (CV PREPROCESSING)
- [ ] Day 1: Set up SAM2 environment
- [ ] Day 1-5: Implement coin detection pipeline

### For Prof. Das (PI DECISIONS)
- [ ] Day 1: Confirm database location policy (Asia-South1)
- [ ] Day 1: Approve HMAC key management approach
- [ ] Day 1: Allocate GPU/TPU for ML training
- [ ] Day 5: Review privacy.py + erasure.py implementations

---

## 📝 NOTES

- **Saugata is the critical path.** Privacy.py blocks export functionality. Once Saugata delivers, Sahil can integrate export + finalize routers.
- **ML training is independent.** Kousttav and Shivraj can train in parallel without blocking Saugata/Sahil.
- **Adreesh's CV work is research-phase.** Can be done in parallel, not blocking any routers.
- **Mobile app is waiting.** React Native client is ready; just waiting for `/api/v1/*` endpoints to be live.
- **Doctor dashboard is waiting.** React Vite dashboard ready; waiting for alert endpoints + inference results.

---

**Last Updated:** May 25, 2026  
**Next Sync:** Daily standup with Sahil and Saugata on privacy.py progress

