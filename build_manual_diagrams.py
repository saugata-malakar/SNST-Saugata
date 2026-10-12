# build_manual_diagrams.py
# Generates high-fidelity visual UI diagrams representing the DOM screens of DiabetesCare AI

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUT_DIR = "manual_assets"
os.makedirs(OUT_DIR, exist_ok=True)

NAVY = "#0B132B"
CARD_BG = "#111C38"
SUB_CARD = "#0C152E"
BORDER = "#23355E"
BLUE = "#2563EB"
EMERALD = "#10B981"
AMBER = "#F59E0B"
RED = "#EF4444"
WHITE = "#FFFFFF"
TEXT_MUTED = "#94A3B8"

def save_fig(fig, filename):
    filepath = os.path.join(OUT_DIR, filename)
    fig.savefig(filepath, dpi=200, bbox_inches='tight', facecolor=NAVY)
    plt.close(fig)
    print(f"Saved: {filepath}")

# 1. Screen: Portal Login
def create_login_screen():
    fig, ax = plt.subplots(figsize=(6, 10))
    ax.set_facecolor(NAVY)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 160)
    ax.axis('off')

    ax.text(8, 155, "09:41", color=WHITE, fontsize=9, weight='bold')
    ax.text(85, 155, "5G | 98%", color=WHITE, fontsize=9)

    circle = patches.Circle((50, 135), 10, color="#1E3A8A")
    ax.add_patch(circle)
    ax.text(50, 133, "+", color=WHITE, fontsize=24, ha='center', weight='bold')
    ax.text(50, 118, "DiabetesCare AI", color=WHITE, fontsize=16, weight='bold', ha='center')
    ax.text(50, 112, "Clinical Triage & Wound Monitoring", color=TEXT_MUTED, fontsize=9, ha='center')
    ax.text(50, 106, "IIT Kharagpur · Paschim Medinipur Apex Hub", color=EMERALD, fontsize=8, ha='center', weight='bold')

    box1 = patches.FancyBboxPatch((8, 55), 84, 46, boxstyle="round,pad=1", ec=BORDER, fc=CARD_BG, lw=1.5)
    ax.add_patch(box1)
    ax.text(14, 96, "SELECT CLINICAL ACCESS PERSONA", color=TEXT_MUTED, fontsize=8, weight='bold')

    roles = [
        ("[DR] Lead Diabetologist", True, RED, 84),
        ("[PT] Enrolled Patient", False, EMERALD, 74),
        ("[HW] ASHA Health Worker", False, BLUE, 64),
        ("[AD] Hospital Administrator", False, AMBER, 54),
    ]
    for title, active, col, y in roles:
        r_box = patches.FancyBboxPatch((12, y), 76, 7.5, boxstyle="round,pad=0.5", ec=col if active else BORDER, fc=col if active else SUB_CARD, lw=1.2)
        ax.add_patch(r_box)
        ax.text(16, y+2, title, color=WHITE if active else TEXT_MUTED, fontsize=8.5, weight='bold' if active else 'normal')
        if active:
            ax.text(82, y+2, "[ACTIVE]", color=WHITE, fontsize=7.5, weight='bold', ha='right')

    box2 = patches.FancyBboxPatch((8, 22), 84, 28, boxstyle="round,pad=1", ec=BORDER, fc=CARD_BG, lw=1.5)
    ax.add_patch(box2)
    ax.text(14, 45, "AUTHORIZED CREDENTIALS (RBAC)", color=TEXT_MUTED, fontsize=8, weight='bold')
    
    f1 = patches.FancyBboxPatch((12, 36), 76, 6, boxstyle="round,pad=0.4", ec=BORDER, fc=SUB_CARD, lw=1)
    ax.add_patch(f1)
    ax.text(16, 38, "doctor@demo.in (Lead Diabetologist)", color=WHITE, fontsize=8)

    f2 = patches.FancyBboxPatch((12, 28), 76, 6, boxstyle="round,pad=0.4", ec=BORDER, fc=SUB_CARD, lw=1)
    ax.add_patch(f2)
    ax.text(16, 30, "******** (DPDP Act TLS 1.3)", color=TEXT_MUTED, fontsize=8)

    btn = patches.FancyBboxPatch((8, 8), 84, 9, boxstyle="round,pad=0.8", ec=BLUE, fc=BLUE, lw=1)
    ax.add_patch(btn)
    ax.text(50, 11.5, "Sign In to Command Portal ->", color=WHITE, fontsize=10, weight='bold', ha='center')

    ax.text(50, 2, "Connected: http://192.168.31.94:8000 (FastAPI Master)", color=TEXT_MUTED, fontsize=7, ha='center')

    save_fig(fig, "screen_login.png")

