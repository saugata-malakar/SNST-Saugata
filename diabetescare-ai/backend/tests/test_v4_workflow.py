import io
import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.api.dependencies import decode_token
from backend.api.main import app
from backend.database.models import Base
from backend.database.session import get_db

_ENGINE = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_ENGINE)


@pytest.fixture(scope="module", autouse=True)
def setup_schema():
    Base.metadata.create_all(bind=_ENGINE)
    yield
    Base.metadata.drop_all(bind=_ENGINE)


@pytest.fixture(scope="module")
def db_session():
    session = _SessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="module")
def client(db_session):
    def override_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_db

    import backend.api.middleware as mw
    original = mw._get_session_local
    mw._get_session_local = lambda: _SessionLocal

    with TestClient(app, raise_server_exceptions=False) as c:
        yield c

    app.dependency_overrides.clear()
    mw._get_session_local = original


def _headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _upload_3_photos(client: TestClient, token: str, sub_id: str):
    for num in (1, 2, 3):
        resp = client.post(
            f"/api/v1/submissions/{sub_id}/photos",
            data={"photo_number": str(num)},
            files={"file": (f"foot_{num}.jpg", b"fake-jpeg-bytes", "image/jpeg")},
            headers=_headers(token),
        )
        assert resp.status_code == 201, resp.text


def test_multi_identifier_registration_login_and_me(client):
    # Register field_worker with phone + username + worker_type
    reg = client.post(
        "/api/v1/auth/register",
        json={
            "phone": "9876543210",
            "username": "asha_rina",
            "password": "Secret123!",
            "role": "field_worker",
            "worker_type": "ASHA",
            "full_name": "Rina Devi",
            "district": "Paschim Medinipur",
        },
    )
    assert reg.status_code == 201, reg.text
    user_data = reg.json()
    worker_id = user_data["worker_id"]
    assert worker_id

    # Login via phone, username, and worker_id
    for body in (
        {"phone": "9876543210", "password": "Secret123!"},
        {"username": "asha_rina", "password": "Secret123!"},
        {"worker_id": worker_id, "password": "Secret123!"},
        {"identifier": worker_id, "password": "Secret123!"},
    ):
        login = client.post("/api/v1/auth/login", json=body)
        assert login.status_code == 200, login.text
        token = login.json()["access_token"]
        claims = decode_token(token)
        assert claims["role"] == "field_worker"
        assert claims["phone"] == "9876543210"
        assert claims["user_id"] == user_data["user_id"]

    me = client.get("/api/v1/auth/me", headers=_headers(token))
    assert me.status_code == 200
    assert me.json()["worker_type"] == "ASHA"


def test_doctor_direct_submission_and_followup_flow(client):
    # Register + login doctor via email
    reg = client.post(
        "/api/v1/auth/register",
        json={
            "email": "doc.sen@kgp.edu",
            "password": "DocPass1!",
            "role": "doctor",
            "full_name": "Dr. Sen",
            "district": "Kharagpur",
        },
    )
    assert reg.status_code == 201
    doc_token = client.post(
        "/api/v1/auth/login",
        json={"email": "doc.sen@kgp.edu", "password": "DocPass1!"},
    ).json()["access_token"]

    # Create submission
    sub_resp = client.post(
        "/api/v1/submissions/",
        json={
            "patient_id": "PT-DOC-001",
            "patient_name": "Ramesh Das",
            "patient_age": 56,
            "patient_weight_kg": 72.5,
            "patient_bp_systolic": 140,
            "patient_bp_diastolic": 90,
            "patient_blood_sugar": 215.0,
            "patient_comorbidities": ["hypertension", "neuropathy"],
        },
        headers=_headers(doc_token),
    )
    assert sub_resp.status_code == 201, sub_resp.text
    sub_id = sub_resp.json()["submission_id"]

    # Submit with only 1 photo -> AI check fails -> rejected, no payment
    client.post(
        f"/api/v1/submissions/{sub_id}/photos",
        data={"photo_number": "1"},
        files={"file": ("foot_1.jpg", b"img1", "image/jpeg")},
        headers=_headers(doc_token),
    )
    fail_submit = client.post(f"/api/v1/submissions/{sub_id}/submit", headers=_headers(doc_token))
    assert fail_submit.status_code == 200
    assert fail_submit.json()["status"] == "rejected"
    assert fail_submit.json()["ai_quality_passed"] is False

    # Upload remaining 2 photos + report + clinical note -> resubmit -> accepted + ₹80
    for num in (2, 3):
        client.post(
            f"/api/v1/submissions/{sub_id}/photos",
            data={"photo_number": str(num)},
            files={"file": (f"foot_{num}.jpg", b"img", "image/jpeg")},
            headers=_headers(doc_token),
        )
    rep = client.post(
        f"/api/v1/submissions/{sub_id}/reports",
        files={"file": ("lab.pdf", b"%PDF-1.4", "application/pdf")},
        headers=_headers(doc_token),
    )
    assert rep.status_code == 201

    note = client.post(
        f"/api/v1/submissions/{sub_id}/clinical-note",
        json={
            "diagnosis": "Wagner Grade 1 superficial ulcer",
            "severity": "moderate",
            "treatment_needed": "offloading + dressing",
            "medication": "Amoxicillin-Clavulanate",
        },
        headers=_headers(doc_token),
    )
    assert note.status_code == 201

    ok_submit = client.post(f"/api/v1/submissions/{sub_id}/submit", headers=_headers(doc_token))
    assert ok_submit.status_code == 200, ok_submit.text
    body = ok_submit.json()
    assert body["status"] == "accepted"
    assert body["ai_quality_passed"] is True
    assert len(body["payments"]) == 1
    assert body["payments"][0]["amount"] == 80.0

    # Follow-up submission referencing same patient_id / original_submission_id
    fu = client.post(
        "/api/v1/submissions/",
        json={
            "is_followup": True,
            "original_submission_id": sub_id,
            "patient_age": 56,
            "patient_blood_sugar": 170.0,
        },
        headers=_headers(doc_token),
    )
    assert fu.status_code == 201
    assert fu.json()["patient_id"] == "PT-DOC-001"
    assert fu.json()["is_followup"] is True


