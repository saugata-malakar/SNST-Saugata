# Week 2 Critical Tasks — Privacy Module Implementation

**Document Purpose:** Exact tasks for Saugata to implement anonymisation + erasure + export  
**Week:** Week 2 (Focus: Get PII mappings → privacy.py → erasure.py)  
**Status:** ⏳ BLOCKED on schema confirmation, READY to execute once confirmed  
**Owner:** Saugata Malakar

---

## 🚨 CRITICAL BLOCKERS (Must Resolve TODAY)

### Blocker 1: Real Database Schema
**Status:** ⏳ NEED THIS FIRST  
**Reason:** Privacy module depends on exact column names, data types, and relationships

**What's Needed:**
Option A: PostgreSQL Migration Files
```bash
# If you have repo/database access, get the schema:
cd backend/legacy/migrations
cat 001_full_schema.sql  # Or similar
```

Option B: Share Column Names
Just tell Saugata the actual columns for each table. Example for patients table:
```
patients:
  - patient_id (UUID, PK)
  - name (VARCHAR, not indexed, DIRECT_ID)
  - phone (VARCHAR, DIRECT_ID)
  - age (INT, QUASI_ID)
  - gender (VARCHAR, QUASI_ID)
  - village (VARCHAR, QUASI_ID)
  - district (VARCHAR, QUASI_ID)
  - aadhar_id (VARCHAR, DIRECT_ID)
  - consent_given_at (TIMESTAMP, QUASI_ID)
  - created_at, updated_at (TIMESTAMP, NS)
  - [other columns?]
```

**Action:** Share the 001_full_schema.sql file or migration files with Saugata **TODAY**

---

### Blocker 2: HMAC Secret Key Storage Policy
**Status:** ⏳ PI DECISION NEEDED  
**Reason:** Determines where rotating salt lives and how to rotate it every 90 days

**Three Options (choose one):**

#### Option A: Google Cloud KMS (Recommended for Production)
```
- HMAC secret stored in: Google Cloud Secret Manager
- Rotation: Automatic 90-day rotation via Secret Manager
- Cost: ~$1/secret/month
- Code in privacy.py:
    from google.cloud import secretmanager
    def get_hmac_secret():
        client = secretmanager.SecretManagerServiceClient()
        secret = client.access_secret_version(
            request={"name": f"projects/PROJECT_ID/secrets/hmac-rotating-salt/versions/latest"}
        )
        return secret.payload.data

- Pro: Secure, audited, compliant
- Con: Requires GCP setup, adds latency (100ms)
```

#### Option B: Environment Variable (Dev Only)
```
- HMAC secret stored in: .env or Docker secret
- Rotation: Manual, every 90 days update .env
- Code in privacy.py:
    HMAC_SECRET = os.getenv("HMAC_SECRET")
    HMAC_SALT_EPOCH = int(os.getenv("HMAC_SALT_EPOCH", "1"))  # Increment on rotation
    
- Pro: Simple, no external dependencies
- Con: Not secure for production, manual rotation
```

#### Option C: Database Table (Hybrid)
```
- HMAC secret stored in: PostgreSQL hmac_secrets table
- Rotation: Script runs every 90 days, creates new row
- Code in privacy.py:
    def get_current_hmac_secret():
        secret = db.query(HmacSecret)\
            .filter(HmacSecret.epoch == CURRENT_EPOCH)\
            .first()
        return secret.secret_key
    
- Pro: Audit trail visible, flexible
- Con: Circular dependency (need to encrypt secret to store it)
```

**Action:** Discuss with Prof. Das and choose. Recommend **Option A for production, Option B for dev**.

---

### Blocker 3: Inference Endpoint Signatures
**Status:** ⏳ NEED TO AGREE  
**Reason:** ML models (wound, skin, eye) need consistent request/response format