# 2. Screen: Doctor Command Hub & Clinical Triage
def create_triage_screen():
    fig, ax = plt.subplots(figsize=(6, 10))
    ax.set_facecolor(NAVY)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 160)
    ax.axis('off')

    ax.text(8, 155, "09:42", color=WHITE, fontsize=9, weight='bold')
    ax.text(85, 155, "5G | 98%", color=WHITE, fontsize=9)
    ax.text(8, 146, "CLINICAL TRIAGE COMMAND HUB", color=RED, fontsize=8, weight='bold')
    ax.text(8, 138, "Lead Diabetologist Dashboard", color=WHITE, fontsize=14, weight='bold')
    ax.text(8, 132, "Midnapore Medical College & Hospital · Apex Center", color=TEXT_MUTED, fontsize=7.5)

    kpis = [
        ("ACTIVE COHORT", "4 Enrolled", "Assigned Cases", 8, 114, WHITE),
        ("URGENT ALERTS", "2 Pending", "Action Required", 52, 114, RED),
        ("TELECONSULT", "1 Scheduled", "eSanjeevani Queue", 8, 97, EMERALD),
        ("HEALING RATE", "74.2% Mean", "30-Day Velocity", 52, 97, BLUE),
    ]
    for title, val, sub, x, y, col in kpis:
        k_box = patches.FancyBboxPatch((x, y), 40, 14, boxstyle="round,pad=0.6", ec=BORDER, fc=CARD_BG, lw=1.2)
        ax.add_patch(k_box)
        ax.text(x+3, y+10.5, title, color=TEXT_MUTED, fontsize=6.5, weight='bold')
        ax.text(x+3, y+5, val, color=col, fontsize=10.5, weight='bold')
        ax.text(x+3, y+1.5, sub, color=TEXT_MUTED, fontsize=6)

    al_box = patches.FancyBboxPatch((8, 66), 84, 26, boxstyle="round,pad=0.8", ec=RED, fc=CARD_BG, lw=1.5)
    ax.add_patch(al_box)
    ax.text(12, 87, "[!] URGENT CLINICAL ALERTS (REAL-TIME TRIAGE)", color=RED, fontsize=8, weight='bold')
    
    ax.text(12, 80, "Ramesh Chandra Sen · PAT_KGP_01", color=WHITE, fontsize=8.5, weight='bold')
    badge1 = patches.FancyBboxPatch((74, 79), 14, 4.5, boxstyle="round,pad=0.2", ec=RED, fc=RED)
    ax.add_patch(badge1)
    ax.text(81, 80.5, "RED HIGH", color=WHITE, fontsize=6, weight='bold', ha='center')
    ax.text(12, 74, "Ulcer area enlargement (+14.2%). Urgent offloading review.", color=TEXT_MUTED, fontsize=7)
    ax.text(12, 69, "Submitted by ASHA · 10m ago  |  [Review Record ->]", color=EMERALD, fontsize=7, weight='bold')

    reg_box = patches.FancyBboxPatch((8, 8), 84, 54, boxstyle="round,pad=0.8", ec=BORDER, fc=CARD_BG, lw=1.2)
    ax.add_patch(reg_box)
    ax.text(12, 57, "DEPARTMENT PATIENT COHORT REGISTRY", color=WHITE, fontsize=8.5, weight='bold')
    ax.text(12, 52, "Live synchronization via /api/v1/patients", color=TEXT_MUTED, fontsize=7)

    pts = [
        ("PAT_KGP_01", "Ramesh Chandra Sen", "58y/M", "Grade 2", "2.15 cm2", RED, 42),
        ("PAT_KGP_02", "Anjali Devi Das", "62y/F", "Grade 2", "2.90 cm2", RED, 31),
        ("PAT_KGP_03", "Sunil Kumar Roy", "50y/M", "Grade 1", "1.45 cm2", AMBER, 20),
        ("PAT_KGP_04", "Lakshmi N. Paul", "67y/M", "Grade 3", "7.10 cm2", RED, 9),
    ]
    for pid, name, dem, wg, area, bcol, y in pts:
        p_row = patches.FancyBboxPatch((11, y), 78, 9, boxstyle="round,pad=0.3", ec=BORDER, fc=SUB_CARD, lw=0.8)
        ax.add_patch(p_row)
        ax.text(14, y+5, name, color=WHITE, fontsize=8, weight='bold')
        ax.text(14, y+1.5, f"{pid} · {dem} · Paschim Medinipur", color=TEXT_MUTED, fontsize=6.5)
        w_b = patches.FancyBboxPatch((55, y+2), 16, 5, boxstyle="round,pad=0.2", ec=bcol, fc=bcol)
        ax.add_patch(w_b)
        ax.text(63, y+3.5, wg, color=WHITE, fontsize=6.5, weight='bold', ha='center')
        ax.text(85, y+3.5, area, color=WHITE, fontsize=7.5, weight='bold', ha='right')

    save_fig(fig, "screen_triage_hub.png")