def test_asha_moderator_doctor_and_admin_workflow(client):
    # Register + login ASHA, Moderator, Doctor, Admin
    def reg_login(email, role, **extra):
        r = client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": "Password1!", "role": role, **extra},
        )
        assert r.status_code == 201, r.text
        l = client.post("/api/v1/auth/login", json={"email": email, "password": "Password1!"})
        assert l.status_code == 200, l.text
        return l.json()["access_token"], r.json()["user_id"]

    asha_tok, asha_id = reg_login("asha1@kgp.edu", "field_worker", worker_type="ICDS", full_name="Maya")
    mod_tok, mod_id = reg_login("mod1@kgp.edu", "moderator", full_name="Mod Priya")
    doc_tok, doc_id = reg_login("doc2@kgp.edu", "doctor", full_name="Dr. Roy")
    adm_tok, _ = reg_login("admin1@kgp.edu", "admin", full_name="Super Admin")

    # 1. ASHA creates submission + 3 photos + submits
    sub = client.post(
        "/api/v1/submissions/",
        json={"patient_name": "Sita Mondal", "patient_age": 62, "patient_blood_sugar": 240.0},
        headers=_headers(asha_tok),
    ).json()
    sid = sub["submission_id"]
    _upload_3_photos(client, asha_tok, sid)
    submitted = client.post(f"/api/v1/submissions/{sid}/submit", headers=_headers(asha_tok))
    assert submitted.status_code == 200
    assert submitted.json()["status"] == "ai_reviewed"

    # ASHA cannot add clinical note
    forbidden_note = client.post(
        f"/api/v1/submissions/{sid}/clinical-note",
        json={"diagnosis": "test"},
        headers=_headers(asha_tok),
    )
    assert forbidden_note.status_code == 403

    # 2. Moderator sees it in queue & approves -> ₹20
    m_queue = client.get("/api/v1/moderator/queue", headers=_headers(mod_tok))
    assert m_queue.status_code == 200
    assert any(item["submission_id"] == sid for item in m_queue.json()["queue"])

    m_app = client.post(
        f"/api/v1/moderator/{sid}/approve",
        json={"note": "Clear coin reference and 3 angles"},
        headers=_headers(mod_tok),
    )
    assert m_app.status_code == 200
    assert m_app.json()["status"] == "moderator_approved"

    # 3. Doctor sees it in doctor queue & validates -> ₹50 ASHA + ₹30 Doctor
    d_queue = client.get("/api/v1/doctor/queue", headers=_headers(doc_tok))
    assert d_queue.status_code == 200
    assert any(item["submission_id"] == sid for item in d_queue.json()["queue"])

    d_val = client.post(
        f"/api/v1/doctor/{sid}/validate",
        json={"diagnosis": "Neuropathic foot ulcer", "severity": "mild", "medication": "Metformin"},
        headers=_headers(doc_tok),
    )
    assert d_val.status_code == 200
    assert d_val.json()["status"] == "doctor_completed"

    # 4. Check payments for ASHA (50), Moderator (20), Doctor (30)
    asha_pay = client.get("/api/v1/payments/my", headers=_headers(asha_tok)).json()
    mod_pay = client.get("/api/v1/payments/my", headers=_headers(mod_tok)).json()
    doc_pay = client.get("/api/v1/payments/my", headers=_headers(doc_tok)).json()
    assert asha_pay["total_earned"] == 50.0
    assert mod_pay["total_earned"] == 20.0
    assert doc_pay["total_earned"] == 30.0

    # 5. Admin endpoints
    assert client.get("/api/v1/admin/users?role=moderator", headers=_headers(adm_tok)).status_code == 200
    assert client.get("/api/v1/admin/submissions?status=doctor_completed", headers=_headers(adm_tok)).status_code == 200
    assert client.get("/api/v1/admin/payments", headers=_headers(adm_tok)).status_code == 200
    stats = client.get("/api/v1/admin/stats", headers=_headers(adm_tok))
    assert stats.status_code == 200
    assert stats.json()["total_payments_amount"] >= 180.0