**Example Format for Wound Inference:**
```python
# Request to /api/v1/wound/classify
{
    "image_url": "s3://bucket/wound-12345.jpg",
    "patient_id": "pat-uuid-123",
    "wound_site": "left_foot",
    "previous_severity": 2  # If available, for tracking
}

# Response from /api/v1/wound/classify
{
    "status": "success",
    "data": {
        "wound_id": "wound-uuid-456",
        "severity": 3,  # Wagner 0-4
        "severity_label": "moderate",
        "confidence": 0.94,
        "recommendation": "Refer to specialist",
        "processing_time_ms": 245,
        "model_version": "wound_v1.0"
    },
    "audit": {
        "model_id": "wound-efficientnet-b0",
        "inference_timestamp": "2026-05-25T10:30:00Z",
        "image_hash": "sha256:abcd1234...",
        "model_confidence": 0.94
    }
}
```

**Action:** Share with Shivraj + Kousttav. Get agreement on format **TODAY**.

---

## ✅ WEEK 2 TASK BREAKDOWN

Once blockers are resolved, Saugata's work follows this sequence:

### TASK 1: Build `backend/database/privacy.py` (2-3 days)

**File Location:** `backend/database/privacy.py`  
**Dependencies:** Real schema (Blocker 1), HMAC policy (Blocker 2)  
**Tests:** 100+ unit tests (existing test suite template)

#### 1.1: Implement RotatingSaltManager
```python
# Pseudocode (exact code in privacy.py)

class RotatingSaltManager:
    """Manages HMAC salt rotation every 90 days"""
    
    ROTATION_INTERVAL_DAYS = 90
    
    @staticmethod
    def get_current_epoch():
        """Returns which 90-day epoch we're in"""
        # Epoch 0 = Jan 1, 2026
        # Epoch 1 = Apr 1, 2026 (90 days later)
        # Epoch 2 = Jul 1, 2026 (180 days later)
        start_date = datetime(2026, 1, 1)
        days_since_start = (datetime.now() - start_date).days
        return days_since_start // RotatingSaltManager.ROTATION_INTERVAL_DAYS
    
    @staticmethod
    def get_rotating_salt(epoch=None):
        """Get HMAC salt for given epoch (or current)"""
        if epoch is None:
            epoch = RotatingSaltManager.get_current_epoch()
        
        # If using Google Cloud KMS (Option A):
        secret = get_secret_from_kms()
        # If using .env (Option B):
        secret = os.getenv("HMAC_SECRET")
        # If using database (Option C):
        secret = db.query(HmacSecret).filter_by(epoch=epoch).first().secret_key
        
        # Append epoch to ensure different salt per epoch
        return f"{secret}:{epoch}".encode()
```

**Deliverable:** RotatingSaltManager class with tests

#### 1.2: Implement AnonymisationEngine.pseudonymise_id()
```python
class AnonymisationEngine:
    """Handles pseudonymisation for direct identifiers"""
    
    @staticmethod
    def pseudonymise_id(identifier: str, id_type: str) -> str:
        """
        Pseudonymise any identifier (patient_id, name, phone, etc.)
        
        Args:
            identifier: "Saugata Malakar" or "pat-12345" or "9876543210"
            id_type: "name" | "patient_id" | "phone" | "aadhar" | "doctor_id"
        
        Returns:
            64-char hex string: "a1b2c3d4e5f6... (same for same input within 90 days)"
        
        Key Properties:
        - Deterministic: Same input → Same output (for audit trails)
        - Domain-separated: "pat-12345" as name ≠ "pat-12345" as patient_id
        - Rotating: Changes every 90 days (breaks linkage in old datasets)
        - One-way: Cannot reverse engineer original identifier
        """
        salt = RotatingSaltManager.get_rotating_salt()
        
        # Domain separation: different prefixes for different ID types
        domain_prefix = {
            "name": "NAME:",
            "patient_id": "PATID:",
            "phone": "PHONE:",
            "aadhar": "AADHAAR:",
            "doctor_id": "DOCID:",
            # ... etc for all ID types
        }.get(id_type, "GENERIC:")
        
        message = f"{domain_prefix}{identifier}".encode()
        pseudonym = hmac.new(salt, message, hashlib.sha256).hexdigest()
        
        return pseudonym  # Returns 64-char hex
```