# 3. Screen: 3-Photo Checklist (Enforced Protocol Lock)
def create_photo_flow_screen():
    fig, ax = plt.subplots(figsize=(6, 10))
    ax.set_facecolor(NAVY)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 160)
    ax.axis('off')

    ax.text(8, 155, "09:43", color=WHITE, fontsize=9, weight='bold')
    ax.text(85, 155, "5G | 98%", color=WHITE, fontsize=9)
    ax.text(8, 145, "3-PHOTO PROTOCOL CHECKLIST", color=EMERALD, fontsize=8, weight='bold')
    ax.text(8, 137, "Mandatory Clinical Sequence", color=WHITE, fontsize=14, weight='bold')
    ax.text(8, 131, "Patient: Ramesh Chandra Sen (PAT_KGP_01) · Visit VIS_004", color=TEXT_MUTED, fontsize=7.5)

    warn_box = patches.FancyBboxPatch((8, 114), 84, 13, boxstyle="round,pad=0.5", ec=AMBER, fc="#2A1B0A", lw=1.2)
    ax.add_patch(warn_box)
    ax.text(12, 122, "[LOCK] PROTOCOL ENFORCEMENT ACTIVE", color=AMBER, fontsize=8, weight='bold')
    ax.text(12, 117, "All 3 photos are clinically mandatory. Submission is locked until complete.", color="#FDE68A", fontsize=6.5)

    steps = [
        ("1", "[P1] Overview Photo", "Capture full limb/foot for bodily context.", True, 88),
        ("2", "[P2] Close-Up Photo", "Macro focus on ulcer bed, margin & depth.", True, 62),
        ("3", "[P3] Measurement Photo", "Circular 20mm calibrant coin on intact skin.", False, 36),
    ]
    for num, title, desc, done, y in steps:
        s_box = patches.FancyBboxPatch((8, y), 84, 22, boxstyle="round,pad=0.8", ec=EMERALD if done else BORDER, fc=CARD_BG, lw=1.5 if done else 1)
        ax.add_patch(s_box)
        nc = patches.Circle((16, y+11), 5, color=EMERALD if done else "#334155")
        ax.add_patch(nc)
        ax.text(16, y+9.5, "[OK]" if done else num, color=WHITE, fontsize=7, weight='bold', ha='center')
        ax.text(25, y+13, title, color=WHITE, fontsize=9, weight='bold')
        ax.text(25, y+7.5, desc, color=TEXT_MUTED, fontsize=7)
        ab = patches.FancyBboxPatch((64, y+3.5), 24, 6.5, boxstyle="round,pad=0.3", ec=EMERALD if done else BLUE, fc="#064E3B" if done else BLUE, lw=1)
        ax.add_patch(ab)
        ax.text(76, y+5.5, "Retake" if done else "Capture ->", color=WHITE, fontsize=7.5, weight='bold', ha='center')

    stk_box = patches.FancyBboxPatch((8, 19), 84, 13, boxstyle="round,pad=0.5", ec=BLUE, fc="#0B2046", lw=1)
    ax.add_patch(stk_box)
    ax.text(12, 27, "(*) CALIBRANT MARKER REMINDER:", color="#60A5FA", fontsize=7.5, weight='bold')
    ax.text(12, 22, "Place blue 20mm marker on intact skin 1–2 cm adjacent to ulcer edge.", color="#93C5FD", fontsize=6.5)

    sbtn = patches.FancyBboxPatch((8, 6), 84, 9, boxstyle="round,pad=0.8", ec="#475569", fc="#334155", lw=1)
    ax.add_patch(sbtn)
    ax.text(50, 9.5, "[LOCKED] 2/3 Captured — Complete All to Proceed", color="#94A3B8", fontsize=8.5, weight='bold', ha='center')

    save_fig(fig, "screen_photo_flow.png")