**Test Cases:**
```python
# Test determinism (same input = same output)
assert pseudonymise_id("pat-12345", "patient_id") == \
       pseudonymise_id("pat-12345", "patient_id")

# Test domain separation (same ID, different type = different pseudonym)
assert pseudonymise_id("pat-12345", "patient_id") != \
       pseudonymise_id("pat-12345", "phone")

# Test rotation (same ID, different epoch = different pseudonym)
# (requires mocking RotatingSaltManager.get_current_epoch())

# Test one-wayness (cannot reverse)
# (verify SHA256 cannot be reversed)
```

**Deliverable:** pseudonymise_id() with 20+ unit tests

#### 1.3: Implement AnonymisationEngine.generalise_age()
```python
@staticmethod
def generalise_age(age: int) -> str:
    """
    Generalise age to 5-year bands for k-anonymity
    
    Example:
    - Input: 32 → Output: "30-34"
    - Input: 5 → Output: "0-4"
    - Input: 105 → Output: "100+"
    """
    if age < 0 or age > 120:
        return "UNKNOWN"
    
    lower_bound = (age // 5) * 5
    upper_bound = lower_bound + 4
    
    if upper_bound >= 100:
        return "100+"
    
    return f"{lower_bound}-{upper_bound}"
```

**Test Cases:**
```python
assert generalise_age(32) == "30-34"
assert generalise_age(0) == "0-4"
assert generalise_age(99) == "95-99"
assert generalise_age(105) == "100+"
```

**Deliverable:** generalise_age() with edge case tests

#### 1.4: Implement AnonymisationEngine.generalise_diabetes_duration()
```python
@staticmethod
def generalise_diabetes_duration(years: int) -> str:
    """
    Generalise diabetes duration to 2-year bands
    
    Example:
    - Input: 3 years → Output: "2-3 years"
    - Input: 0 years → Output: "0-1 years"
    - Input: 25 years → Output: "24+ years"
    """
    if years < 0:
        return "UNKNOWN"
    
    lower_bound = (years // 2) * 2
    upper_bound = lower_bound + 1
    
    if upper_bound >= 24:
        return "24+ years"
    
    return f"{lower_bound}-{upper_bound} years"
```

**Deliverable:** generalise_diabetes_duration() with tests

#### 1.5: Implement AnonymisationEngine.strip_village()
```python
@staticmethod
def strip_village(record: dict, table_name: str) -> dict:
    """
    Remove village name from record (quasi-identifier removal)
    
    Workflow:
    1. Identify which fields are "village" for this table
    2. Set them to None (NULL in database)
    3. Return modified record
    
    Why: Village name too specific for k-anonymity. District alone is enough.
    """
    record_copy = record.copy()
    
    if table_name == "patients":
        record_copy["village"] = None
    
    elif table_name == "doctors":
        record_copy["clinic_village"] = None
    
    elif table_name == "asha_workers":
        record_copy["village"] = None
    
    # ... etc for all tables with village fields
    
    return record_copy
```

**Deliverable:** strip_village() with table-specific logic

#### 1.6: Implement AnonymisationEngine.anonymise_record()
```python
@staticmethod
def anonymise_record(table_name: str, record: dict) -> dict:
    """
    Apply all anonymisation rules to a single record
    
    Workflow:
    1. For each field in record, check PII_FIELD_MAP[table][field]
    2. If DIRECT_ID → pseudonymise
    3. If QUASI_ID → generalise (age, duration, date) or strip (village)
    4. If NON_SENSITIVE → keep as-is
    5. Return anonymised record
    """
    PII_FIELD_MAP = {
        "patients": {
            "patient_id": "DIRECT_ID",
            "name": "DIRECT_ID",
            "phone": "DIRECT_ID",
            "aadhar_id": "DIRECT_ID",
            "age": "QUASI_ID",
            "diabetes_duration_years": "QUASI_ID",
            "village": "QUASI_ID",
            "district": "QUASI_ID",
            "gender": "QUASI_ID",
            "consent_given_at": "QUASI_ID",
            "hba1c": "NON_SENSITIVE",
            "created_at": "NON_SENSITIVE",
            # ... all other fields
        },
        # ... repeat for all 26 tables
    }
    
    anon_record = record.copy()
    
    for field_name, pii_type in PII_FIELD_MAP.get(table_name, {}).items():
        if field_name not in anon_record:
            continue
        
        if pii_type == "DIRECT_ID":
            # Pseudonymise (but skip if NULL)
            if anon_record[field_name] is not None:
                anon_record[field_name] = \
                    AnonymisationEngine.pseudonymise_id(
                        str(anon_record[field_name]), 
                        field_name
                    )
        
        elif pii_type == "QUASI_ID":
            if field_name == "age":
                anon_record[field_name] = generalise_age(anon_record[field_name])
            elif field_name == "diabetes_duration_years":
                anon_record[field_name] = generalise_diabetes_duration(anon_record[field_name])
            elif field_name.endswith("_date") or field_name == "consent_given_at":
                anon_record[field_name] = generalise_date_to_month(anon_record[field_name])
            # ... etc
        
        elif pii_type == "NON_SENSITIVE":
            # Keep as-is
            pass
    
    # Finally, strip village fields across all tables
    anon_record = AnonymisationEngine.strip_village(anon_record, table_name)
    
    return anon_record
```

**Deliverable:** anonymise_record() with comprehensive tests

#### 1.7: Implement AnonymisationEngine.verify_k_anonymity()
```python
@staticmethod
def verify_k_anonymity(records: List[dict], table_name: str, k_threshold: int = 5) -> Tuple[bool, dict]:
    """
    Verify dataset meets k-anonymity threshold
    
    Args:
        records: List of anonymised records
        table_name: Which table (to know quasi-identifiers)
        k_threshold: Minimum group size (default 5)
    
    Returns:
        (is_compliant: bool, report: dict)
        
    Example report:
    {
        "is_compliant": False,
        "threshold": 5,
        "violations": [
            {
                "quasi_id_values": {"district": "Mumbai", "age": "90-94", "gender": "M"},
                "group_size": 2,  # Less than threshold!
                "record_ids": ["anon-pat-123", "anon-pat-456"]
            }
        ]
    }
    """
    # Step 1: Define quasi-identifiers for this table
    QI_FIELDS = {
        "patients": ["district", "age", "gender"],
        "wound_sites": ["district", "age", "gender"],
        # ... etc for all tables with QI fields
    }.get(table_name, [])
    
    # Step 2: Group records by quasi-identifiers
    groups = {}
    for record in records:
        # Create key from QI values
        qi_values = tuple(record.get(field) for field in QI_FIELDS)
        qi_dict = dict(zip(QI_FIELDS, qi_values))
        qi_key = str(qi_dict)  # hashable key
        
        if qi_key not in groups:
            groups[qi_key] = {"values": qi_dict, "record_ids": [], "count": 0}
        
        groups[qi_key]["record_ids"].append(record.get("patient_id"))
        groups[qi_key]["count"] += 1
    
    # Step 3: Check each group for violations
    violations = []
    for qi_key, group_info in groups.items():
        if group_info["count"] < k_threshold:
            violations.append({
                "quasi_id_values": group_info["values"],
                "group_size": group_info["count"],
                "record_ids": group_info["record_ids"]
            })
    
    # Step 4: Return compliance status
    is_compliant = len(violations) == 0
    
    return is_compliant, {
        "is_compliant": is_compliant,
        "threshold": k_threshold,
        "total_groups": len(groups),
        "violations_count": len(violations),
        "violations": violations,
        "timestamp": datetime.now().isoformat()
    }
```