# 4. Screen: Review & Doctor Diagnosis Concordance Matching
def create_review_screen():
    fig, ax = plt.subplots(figsize=(6, 10))
    ax.set_facecolor(NAVY)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 160)
    ax.axis('off')

    ax.text(8, 155, "09:45", color=WHITE, fontsize=9, weight='bold')
    ax.text(85, 155, "5G | 97%", color=WHITE, fontsize=9)
    ax.text(8, 145, "AI ANALYSIS & CLINICAL REVIEW", color=BLUE, fontsize=8, weight='bold')
    ax.text(8, 137, "Measurement Photo Verification", color=WHITE, fontsize=13, weight='bold')

    img_box = patches.FancyBboxPatch((8, 97), 84, 36, boxstyle="round,pad=0.8", ec=BORDER, fc="#050A18", lw=1.2)
    ax.add_patch(img_box)
    ax.text(50, 120, "[AI SEGMENTATION CONTOUR OVERLAY ACTIVE]", color=EMERALD, fontsize=8, weight='bold', ha='center')
    ax.text(50, 114, "Calibrant Circle Detected · Hough px/mm: 14.2 · Blur: PASS", color=TEXT_MUTED, fontsize=6.5, ha='center')
    
    t1 = patches.FancyBboxPatch((14, 100), 34, 5.5, boxstyle="round,pad=0.2", ec=BLUE, fc=BLUE)
    ax.add_patch(t1)
    ax.text(31, 101.8, "AI Segmentation Overlay", color=WHITE, fontsize=6.5, weight='bold', ha='center')
    t2 = patches.FancyBboxPatch((52, 100), 34, 5.5, boxstyle="round,pad=0.2", ec=BORDER, fc=SUB_CARD)
    ax.add_patch(t2)
    ax.text(69, 101.8, "Original Clinical Photo", color=TEXT_MUTED, fontsize=6.5, ha='center')

    m_box = patches.FancyBboxPatch((8, 64), 84, 30, boxstyle="round,pad=0.8", ec=BORDER, fc=CARD_BG, lw=1.2)
    ax.add_patch(m_box)
    ax.text(12, 89, "AUTOMATED MEASUREMENTS & ML CLASSIFICATION", color=TEXT_MUTED, fontsize=7.5, weight='bold')
    
    m_vals = [
        ("Surface Area (2D):", "2.15 cm2", "Max Feret Length:", "22.4 mm"),
        ("Orthogonal Width:", "14.1 mm", "Perimeter Length:", "58.2 mm"),
        ("ML Wagner Grade:", "Grade 1 (Superficial)", "Confidence Score:", "94.0% Optimal"),
    ]
    y_pos = 81
    for l1, v1, l2, v2 in m_vals:
        ax.text(12, y_pos, l1, color=TEXT_MUTED, fontsize=7)
        ax.text(34, y_pos, v1, color=EMERALD if "Area" in l1 or "Grade" in l1 else WHITE, fontsize=7, weight='bold')
        ax.text(52, y_pos, l2, color=TEXT_MUTED, fontsize=7)
        ax.text(78, y_pos, v2, color=WHITE, fontsize=7, weight='bold')
        y_pos -= 6.5

    doc_box = patches.FancyBboxPatch((8, 19), 84, 42, boxstyle="round,pad=0.8", ec=EMERALD, fc=CARD_BG, lw=1.5)
    ax.add_patch(doc_box)
    ax.text(12, 56, "DOCTOR CLINICAL DIAGNOSIS & AI MATCHING", color=WHITE, fontsize=8, weight='bold')
    
    for i in range(6):
        is_sel = (i == 1)
        gb = patches.FancyBboxPatch((12 + i*13, 46), 11, 6.5, boxstyle="round,pad=0.2", ec=EMERALD if is_sel else BORDER, fc=EMERALD if is_sel else SUB_CARD)
        ax.add_patch(gb)
        ax.text(17.5 + i*13, 48.5, f"G{i}", color=WHITE if is_sel else TEXT_MUTED, fontsize=7, weight='bold', ha='center')

    inp = patches.FancyBboxPatch((12, 33), 76, 10, boxstyle="round,pad=0.4", ec=BORDER, fc=SUB_CARD)
    ax.add_patch(inp)
    ax.text(14, 39, "Dr. Notes: Superficial neuropathic ulcer with clean granulating bed.", color=WHITE, fontsize=6.8)
    ax.text(14, 35, "Offloading rocker shoe prescribed · Review in 7 days.", color=TEXT_MUTED, fontsize=6.5)

    mb = patches.FancyBboxPatch((12, 22), 76, 8.5, boxstyle="round,pad=0.3", ec=EMERALD, fc="#064E3B")
    ax.add_patch(mb)
    ax.text(15, 26.5, "[OK] CONCORDANT DIAGNOSIS (AI & Doctor in Agreement)", color="#6EE7B7", fontsize=7, weight='bold')
    ax.text(15, 23.5, "• AI Model: Wagner Grade 1  ==  Doctor Assessment: Wagner Grade 1", color=WHITE, fontsize=6.2)

    sub_btn = patches.FancyBboxPatch((8, 5), 84, 10, boxstyle="round,pad=0.8", ec=EMERALD, fc=EMERALD)
    ax.add_patch(sub_btn)
    ax.text(50, 9, "Accept & Submit Authoritative Diagnosis [OK]", color=WHITE, fontsize=9.5, weight='bold', ha='center')

    save_fig(fig, "screen_review.png")