**Test Cases:**
```python
# Test: Compliant dataset
records = [
    {"patient_id": "p1", "district": "Mumbai", "age": "30-34", "gender": "M", ...},
    {"patient_id": "p2", "district": "Mumbai", "age": "30-34", "gender": "M", ...},
    {"patient_id": "p3", "district": "Mumbai", "age": "30-34", "gender": "M", ...},
    {"patient_id": "p4", "district": "Mumbai", "age": "30-34", "gender": "M", ...},
    {"patient_id": "p5", "district": "Mumbai", "age": "30-34", "gender": "M", ...},
]
is_compliant, report = verify_k_anonymity(records, "patients", k_threshold=5)
assert is_compliant == True

# Test: Non-compliant dataset (group size 2 < 5)
records = [
    {"patient_id": "p1", "district": "Mumbai", "age": "90-94", "gender": "M", ...},
    {"patient_id": "p2", "district": "Mumbai", "age": "90-94", "gender": "M", ...},  # Only 2 in this group!
    {"patient_id": "p3", "district": "Delhi", "age": "30-34", "gender": "F", ...},
    # ... other records in larger groups
]
is_compliant, report = verify_k_anonymity(records, "patients", k_threshold=5)
assert is_compliant == False
assert len(report["violations"]) == 1  # One group violates
```

**Deliverable:** verify_k_anonymity() with 15+ test cases

#### 1.8: Implement anonymise_dataset()
```python
@staticmethod
def anonymise_dataset(table_name: str, records: List[dict], 
                      verify_k_anonymity: bool = True, 
                      k_threshold: int = 5) -> Tuple[List[dict], dict]:
    """
    Anonymise entire dataset (used for exports)
    
    Returns:
        (anonymised_records: List[dict], metadata: dict)
    """
    # Step 1: Anonymise each record
    anon_records = [
        AnonymisationEngine.anonymise_record(table_name, record)
        for record in records
    ]
    
    # Step 2: Verify k-anonymity (if requested)
    metadata = {
        "table": table_name,
        "original_count": len(records),
        "anonymised_count": len(anon_records),
        "timestamp": datetime.now().isoformat(),
        "k_anonymity": None
    }
    
    if verify_k_anonymity:
        is_compliant, k_report = AnonymisationEngine.verify_k_anonymity(
            anon_records, table_name, k_threshold
        )
        metadata["k_anonymity"] = k_report
        metadata["k_anonymity_compliant"] = is_compliant
        
        if not is_compliant:
            # Log warning but don't fail
            AuditLogger.log_k_anonymity_violation(table_name, k_report)
    
    return anon_records, metadata
```

**Deliverable:** anonymise_dataset() with integration tests

#### 1.9: Create tests/test_anonymisation.py
```python
# 100+ unit tests covering:
# - TestPseudonymisation (determinism, domain separation, rotating salt)
# - TestAgeGeneralization (all edge cases)
# - TestDurationGeneralization (all edge cases)
# - TestVillageStripping (all table variants)
# - TestRecordAnonymisation (full pipeline)
# - TestKAnonymityVerification (compliant/violating datasets)
# - TestDatasetAnonymisation (end-to-end)
```

**Run Tests:**
```bash
cd backend
python -m pytest tests/test_anonymisation.py -v
# Expected: All 100+ tests pass ✅
```

**Deliverable:** Complete test suite with 100%+ coverage

---

### TASK 2: Build `backend/database/erasure.py` (1-2 days)

**File Location:** `backend/database/erasure.py`  
**Dependencies:** privacy.py complete, real schema  
**Tests:** Integration tests with live PostgreSQL

#### 2.1: Define DELETION_ORDER
```python
# Why this order? Foreign key constraints.
# Must delete child records before parent.

DELETION_ORDER = [
    # Tier 1: Deepest children (no other tables reference them)
    "ResearchExport",  # References Patient
    "Consent",         # References Patient
    "WoundSite",       # References Patient
    "PatientMedicalHistory",  # References Patient
    "DoctorPatientAssignment",  # References Patient + Doctor
    "AshaPatientAssignment",  # References Patient + AshaWorker
    "Prescription",    # References Patient + Doctor + Consultation
    "Consultation",    # References Patient + Doctor
    "TeleconsultSession",  # References Patient + Doctor
    "Notification",    # References Patient/Doctor/AshaWorker
    "SubscriptionTransaction",  # References Subscription
    "Subscription",    # References Patient
    "MonitoringSession",  # References Patient + WoundSite
    "Alert",           # References Patient + Doctor
    
    # Tier 2: Parent entities (can now delete safely)
    "Patient",         # Central entity
    
    # Tier 3: Other users (not related to this patient)
    # "Doctor"
    # "AshaWorker"
    # "Admin"
]
```

**Test:** Verify order respects all foreign keys

#### 2.2: Implement ErasurePipeline.request_erasure()
```python
class ErasurePipeline:
    """Manages 72-hour patient data deletion process per DPDP Section 8"""
    
    @staticmethod
    def request_erasure(patient_id: str, reason: str, db: Session) -> str:
        """
        Create erasure request (72-hour pending period)
        
        Args:
            patient_id: Patient UUID
            reason: Why is data being deleted (e.g., "patient-requested", "consent-revoked")
            db: Database session
        
        Returns:
            erasure_request_id: For tracking
        
        Workflow:
        1. Create ErasureRequest record in database
        2. Log audit event
        3. Return request ID
        
        72-hour window allows:
        - Doctor to retrieve patient records before deletion
        - Audit trail to be prepared
        - Emergency access if data deletion was accidental
        """
        import uuid
        from datetime import datetime, timedelta
        
        request_id = str(uuid.uuid4())
        can_delete_at = datetime.now() + timedelta(hours=72)
        
        # Create erasure request
        erasure_req = ErasureRequest(
            erasure_request_id=request_id,
            patient_id=uuid.UUID(patient_id),
            status="PENDING",  # Or "APPROVED", "CANCELLED", "EXECUTED"
            reason=reason,
            requested_at=datetime.now(),
            can_delete_at=can_delete_at,
            deleted_at=None
        )
        db.add(erasure_req)
        db.commit()
        
        # Audit log
        AuditLogger.log_patient_deletion(
            patient_id=patient_id,
            user_id="system",  # Or actual user if doctor initiated
            reason=f"{reason} (pending for 72 hours)",
            rows_deleted=0  # Not yet deleted
        )
        
        return request_id
```

**Deliverable:** request_erasure() with tests