# 5. Screen: Option 4 Full Wound Trajectory & 10-Point Monofilament Map
def create_trajectory_screen():
    fig, ax = plt.subplots(figsize=(6, 10))
    ax.set_facecolor(NAVY)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 160)
    ax.axis('off')

    ax.text(8, 155, "09:46", color=WHITE, fontsize=9, weight='bold')
    ax.text(85, 155, "5G | 97%", color=WHITE, fontsize=9)
    ax.text(8, 145, "LONGITUDINAL CLINICAL TRAJECTORY", color=BLUE, fontsize=8, weight='bold')
    ax.text(8, 137, "Ramesh Chandra Sen · ABHA: 91-8421", color=WHITE, fontsize=13, weight='bold')
    ax.text(8, 131, "58y · Plantar Ulcer · Paschim Medinipur Sub-Centre", color=TEXT_MUTED, fontsize=7.5)

    ch_box = patches.FancyBboxPatch((8, 86), 84, 42, boxstyle="round,pad=0.8", ec=BORDER, fc=CARD_BG, lw=1.2)
    ax.add_patch(ch_box)
    ax.text(12, 122, "30-DAY WOUND SURFACE AREA REDUCTION (cm2)", color=TEXT_MUTED, fontsize=7.5, weight='bold')
    ax.text(85, 122, "-58.6% Total", color=EMERALD, fontsize=8, weight='bold', ha='right')

    dates = ["10 Aug", "14 Aug", "18 Aug", "22 Aug", "26 Aug", "30 Aug", "04 Oct"]
    areas = [5.2, 4.6, 3.9, 3.4, 2.8, 2.5, 2.15]
    for idx, (d, a) in enumerate(zip(dates, areas)):
        bx = 14 + idx * 10.5
        bh = (a / 6.0) * 20
        b_bar = patches.Rectangle((bx, 96), 6.5, bh, color=EMERALD if idx == 6 else BLUE)
        ax.add_patch(b_bar)
        ax.text(bx+3.2, 96+bh+1.5, f"{a}", color=WHITE, fontsize=6, ha='center', weight='bold')
        ax.text(bx+3.2, 91, d, color=TEXT_MUTED, fontsize=5.5, ha='center')

    mono_box = patches.FancyBboxPatch((8, 44), 84, 38, boxstyle="round,pad=0.8", ec=BORDER, fc=CARD_BG, lw=1.2)
    ax.add_patch(mono_box)
    ax.text(12, 76, "10-POINT MONOFILAMENT MAP (NEUROPATHY)", color=WHITE, fontsize=8, weight='bold')
    ax.text(12, 71, "Semmes-Weinstein 5.07 (10g) sensory testing protocol", color=TEXT_MUTED, fontsize=6.8)

    foot_out = patches.Ellipse((32, 57), 16, 22, color=SUB_CARD)
    ax.add_patch(foot_out)
    
    sens_pts = [
        (30, 65, RED, "Great Toe: Absent"),
        (35, 62, RED, "3rd Toe: Absent"),
        (26, 57, RED, "1st Metatarsal: Absent"),
        (32, 55, AMBER, "3rd Metatarsal: Diminished"),
        (37, 56, RED, "5th Metatarsal: Absent"),
        (30, 48, EMERALD, "Heel: Sensation Intact"),
    ]
    for px, py, pcol, _ in sens_pts:
        dot = patches.Circle((px, py), 1.2, color=pcol)
        ax.add_patch(dot)

    ax.text(50, 65, "Total Score: 4/10", color=RED, fontsize=10, weight='bold')
    ax.text(50, 60, "Loss of Protective Sensation (LOPS)", color=AMBER, fontsize=7, weight='bold')
    ax.text(50, 54, "[o] Red: Sensation Absent (LOPS)", color=RED, fontsize=6.5)
    ax.text(50, 49, "[o] Amber: Diminished Perception", color=AMBER, fontsize=6.5)
    ax.text(50, 44, "[o] Green: Normal Tactile Response", color=EMERALD, fontsize=6.5)

    cp_box = patches.FancyBboxPatch((8, 8), 84, 32, boxstyle="round,pad=0.8", ec=BORDER, fc=CARD_BG, lw=1.2)
    ax.add_patch(cp_box)
    ax.text(12, 34, "AI CLINICAL CARE PLAN ADVISORY", color=WHITE, fontsize=8, weight='bold')
    ax.text(12, 28, "• Total Contact Cast (TCC) or rigid diabetic rocker shoe offloading.", color=TEXT_MUTED, fontsize=7)
    ax.text(12, 23, "• Sterile normal saline irrigation with hydrocolloid foam barrier.", color=TEXT_MUTED, fontsize=7)
    ax.text(12, 18, "• Weekly serial digital photography with circular calibrant marker.", color=TEXT_MUTED, fontsize=7)
    ax.text(12, 13, "• Strict glycemic target: HbA1c < 7.0%, fasting glucose < 120 mg/dL.", color=TEXT_MUTED, fontsize=7)

    save_fig(fig, "screen_trajectory.png")