#### 2.3: Implement ErasurePipeline.execute_erasure()
```python
@staticmethod
def execute_erasure(patient_id: str, dry_run: bool = False, db: Session = None) -> dict:
    """
    Execute patient deletion (after 72-hour period)
    
    Args:
        patient_id: Patient UUID
        dry_run: If True, count records but don't delete
        db: Database session
    
    Returns:
        {
            "status": "success",
            "patient_id": "pat-uuid",
            "dry_run": False,
            "deleted_records": {
                "Consent": 3,
                "WoundSite": 2,
                "MonitoringSession": 12,
                "Patient": 1,
                ... (all 26 tables)
            },
            "total_rows_deleted": 47,
            "erasure_duration_ms": 1230,
            "verification": {"all_deleted": True}
        }
    """
    start_time = datetime.now()
    patient_uuid = uuid.UUID(patient_id)
    deleted_counts = {}
    
    for table_name in DELETION_ORDER:
        # Get table class
        model_class = globals()[table_name]  # e.g., Consent, WoundSite, Patient
        
        # Build query
        query = db.query(model_class)
        
        # Filter by patient_id (or relationship to patient)
        if hasattr(model_class, "patient_id"):
            query = query.filter(model_class.patient_id == patient_uuid)
        # ... handle other relationships
        
        # Count records before delete
        count = query.count()
        deleted_counts[table_name] = count
        
        # Delete (or dry-run)
        if not dry_run:
            query.delete(synchronize_session=False)
            db.commit()
    
    # Verify all deleted
    verification = ErasurePipeline._verify_deletion(patient_id, db)
    
    elapsed_ms = int((datetime.now() - start_time).total_seconds() * 1000)
    
    return {
        "status": "success" if verification["all_deleted"] else "partial_failure",
        "patient_id": patient_id,
        "dry_run": dry_run,
        "deleted_records": deleted_counts,
        "total_rows_deleted": sum(deleted_counts.values()),
        "erasure_duration_ms": elapsed_ms,
        "verification": verification
    }
```

**Deliverable:** execute_erasure() with transaction rollback on error

#### 2.4: Implement ErasurePipeline._verify_deletion()
```python
@staticmethod
def _verify_deletion(patient_id: str, db: Session) -> dict:
    """
    Verify all patient records are deleted
    
    Returns:
        {
            "all_deleted": True/False,
            "tables_checked": 26,
            "remaining_records": {
                "Consent": 0,
                "WoundSite": 0,
                ...
            }
        }
    """
    patient_uuid = uuid.UUID(patient_id)
    remaining = {}
    
    for table_name in DELETION_ORDER:
        model_class = globals()[table_name]
        query = db.query(model_class)
        if hasattr(model_class, "patient_id"):
            query = query.filter(model_class.patient_id == patient_uuid)
        
        count = query.count()
        if count > 0:
            remaining[table_name] = count
    
    return {
        "all_deleted": len(remaining) == 0,
        "tables_checked": len(DELETION_ORDER),
        "remaining_records": remaining,
        "timestamp": datetime.now().isoformat()
    }
```

**Deliverable:** _verify_deletion() with 100% coverage

#### 2.5: Create tests/test_erasure.py
```python
# Integration tests covering:
# - TestErasureRequest (creation, 72-hour pending)
# - TestErasureExecution (dry-run, full deletion)
# - TestCascadeDeletion (verify all relationships deleted)
# - TestErasureVerification (confirm all records gone)
# - TestErasureAuditTrail (log events recorded)
```

**Run Tests:**
```bash
cd backend
python -m pytest tests/test_erasure.py -v
# Uses test PostgreSQL database (or SQLite)
```

**Deliverable:** Complete erasure test suite

---

### TASK 3: Integrate into Sahil's Export Endpoint (1 day)

**File to Update:** `backend/api/routers/export.py`  
**Dependencies:** privacy.py + erasure.py complete