# 6. Screen: Option 2 Govt Teleconsultation Room
def create_teleconsult_screen():
    fig, ax = plt.subplots(figsize=(6, 10))
    ax.set_facecolor(NAVY)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 160)
    ax.axis('off')

    ax.text(8, 155, "09:47", color=WHITE, fontsize=9, weight='bold')
    ax.text(85, 155, "5G | 96%", color=WHITE, fontsize=9)
    ax.text(8, 145, "eSANJEEVANI & ABDM TELEHEALTH", color=EMERALD, fontsize=8, weight='bold')
    ax.text(8, 137, "Live Govt Video Teleconsultation", color=WHITE, fontsize=13, weight='bold')

    v_box = patches.FancyBboxPatch((8, 62), 84, 70, boxstyle="round,pad=1", ec=BORDER, fc="#070E24", lw=1.5)
    ax.add_patch(v_box)
    
    pb = patches.FancyBboxPatch((14, 122), 34, 5.5, boxstyle="round,pad=0.3", ec=EMERALD, fc="#064E3B")
    ax.add_patch(pb)
    ax.text(31, 124, "[REC] LIVE CONSULTATION · 04:18", color="#6EE7B7", fontsize=6, weight='bold', ha='center')

    ax.text(50, 95, "[DR VIEW]", color=BLUE, fontsize=24, ha='center', weight='bold')
    ax.text(50, 78, "Dr. Clinical Specialist (Lead Diabetologist)", color=WHITE, fontsize=8.5, weight='bold', ha='center')
    ax.text(50, 72, "Midnapore Medical College & Hospital · Apex Tele-Hub", color=TEXT_MUTED, fontsize=6.8, ha='center')

    pip = patches.FancyBboxPatch((64, 88), 24, 22, boxstyle="round,pad=0.5", ec=BORDER, fc="#0F172A", lw=1.2)
    ax.add_patch(pip)
    ax.text(76, 102, "[PAT]", color=EMERALD, fontsize=14, ha='center')
    ax.text(76, 92, "Ramesh C. Sen", color=WHITE, fontsize=6, ha='center')
    ax.text(76, 88, "(Patient Plantar View)", color=TEXT_MUTED, fontsize=5, ha='center')

    ctrl_box = patches.FancyBboxPatch((8, 46), 84, 12, boxstyle="round,pad=0.6", ec=BORDER, fc=CARD_BG)
    ax.add_patch(ctrl_box)
    
    b_mute = patches.Circle((25, 52), 4, color="#334155")
    ax.add_patch(b_mute)
    ax.text(25, 50.8, "MIC", color=WHITE, fontsize=6, ha='center', weight='bold')

    b_cam = patches.Circle((50, 52), 4, color="#334155")
    ax.add_patch(b_cam)
    ax.text(50, 50.8, "CAM", color=WHITE, fontsize=6, ha='center', weight='bold')

    b_end = patches.Circle((75, 52), 4, color=RED)
    ax.add_patch(b_end)
    ax.text(75, 50.8, "END", color=WHITE, fontsize=6, ha='center', weight='bold')

    np_box = patches.FancyBboxPatch((8, 8), 84, 34, boxstyle="round,pad=0.8", ec=BORDER, fc=CARD_BG, lw=1.2)
    ax.add_patch(np_box)
    ax.text(12, 36, "REAL-TIME CLINICAL CONSULTATION NOTES", color=WHITE, fontsize=8, weight='bold')
    
    lines = [
        "• Plantar wound area improved from 5.2 cm2 to 2.15 cm2 (-58.6%).",
        "• Granulation tissue healthy, no active exudate or spreading cellulitis.",
        "• Continue Amoxicillin-Clavulanate 625mg BID x 7 days.",
        "• Schedule follow-up visit with ASHA Manasi Roy next Tuesday.",
    ]
    ny = 30
    for line in lines:
        ax.text(12, ny, line, color=TEXT_MUTED, fontsize=6.8)
        ny -= 5.5

    save_fig(fig, "screen_teleconsult.png")

# 7. System Architecture Diagram
def create_system_arch():
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.set_facecolor(NAVY)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 70)
    ax.axis('off')

    ax.text(50, 65, "DIABETESCARE AI — HYBRID SYSTEM TOPOLOGY", color=WHITE, fontsize=12, weight='bold', ha='center')
    ax.text(50, 60.5, "DPDP Act 2023 Compliant · Edge Mobile App · OpenCV & PyTorch Inference · SQLite Persistence", color=TEXT_MUTED, fontsize=7.5, ha='center')

    b1 = patches.FancyBboxPatch((4, 12), 26, 44, boxstyle="round,pad=0.8", ec=EMERALD, fc=CARD_BG, lw=1.5)
    ax.add_patch(b1)
    ax.text(17, 51, "ANDROID MOBILE", color=EMERALD, fontsize=8.5, weight='bold', ha='center')
    ax.text(17, 45, "React Native 0.73", color=WHITE, fontsize=7.5, ha='center')
    ax.text(17, 39, "3-Photo Protocol Lock", color=TEXT_MUTED, fontsize=6.8, ha='center')
    ax.text(17, 33, "Doctor Manual Diagnosis", color=TEXT_MUTED, fontsize=6.8, ha='center')
    ax.text(17, 27, "Concordance Matching", color=TEXT_MUTED, fontsize=6.8, ha='center')
    ax.text(17, 21, "eSanjeevani WebRTC", color=TEXT_MUTED, fontsize=6.8, ha='center')
    ax.text(17, 15, "Offline Fallback Cache", color=TEXT_MUTED, fontsize=6.8, ha='center')

    ax.annotate("", xy=(37, 34), xytext=(30, 34), arrowprops=dict(arrowstyle="<->", color=WHITE, lw=1.5))
    ax.text(33.5, 36.5, "Wi-Fi LAN / TLS", color=WHITE, fontsize=6, ha='center', weight='bold')
    ax.text(33.5, 30, ":8000 REST", color=TEXT_MUTED, fontsize=5.5, ha='center')

    b2 = patches.FancyBboxPatch((37, 12), 28, 44, boxstyle="round,pad=0.8", ec=BLUE, fc=CARD_BG, lw=1.5)
    ax.add_patch(b2)
    ax.text(51, 51, "FASTAPI MASTER", color=BLUE, fontsize=8.5, weight='bold', ha='center')
    ax.text(51, 45, "Python 3.12 · Port 8000", color=WHITE, fontsize=7.5, ha='center')
    ax.text(51, 39, "Quality & Blur Detection", color=TEXT_MUTED, fontsize=6.8, ha='center')
    ax.text(51, 33, "Hough Calibrant px/mm", color=TEXT_MUTED, fontsize=6.8, ha='center')
    ax.text(51, 27, "Adaptive Segmentation", color=TEXT_MUTED, fontsize=6.8, ha='center')
    ax.text(51, 21, "Wagner ML Classifier", color=TEXT_MUTED, fontsize=6.8, ha='center')
    ax.text(51, 15, "DPDP Audit Logging", color=TEXT_MUTED, fontsize=6.8, ha='center')

    ax.annotate("", xy=(72, 34), xytext=(65, 34), arrowprops=dict(arrowstyle="<->", color=WHITE, lw=1.5))
    ax.text(68.5, 36.5, "Persistent I/O", color=WHITE, fontsize=6, ha='center', weight='bold')

    b3 = patches.FancyBboxPatch((72, 12), 24, 44, boxstyle="round,pad=0.8", ec=AMBER, fc=CARD_BG, lw=1.5)
    ax.add_patch(b3)
    ax.text(84, 51, "LOCAL STORAGE", color=AMBER, fontsize=8.5, weight='bold', ha='center')
    ax.text(84, 45, "SQLite + Disk Folders", color=WHITE, fontsize=7.5, ha='center')
    ax.text(84, 38, "diabetescare.db", color=WHITE, fontsize=7, ha='center', weight='bold')
    ax.text(84, 32, "stored_photos/*.jpg", color=WHITE, fontsize=7, ha='center', weight='bold')
    ax.text(84, 25, "models/*.pth", color=WHITE, fontsize=7, ha='center', weight='bold')
    ax.text(84, 17, "AES-256 Encryption", color=TEXT_MUTED, fontsize=6.5, ha='center')

    save_fig(fig, "screen_system_architecture.png")

if __name__ == "__main__":
    create_login_screen()
    create_triage_screen()
    create_photo_flow_screen()
    create_review_screen()
    create_trajectory_screen()
    create_teleconsult_screen()
    create_system_arch()
    print("All diagrams generated cleanly!")