#### 3.1: Update export endpoint to use privacy module
```python
from backend.database.privacy import AnonymisationEngine, AuditLogger

@router.post("/api/v1/export")
async def export_data(
    export_query: ExportFilterQuery,
    current_user: TokenPayload = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Export filtered dataset with k-anonymity verification
    
    Workflow:
    1. Query records from database
    2. Verify authorization (can user access this data?)
    3. Anonymise each record
    4. Verify k-anonymity (k ≥ 5)
    5. Return anonymised data + verification report
    """
    
    # Step 1: Query records
    records = db.query(Patient).filter(...).all()
    
    # Step 2: Verify authorization
    if current_user.user_type != "researcher":
        raise HTTPException(403, "Only researchers can export data")
    
    # Step 3: Anonymise
    anon_records, anon_metadata = AnonymisationEngine.anonymise_dataset(
        table_name="Patient",
        records=[r.__dict__ for r in records],
        verify_k_anonymity=True,
        k_threshold=5
    )
    
    # Step 4: Check k-anonymity
    if not anon_metadata["k_anonymity_compliant"]:
        # Reject export
        AuditLogger.log_k_anonymity_violation(
            "Patient",
            anon_metadata["k_anonymity"]
        )
        raise HTTPException(
            400,
            "Dataset does not meet k-anonymity threshold (k ≥ 5)",
            detail=anon_metadata["k_anonymity"]
        )
    
    # Step 5: Log export
    AuditLogger.log_data_export(
        user_id=current_user.user_id,
        user_type=current_user.user_type,
        table="Patient",
        record_count=len(anon_records),
        k_anonymity_verified=True
    )
    
    # Step 6: Return
    return response.success_response(
        data=anon_records,
        message="Data exported successfully",
        metadata={
            "count": len(anon_records),
            "anonymised": True,
            "k_anonymity": anon_metadata["k_anonymity"],
            "exported_at": datetime.now().isoformat()
        }
    )
```

**Deliverable:** Export endpoint fully integrated with privacy module

---

## 📋 CHECKLIST FOR SAUGATA

### Week 2 Deliverables (in order)

- [ ] **Day 0 (TODAY)**
  - [ ] Get real database schema (migration files or column list)
  - [ ] Discuss HMAC key management with Prof. Das
  - [ ] Agree on ML inference endpoint signatures with Shivraj

- [ ] **Days 1-2: privacy.py (HMAC + k-anonymity)**
  - [ ] RotatingSaltManager (with tests)
  - [ ] pseudonymise_id() (with determinism + domain separation tests)
  - [ ] generalise_age() (with edge cases)
  - [ ] generalise_diabetes_duration() (with edge cases)
  - [ ] strip_village() (with all table variants)
  - [ ] anonymise_record() (full pipeline)
  - [ ] verify_k_anonymity() (compliance checking)
  - [ ] anonymise_dataset() (end-to-end)
  - [ ] 100+ unit tests passing ✅

- [ ] **Days 3-4: erasure.py (72-hour deletion)**
  - [ ] DELETION_ORDER (respecting FK constraints)
  - [ ] request_erasure() (72-hour pending period)
  - [ ] execute_erasure() (cascading delete)
  - [ ] _verify_deletion() (confirmation)
  - [ ] Integration tests with live database ✅

- [ ] **Day 5: Integration + Export**
  - [ ] Export endpoint integrated with privacy.py
  - [ ] k-anonymity verification in export
  - [ ] Export audit logging working
  - [ ] End-to-end test: Export → Anonymised data returned ✅

### Success Criteria

✅ All 100+ tests passing  
✅ No Python linting errors (black, flake8, mypy)  
✅ DPDP compliance verified (Section 8 erasure, Section 5 pseudonymisation)  
✅ Export endpoint rejects data that fails k-anonymity  
✅ Audit logs record all privacy events (export, deletion, consent)  
✅ Code submitted to GitHub by End of Week 2

---

## 📞 CONTACTS FOR BLOCKERS

| Blocker | Contact | Response Time |
|---------|---------|----------------|
| Database schema | Sahil Kumar Gupta | 2 hours |
| HMAC key policy | Prof. Dipak Kumar Das | 24 hours |
| ML endpoint format | Shivraj Gulve | 3 hours |
| PII field classification | Saugata (self) | — |
| SQL query help | Sahil | 1 hour |

---

## 🚀 SUCCESS = Week 2 Complete When

1. ✅ privacy.py ready (all tests pass)
2. ✅ erasure.py ready (all tests pass)
3. ✅ Export endpoint integrated
4. ✅ Real database tested (not just unit tests)
5. ✅ DPDP audit trail complete
6. ✅ Code submitted to GitHub
7. ✅ Prof. Das reviews and approves

**Target Date:** End of Week 2 (by Friday)

