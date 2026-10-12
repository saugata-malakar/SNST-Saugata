# build_device_mockups.py
# Publication-grade photorealistic smartphone mockups and UI composites
# for DiabetesCare AI Official User Manual

import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT_DIR = "manual_assets"
os.makedirs(OUT_DIR, exist_ok=True)

# ── Font Loaders ─────────────────────────────────────────────────────────────
FONT_REG_PATH = "C:/Windows/Fonts/segoeui.ttf"
FONT_BOLD_PATH = "C:/Windows/Fonts/segoeuib.ttf"
FONT_MONO_PATH = "C:/Windows/Fonts/consola.ttf"

def get_font(size, bold=False, mono=False):
    path = FONT_MONO_PATH if mono else (FONT_BOLD_PATH if bold else FONT_REG_PATH)
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

# ── Color Palette ────────────────────────────────────────────────────────────
NAVY_BG     = (11, 19, 43, 255)       # #0B132B
CARD_BG     = (17, 28, 56, 255)       # #111C38
CARD_SUB    = (12, 21, 46, 255)       # #0C152E
CARD_BORDER = (35, 53, 94, 255)       # #23355E
BLUE_ACCENT = (37, 99, 235, 255)      # #2563EB
BLUE_LIGHT  = (59, 130, 246, 255)     # #3B82F6
EMERALD     = (16, 185, 129, 255)     # #10B981
EMERALD_BG  = (6, 78, 59, 255)
AMBER       = (245, 158, 11, 255)     # #F59E0B
AMBER_BG    = (120, 53, 15, 255)
RED_ACCENT  = (239, 68, 68, 255)      # #EF4444
RED_BG      = (127, 29, 29, 255)
PURPLE      = (147, 51, 234, 255)     # #9333EA
TEXT_WHITE  = (255, 255, 255, 255)
TEXT_MUTED  = (148, 163, 184, 255)    # #94A3B8
TEXT_DIM    = (100, 116, 139, 255)    # #64748B

# ── Device Chassis Wrapper ───────────────────────────────────────────────────
def wrap_in_phone_mockup(screen_img, target_screen_w=460, target_screen_h=960):
    screen_resized = screen_img.convert("RGBA").resize((target_screen_w, target_screen_h), Image.Resampling.LANCZOS)
    bezel_lr = 22
    bezel_tb = 26
    phone_w = target_screen_w + bezel_lr * 2
    phone_h = target_screen_h + bezel_tb * 2

    shadow_margin = 40
    canvas_w = phone_w + shadow_margin * 2
    canvas_h = phone_h + shadow_margin * 2

    canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))

    # Ambient drop shadow
    shadow = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    phone_rect = [shadow_margin, shadow_margin, shadow_margin + phone_w, shadow_margin + phone_h]
    s_draw.rounded_rectangle(phone_rect, radius=52, fill=(15, 23, 42, 130))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=22))
    canvas.paste(shadow, (0, 10), shadow)

    draw = ImageDraw.Draw(canvas)

    # Physical Buttons
    draw.rounded_rectangle([phone_rect[0] - 4, phone_rect[1] + 160, phone_rect[0] + 1, phone_rect[1] + 215], radius=3, fill=(71, 85, 105, 255))
    draw.rounded_rectangle([phone_rect[0] - 4, phone_rect[1] + 230, phone_rect[0] + 1, phone_rect[1] + 285], radius=3, fill=(71, 85, 105, 255))
    draw.rounded_rectangle([phone_rect[2] - 1, phone_rect[1] + 180, phone_rect[2] + 4, phone_rect[1] + 250], radius=3, fill=(71, 85, 105, 255))

    # Titanium Chassis Outer Edge & Chamfer
    draw.rounded_rectangle(phone_rect, radius=52, fill=(30, 41, 59, 255), outline=(71, 85, 105, 255), width=2)
    inner_bezel = [phone_rect[0] + 2, phone_rect[1] + 2, phone_rect[2] - 2, phone_rect[3] - 2]
    draw.rounded_rectangle(inner_bezel, radius=50, fill=(15, 23, 42, 255))

    screen_x = shadow_margin + bezel_lr
    screen_y = shadow_margin + bezel_tb

    screen_mask = Image.new("L", (target_screen_w, target_screen_h), 0)
    m_draw = ImageDraw.Draw(screen_mask)
    m_draw.rounded_rectangle([0, 0, target_screen_w, target_screen_h], radius=36, fill=255)

    canvas.paste(screen_resized, (screen_x, screen_y), screen_mask)

    # Status Bar overlay
    draw_screen = ImageDraw.Draw(canvas)
    f_stat = get_font(13, bold=True)
    draw_screen.text((screen_x + 32, screen_y + 12), "09:41", font=f_stat, fill=TEXT_WHITE)
    draw_screen.text((screen_x + target_screen_w - 82, screen_y + 12), "5G  98%", font=f_stat, fill=TEXT_WHITE)

    # Speaker slit
    draw.rounded_rectangle([screen_x + target_screen_w // 2 - 30, screen_y - 12, screen_x + target_screen_w // 2 + 30, screen_y - 8], radius=2, fill=(51, 65, 85, 255))

    # Dynamic Island / Camera punch-hole pill
    pill_w = 100
    pill_h = 24
    pill_x = screen_x + (target_screen_w - pill_w) // 2
    pill_y = screen_y + 10
    draw.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h], radius=12, fill=(0, 0, 0, 255))
    lens_x = pill_x + pill_w - 24
    lens_y = pill_y + 4
    draw.ellipse([lens_x, lens_y, lens_x + 16, lens_y + 16], fill=(15, 23, 42, 255), outline=(30, 41, 59, 255), width=1)
    draw.ellipse([lens_x + 5, lens_y + 5, lens_x + 11, lens_y + 11], fill=(37, 99, 235, 255))

    # Bottom Home Bar Indicator
    bar_w = 140
    bar_h = 4
    bar_x = screen_x + (target_screen_w - bar_w) // 2
    bar_y = screen_y + target_screen_h - 15
    draw.rounded_rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], radius=2, fill=(203, 213, 225, 220))

    return canvas

def wrap_in_tablet_mockup(screen_img, target_screen_w=920, target_screen_h=640):
    screen_resized = screen_img.convert("RGBA").resize((target_screen_w, target_screen_h), Image.Resampling.LANCZOS)
    bezel = 26
    tab_w = target_screen_w + bezel * 2
    tab_h = target_screen_h + bezel * 2
    shadow_margin = 38

    canvas_w = tab_w + shadow_margin * 2
    canvas_h = tab_h + shadow_margin * 2

    canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))

    shadow = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    tab_rect = [shadow_margin, shadow_margin, shadow_margin + tab_w, shadow_margin + tab_h]
    s_draw.rounded_rectangle(tab_rect, radius=38, fill=(15, 23, 42, 135))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=24))
    canvas.paste(shadow, (0, 12), shadow)

    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle(tab_rect, radius=38, fill=(30, 41, 59, 255), outline=(71, 85, 105, 255), width=2)
    inner_rect = [tab_rect[0] + 2, tab_rect[1] + 2, tab_rect[2] - 2, tab_rect[3] - 2]
    draw.rounded_rectangle(inner_rect, radius=36, fill=(15, 23, 42, 255))

    screen_x = shadow_margin + bezel
    screen_y = shadow_margin + bezel
    mask = Image.new("L", (target_screen_w, target_screen_h), 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.rounded_rectangle([0, 0, target_screen_w, target_screen_h], radius=22, fill=255)
    canvas.paste(screen_resized, (screen_x, screen_y), mask)

    cam_x = shadow_margin + tab_w // 2
    cam_y = shadow_margin + bezel // 2
    draw.ellipse([cam_x - 5, cam_y - 5, cam_x + 5, cam_y + 5], fill=(0, 0, 0, 255), outline=(51, 65, 85, 255), width=1)

    return canvas

# ── Screen Generator Helpers ─────────────────────────────────────────────────
W = 460
H = 960

def create_base_screen():
    img = Image.new("RGBA", (W, H), NAVY_BG)
    draw = ImageDraw.Draw(img)
    return img, draw

# 1. Screen: Portal Login
def build_screen_login():
    img, draw = create_base_screen()

    # Brand Header
    logo_y = 65
    draw.ellipse([W//2 - 32, logo_y, W//2 + 32, logo_y + 64], fill=(30, 58, 138, 255), outline=BLUE_ACCENT, width=2)
    draw.text((W//2, logo_y + 32), "+", font=get_font(34, bold=True), fill=TEXT_WHITE, anchor="mm")

    draw.text((W//2, logo_y + 88), "DiabetesCare AI", font=get_font(24, bold=True), fill=TEXT_WHITE, anchor="mm")
    draw.text((W//2, logo_y + 116), "Clinical Triage & Wound Monitoring", font=get_font(13), fill=TEXT_MUTED, anchor="mm")
    draw.text((W//2, logo_y + 138), "IIT Kharagpur · Paschim Medinipur Apex Hub", font=get_font(11, bold=True), fill=EMERALD, anchor="mm")

    # Persona Selector Card
    card_y = 240
    draw.rounded_rectangle([20, card_y, W - 20, card_y + 330], radius=16, fill=CARD_BG, outline=CARD_BORDER, width=1)
    draw.text((36, card_y + 18), "SELECT CLINICAL ACCESS PERSONA", font=get_font(11, bold=True), fill=TEXT_MUTED)

    personas = [
        ("[DR] Lead Diabetologist", "Full Clinical Triage & Validation", RED_ACCENT, True),
        ("[PT] Enrolled Patient", "Self-Monitoring & Healing Journey", EMERALD, False),
        ("[HW] ASHA Health Worker", "Field Screening & Offline Queue", BLUE_ACCENT, False),
        ("[AD] Hospital Administrator", "Audit Logs & Master Registry", AMBER, False)
    ]
    p_y = card_y + 48
    for title, sub, col, active in personas:
        bg = col if active else CARD_SUB
        border = col if active else CARD_BORDER
        draw.rounded_rectangle([32, p_y, W - 32, p_y + 56], radius=10, fill=bg, outline=border, width=1)
        draw.text((46, p_y + 16), title, font=get_font(13, bold=True), fill=TEXT_WHITE if active else TEXT_WHITE)
        draw.text((46, p_y + 34), sub, font=get_font(10), fill=TEXT_WHITE if active else TEXT_MUTED)
        if active:
            draw.rounded_rectangle([W - 110, p_y + 16, W - 44, p_y + 40], radius=6, fill=(15, 23, 42, 200))
            draw.text((W - 77, p_y + 28), "ACTIVE", font=get_font(10, bold=True), fill=TEXT_WHITE, anchor="mm")
        p_y += 66

    # Credentials Card
    cred_y = card_y + 350
    draw.rounded_rectangle([20, cred_y, W - 20, cred_y + 175], radius=16, fill=CARD_BG, outline=CARD_BORDER, width=1)
    draw.text((36, cred_y + 18), "AUTHORIZED CREDENTIALS (RBAC)", font=get_font(11, bold=True), fill=TEXT_MUTED)

    # Input 1
    draw.rounded_rectangle([32, cred_y + 42, W - 32, cred_y + 88], radius=8, fill=CARD_SUB, outline=CARD_BORDER, width=1)
    draw.text((46, cred_y + 54), "doctor@demo.in (Lead Diabetologist)", font=get_font(12), fill=TEXT_WHITE)
    draw.text((46, cred_y + 70), "Verified Identity · MMC&H Paschim Medinipur", font=get_font(9), fill=TEXT_DIM)

    # Input 2
    draw.rounded_rectangle([32, cred_y + 98, W - 32, cred_y + 144], radius=8, fill=CARD_SUB, outline=CARD_BORDER, width=1)
    draw.text((46, cred_y + 110), "••••••••••••••••", font=get_font(14), fill=TEXT_WHITE)
    draw.text((46, cred_y + 126), "Hardware Keystore · TLS 1.3 End-to-End", font=get_font(9), fill=EMERALD)

    # Submit Button
    btn_y = cred_y + 195
    draw.rounded_rectangle([20, btn_y, W - 20, btn_y + 58], radius=12, fill=BLUE_ACCENT)
    draw.text((W//2, btn_y + 29), "Sign In to Command Portal  ->", font=get_font(15, bold=True), fill=TEXT_WHITE, anchor="mm")

    # Bottom status
    draw.text((W//2, btn_y + 80), "Connected: http://192.168.31.94:8000 (FastAPI Master)", font=get_font(10, mono=True), fill=TEXT_DIM, anchor="mm")
    draw.text((W//2, btn_y + 98), "DPDP Act 2023 · CDSCO Class B Medical Device Software", font=get_font(9), fill=TEXT_MUTED, anchor="mm")

    return wrap_in_phone_mockup(img)

# 2. Screen: Mandatory 3-Photo Checklist & Protocol Lock [Bug Fix #1]
def build_screen_3photo_lock():
    img, draw = create_base_screen()

    # Header
    draw.text((24, 55), "CLINICAL PHOTO CAPTURE", font=get_font(11, bold=True), fill=RED_ACCENT)
    draw.text((24, 76), "3-Photo Protocol Verification", font=get_font(18, bold=True), fill=TEXT_WHITE)
    draw.text((24, 102), "Patient: Subhash Mondal (PAT-KGP-004) · Visit #4", font=get_font(11), fill=TEXT_MUTED)

    # Protocol Lock Alert Banner (Bug Fix #1)
    banner_y = 130
    draw.rounded_rectangle([20, banner_y, W - 20, banner_y + 115], radius=12, fill=(69, 10, 10, 255), outline=RED_ACCENT, width=2)
    draw.text((36, banner_y + 18), "MANDATORY 3-PHOTO CLINICAL LOCK [ACTIVE]", font=get_font(12, bold=True), fill=RED_ACCENT)
    info_text = (
        "Strict CDSCO Tri-Plane Protocol Enforced:\n"
        "AI diagnostic pipeline strictly prohibits single-photograph\n"
        "submissions. Three distinct angles required for volumetric,\n"
        "depth, and scale validation before review is unlocked."
    )
    draw.text((36, banner_y + 42), info_text, font=get_font(10.5), fill=(254, 202, 202, 255), spacing=3)

    # 3 Photo Cards
    cards_y = banner_y + 130
    photos = [
        ("PHOTO 1 OF 3: PLANTAR OVERVIEW", "90° Orthogonal Alignment (30 cm)", "Status: CAPTURED & VALIDATED", EMERALD, EMERALD_BG, True),
        ("PHOTO 2 OF 3: 45° OBLIQUE LATERAL", "Depth profiling & margin evaluation", "Status: CAPTURED & VALIDATED", EMERALD, EMERALD_BG, True),
        ("PHOTO 3 OF 3: CALIBRATED CLOSE-UP", "Macro inspection with 24mm calibrant coin", "Status: PENDING CAPTURE...", AMBER, CARD_SUB, False),
    ]
    p_y = cards_y
    for title, sub, stat, col, bg_col, comp in photos:
        draw.rounded_rectangle([20, p_y, W - 20, p_y + 115], radius=14, fill=CARD_BG, outline=col if comp else CARD_BORDER, width=2)
        # Left status indicator strip
        draw.rounded_rectangle([20, p_y, 28, p_y + 115], radius=3, fill=col)

        draw.text((40, p_y + 16), title, font=get_font(12, bold=True), fill=TEXT_WHITE)
        draw.text((40, p_y + 36), sub, font=get_font(10.5), fill=TEXT_MUTED)

        # Status badge
        draw.rounded_rectangle([40, p_y + 60, W - 36, p_y + 96], radius=8, fill=bg_col, outline=col, width=1)
        check_icon = "[OK]" if comp else "[WAITING]"
        draw.text((54, p_y + 78), f"{check_icon}  {stat}", font=get_font(11, bold=True), fill=col, anchor="lm")
        p_y += 128

    # Bottom Submission Status (Locked state)
    bot_y = p_y + 15
    draw.rounded_rectangle([20, bot_y, W - 20, bot_y + 70], radius=12, fill=CARD_BG, outline=CARD_BORDER, width=1)
    draw.text((W//2, bot_y + 24), "REVIEW SUBMISSION LOCKED (2 OF 3 COMPLETED)", font=get_font(11, bold=True), fill=AMBER, anchor="mm")
    draw.text((W//2, bot_y + 46), "Capture remaining close-up image to enable AI analysis", font=get_font(10), fill=TEXT_MUTED, anchor="mm")

    # Action button (Greyed out)
    btn_y = bot_y + 85
    draw.rounded_rectangle([20, btn_y, W - 20, btn_y + 54], radius=12, fill=(51, 65, 85, 255))
    draw.text((W//2, btn_y + 27), "[LOCKED] Proceed to Clinical Review (3/3 Required)", font=get_font(12, bold=True), fill=TEXT_MUTED, anchor="mm")

    return wrap_in_phone_mockup(img)

# 3. Screen: Doctor Manual Diagnosis & AI Concordance Matching [Bug Fix #2]
def build_screen_doctor_diagnosis():
    img, draw = create_base_screen()

    # Header
    draw.text((24, 55), "CLINICAL REVIEW & DIAGNOSIS", font=get_font(11, bold=True), fill=EMERALD)
    draw.text((24, 76), "AI Predictions & Manual Validation", font=get_font(18, bold=True), fill=TEXT_WHITE)
    draw.text((24, 102), "Session: SES-20261001-004 · Dr. Aris Banerjee, MD", font=get_font(11), fill=TEXT_MUTED)

    # AI Model Prediction Card
    ai_y = 125
    draw.rounded_rectangle([20, ai_y, W - 20, ai_y + 140], radius=14, fill=CARD_BG, outline=BLUE_ACCENT, width=2)
    draw.text((36, ai_y + 16), "AI DEEP LEARNING INFERENCE RESULT", font=get_font(11, bold=True), fill=BLUE_LIGHT)

    # Metrics row
    m_box_w = (W - 40 - 24) // 3
    metrics = [
        ("Wagner Grade", "Grade 2", EMERALD),
        ("Cellulitis", "Negative (0.12)", BLUE_LIGHT),
        ("Ulcer Area", "3.84 cm²", AMBER)
    ]
    for i, (label, val, col) in enumerate(metrics):
        bx = 32 + i * (m_box_w + 8)
        draw.rounded_rectangle([bx, ai_y + 42, bx + m_box_w, ai_y + 115], radius=8, fill=CARD_SUB, outline=CARD_BORDER, width=1)
        draw.text((bx + m_box_w//2, ai_y + 60), label, font=get_font(10), fill=TEXT_MUTED, anchor="mm")
        draw.text((bx + m_box_w//2, ai_y + 88), val, font=get_font(12, bold=True), fill=col, anchor="mm")

    # Mandatory Doctor Diagnosis Card (Bug Fix #2)
    diag_y = ai_y + 155
    draw.rounded_rectangle([20, diag_y, W - 20, diag_y + 250], radius=14, fill=CARD_BG, outline=RED_ACCENT, width=2)
    draw.text((36, diag_y + 16), "DOCTOR MANUAL CLINICAL DIAGNOSIS [MANDATORY]", font=get_font(11, bold=True), fill=RED_ACCENT)
    draw.text((36, diag_y + 36), "Physician clinical impression matched against AI models:", font=get_font(10), fill=TEXT_MUTED)

    # Doctor text input box
    inp_y = diag_y + 58
    draw.rounded_rectangle([32, inp_y, W - 32, inp_y + 110], radius=8, fill=CARD_SUB, outline=BLUE_ACCENT, width=2)
    doc_note = (
        "Neuropathic ulcer on 1st metatarsal head.\n"
        "Wagner Grade 2 confirmed. Healthy granulation\n"
        "tissue (~65%), mild peripheral erythema.\n"
        "No deep fascial involvement. Hydrocolloid dress."
    )
    draw.text((44, inp_y + 14), doc_note, font=get_font(11), fill=TEXT_WHITE, spacing=4)

    # Live Concordance Badge (Bug Fix #2)
    badge_y = inp_y + 125
    draw.rounded_rectangle([32, badge_y, W - 32, badge_y + 50], radius=10, fill=EMERALD_BG, outline=EMERALD, width=2)
    draw.text((48, badge_y + 25), "★ 98.4% CONCORDANCE [EXCELLENT MATCH]", font=get_font(12, bold=True), fill=EMERALD, anchor="lm")
    draw.text((W - 48, badge_y + 25), "AI & MD ALIGNED", font=get_font(10, bold=True), fill=TEXT_WHITE, anchor="rm")

    # Synchronous Commit Note (Bug Fix #3)
    sync_y = diag_y + 265
    draw.rounded_rectangle([20, sync_y, W - 20, sync_y + 70], radius=12, fill=CARD_BG, outline=CARD_BORDER, width=1)
    draw.text((36, sync_y + 16), "SYNCHRONOUS DOCTOR HUB REFLECTION [READY]", font=get_font(11, bold=True), fill=EMERALD)
    draw.text((36, sync_y + 38), "Immediate atomic commit to database & instant dashboard update.", font=get_font(10), fill=TEXT_MUTED)

    # Submit Button
    btn_y = sync_y + 85
    draw.rounded_rectangle([20, btn_y, W - 20, btn_y + 54], radius=12, fill=EMERALD)
    draw.text((W//2, btn_y + 27), "Submit Diagnosis & Reflect to Doctor Hub ->", font=get_font(13, bold=True), fill=TEXT_WHITE, anchor="mm")

    return wrap_in_phone_mockup(img)

# 4. Screen: Doctor Account Live Data Reflection [Bug Fix #3]
def build_screen_doctor_reflection():
    img, draw = create_base_screen()

    # Header
    draw.text((24, 55), "DOCTOR COMMAND HUB", font=get_font(11, bold=True), fill=RED_ACCENT)
    draw.text((24, 76), "Live Patient Triage Roster", font=get_font(18, bold=True), fill=TEXT_WHITE)
    draw.text((24, 102), "Paschim Medinipur Apex Center · MMC&H", font=get_font(11), fill=TEXT_MUTED)

    # Live Sync Indicator Banner (Bug Fix #3)
    syn_y = 125
    draw.rounded_rectangle([20, syn_y, W - 20, syn_y + 55], radius=10, fill=EMERALD_BG, outline=EMERALD, width=1)
    draw.text((36, syn_y + 27), "● REAL-TIME SYNCHRONIZED: SUBMISSION REFLECTED", font=get_font(11, bold=True), fill=EMERALD, anchor="lm")
    draw.text((W - 36, syn_y + 27), "0s ago", font=get_font(11, bold=True), fill=TEXT_WHITE, anchor="rm")

    # Newly Reflected Patient Card (Highlighted)
    c1_y = syn_y + 70
    draw.rounded_rectangle([20, c1_y, W - 20, c1_y + 185], radius=14, fill=CARD_BG, outline=EMERALD, width=2)
    # Status pill
    draw.rounded_rectangle([32, c1_y + 16, 175, c1_y + 38], radius=6, fill=EMERALD)
    draw.text((103, c1_y + 27), "JUST SUBMITTED · REFLECTED", font=get_font(9, bold=True), fill=TEXT_WHITE, anchor="mm")

    draw.text((W - 36, c1_y + 27), "PAT-KGP-004", font=get_font(12, bold=True), fill=TEXT_WHITE, anchor="rm")
    draw.text((32, c1_y + 52), "Subhash Mondal", font=get_font(16, bold=True), fill=TEXT_WHITE)
    draw.text((32, c1_y + 74), "58M · Midnapore Rural · Diabetology OPD", font=get_font(11), fill=TEXT_MUTED)

    # Details
    draw.rounded_rectangle([32, c1_y + 95, W - 32, c1_y + 165], radius=8, fill=CARD_SUB, outline=CARD_BORDER, width=1)
    draw.text((44, c1_y + 112), "Wagner Grade: Grade 2 (Deep Ulcer)", font=get_font(11, bold=True), fill=TEXT_WHITE)
    draw.text((44, c1_y + 130), "Doctor Diagnosis: Neuropathic ulcer, Granulation 65%", font=get_font(10), fill=EMERALD)
    draw.text((44, c1_y + 148), "Concordance: 98.4% Match · 3-Photo Protocol Complete", font=get_font(10), fill=BLUE_LIGHT)

    # Cohort Patient Card 2
    c2_y = c1_y + 200
    draw.rounded_rectangle([20, c2_y, W - 20, c2_y + 145], radius=14, fill=CARD_BG, outline=CARD_BORDER, width=1)
    draw.rounded_rectangle([32, c2_y + 16, 140, c2_y + 38], radius=6, fill=RED_BG, outline=RED_ACCENT, width=1)
    draw.text((86, c2_y + 27), "URGENT TRIAGE", font=get_font(9, bold=True), fill=RED_ACCENT, anchor="mm")
    draw.text((W - 36, c2_y + 27), "PAT-KGP-002", font=get_font(12, bold=True), fill=TEXT_WHITE, anchor="rm")
    draw.text((32, c2_y + 52), "Rameshwar Sen", font=get_font(15, bold=True), fill=TEXT_WHITE)
    draw.text((32, c2_y + 72), "64M · Kharagpur Sub-Divisional Hospital", font=get_font(11), fill=TEXT_MUTED)
    draw.text((32, c2_y + 96), "Wagner Grade 4 (Gangrene Suspected) · Cellulitis POSITIVE", font=get_font(11, bold=True), fill=RED_ACCENT)
    draw.text((32, c2_y + 118), "Escalation: Immediate Surgical Debridement Referral", font=get_font(10), fill=AMBER)

    # Cohort Patient Card 3
    c3_y = c2_y + 160
    draw.rounded_rectangle([20, c3_y, W - 20, c3_y + 145], radius=14, fill=CARD_BG, outline=CARD_BORDER, width=1)
    draw.rounded_rectangle([32, c3_y + 16, 140, c3_y + 38], radius=6, fill=BLUE_ACCENT)
    draw.text((86, c3_y + 27), "ROUTINE FOLLOW-UP", font=get_font(9, bold=True), fill=TEXT_WHITE, anchor="mm")
    draw.text((W - 36, c3_y + 27), "PAT-KGP-001", font=get_font(12, bold=True), fill=TEXT_WHITE, anchor="rm")
    draw.text((32, c3_y + 52), "Anjali Devi", font=get_font(15, bold=True), fill=TEXT_WHITE)
    draw.text((32, c3_y + 72), "52F · Debra Rural Block Health Center", font=get_font(11), fill=TEXT_MUTED)
    draw.text((32, c3_y + 96), "Wagner Grade 1 (Superficial Ulcer) · Healing +24%", font=get_font(11, bold=True), fill=EMERALD)
    draw.text((32, c3_y + 118), "Teleconsultation: Completed on eSanjeevani", font=get_font(10), fill=TEXT_MUTED)

    # Quick Action Strip
    btn_y = c3_y + 160
    draw.rounded_rectangle([20, btn_y, W - 20, btn_y + 52], radius=12, fill=BLUE_ACCENT)
    draw.text((W//2, btn_y + 26), "Open Full Triage Dossier (All 4 Cohort Cases)", font=get_font(13, bold=True), fill=TEXT_WHITE, anchor="mm")

    return wrap_in_phone_mockup(img)

# 5. Screen: Option 1 - My Healing Journey (Patient Experience)
def build_screen_healing_journey():
    img, draw = create_base_screen()

    # Header
    draw.text((24, 55), "PATIENT CARE PORTAL", font=get_font(11, bold=True), fill=EMERALD)
    draw.text((24, 76), "My Healing Journey", font=get_font(18, bold=True), fill=TEXT_WHITE)
    draw.text((24, 102), "Namaste, Subhash Mondal (PAT-KGP-004)", font=get_font(11), fill=TEXT_MUTED)

    # Trajectory Card
    t_y = 125
    draw.rounded_rectangle([20, t_y, W - 20, t_y + 200], radius=16, fill=CARD_BG, outline=CARD_BORDER, width=1)
    draw.text((36, t_y + 18), "HEALING TRAJECTORY OVERVIEW", font=get_font(11, bold=True), fill=TEXT_MUTED)
    draw.text((36, t_y + 40), "+18.2% Healing Progress", font=get_font(20, bold=True), fill=EMERALD)
    draw.text((36, t_y + 68), "Wound area reduced from 4.7 cm² to 3.84 cm² (14 Days)", font=get_font(11), fill=TEXT_MUTED)

    # Progress bar
    draw.rounded_rectangle([36, t_y + 95, W - 36, t_y + 115], radius=10, fill=CARD_SUB)
    draw.rounded_rectangle([36, t_y + 95, 36 + int((W - 72) * 0.68), t_y + 115], radius=10, fill=EMERALD)
    draw.text((W - 40, t_y + 130), "68% Epithelialized", font=get_font(11, bold=True), fill=EMERALD, anchor="rm")

    # Key stats
    draw.text((36, t_y + 155), "Current Wagner Grade: Grade 2", font=get_font(12, bold=True), fill=TEXT_WHITE)
    draw.text((36, t_y + 175), "Target: Grade 0 (Full Epithelial Closure by Week 8)", font=get_font(10.5), fill=BLUE_LIGHT)

    # Daily Care Checklist
    care_y = t_y + 220
    draw.rounded_rectangle([20, care_y, W - 20, care_y + 250], radius=16, fill=CARD_BG, outline=CARD_BORDER, width=1)
    draw.text((36, care_y + 18), "TODAY'S DIABETIC FOOT PROTOCOL", font=get_font(11, bold=True), fill=TEXT_MUTED)

    tasks = [
        ("[x] Morning Foot Inspection & Wash", "Tepid water wash completed · No maceration", EMERALD, True),
        ("[x] Dressing Renewal (Hydrocolloid)", "Clean sterile dressing applied · Doctor prescribed", EMERALD, True),
        ("[ ] Evening Offloading Footwear Check", "Wear custom therapeutic sandals indoors", AMBER, False),
        ("[ ] Fasting Blood Sugar Log", "Record morning reading before breakfast", BLUE_LIGHT, False)
    ]
    k_y = care_y + 46
    for t_title, t_sub, col, comp in tasks:
        draw.rounded_rectangle([32, k_y, W - 32, k_y + 44], radius=8, fill=CARD_SUB, outline=col if comp else CARD_BORDER, width=1)
        draw.text((44, k_y + 12), t_title, font=get_font(11, bold=True), fill=TEXT_WHITE if comp else TEXT_MUTED)
        draw.text((44, k_y + 28), t_sub, font=get_font(9.5), fill=TEXT_MUTED)
        k_y += 50

    # Emergency SOS & Teleconsult Buttons
    sos_y = care_y + 265
    draw.rounded_rectangle([20, sos_y, W - 20, sos_y + 54], radius=12, fill=EMERALD_BG, outline=EMERALD, width=2)
    draw.text((W//2, sos_y + 27), "Open Teleconsultation with Doctor ->", font=get_font(13, bold=True), fill=EMERALD, anchor="mm")

    sos2_y = sos_y + 64
    draw.rounded_rectangle([20, sos2_y, W - 20, sos2_y + 54], radius=12, fill=RED_BG, outline=RED_ACCENT, width=2)
    draw.text((W//2, sos2_y + 27), "SOS Emergency Hotline / ASHA Helpdesk", font=get_font(13, bold=True), fill=RED_ACCENT, anchor="mm")

    return wrap_in_phone_mockup(img)

# 6. Screen: Option 2 - National Teleconsultation Network (eSanjeevani)
def build_screen_teleconsult():
    img, draw = create_base_screen()

    # Header
    draw.text((24, 55), "NATIONAL TELECONSULTATION", font=get_font(11, bold=True), fill=BLUE_LIGHT)
    draw.text((24, 76), "eSanjeevani 2.0 Video Room", font=get_font(18, bold=True), fill=TEXT_WHITE)
    draw.text((24, 102), "ABDM M4 Integration · ABHA ID: 91-4521-8890-1234", font=get_font(10.5), fill=TEXT_MUTED)

    # Video Feed Window
    v_y = 125
    v_h = 240
    draw.rounded_rectangle([20, v_y, W - 20, v_y + v_h], radius=16, fill=(15, 23, 42, 255), outline=BLUE_ACCENT, width=2)
    # Doctor video representation
    draw.text((W//2, v_y + 80), "[DOCTOR LIVE FEED]", font=get_font(14, bold=True), fill=TEXT_MUTED, anchor="mm")
    draw.text((W//2, v_y + 105), "Dr. Aris Banerjee, MD (Diabetology)", font=get_font(13, bold=True), fill=TEXT_WHITE, anchor="mm")
    draw.text((W//2, v_y + 125), "Midnapore Medical College & Hospital", font=get_font(11), fill=EMERALD, anchor="mm")

    # Patient PIP window
    pip_w = 110
    pip_h = 75
    draw.rounded_rectangle([W - 36 - pip_w, v_y + v_h - 16 - pip_h, W - 36, v_y + v_h - 16], radius=10, fill=CARD_BG, outline=EMERALD, width=2)
    draw.text((W - 36 - pip_w//2, v_y + v_h - 16 - pip_h//2), "Self Video", font=get_font(10, bold=True), fill=TEXT_WHITE, anchor="mm")

    # Live Call Controls Pill
    draw.rounded_rectangle([36, v_y + 16, 120, v_y + 40], radius=8, fill=EMERALD_BG)
    draw.text((96, v_y + 28), "● 12:45 LIVE", font=get_font(10, bold=True), fill=EMERALD, anchor="mm")

    # Real-Time IoT Vitals Strip
    vit_y = v_y + v_h + 15
    draw.rounded_rectangle([20, vit_y, W - 20, vit_y + 115], radius=14, fill=CARD_BG, outline=CARD_BORDER, width=1)
    draw.text((36, vit_y + 16), "LIVE TELEMETRY & PATIENT VITALS (IoT GATEWAY)", font=get_font(11, bold=True), fill=TEXT_MUTED)

    v_col_w = (W - 40 - 24) // 3
    vitals = [
        ("SpO2", "98%", EMERALD),
        ("Blood Glucose", "138 mg/dL", BLUE_LIGHT),
        ("Skin Temp", "98.4°F", AMBER)
    ]
    for i, (v_label, v_val, v_col) in enumerate(vitals):
        vx = 32 + i * (v_col_w + 8)
        draw.rounded_rectangle([vx, vit_y + 38, vx + v_col_w, vit_y + 98], radius=8, fill=CARD_SUB, outline=CARD_BORDER, width=1)
        draw.text((vx + v_col_w//2, vit_y + 54), v_label, font=get_font(9.5), fill=TEXT_MUTED, anchor="mm")
        draw.text((vx + v_col_w//2, vit_y + 78), v_val, font=get_font(12, bold=True), fill=v_col, anchor="mm")

    # Prescription & Clinical Chat Card
    chat_y = vit_y + 130
    draw.rounded_rectangle([20, chat_y, W - 20, chat_y + 180], radius=14, fill=CARD_BG, outline=CARD_BORDER, width=1)
    draw.text((36, chat_y + 16), "DIGITAL PRESCRIPTION & CLINICAL ORDERS", font=get_font(11, bold=True), fill=TEXT_MUTED)

    orders = (
        "1. Hydrocolloid Dressing - Apply every 48 hours\n"
        "2. Offloading Therapeutic Footwear - Mandatory\n"
        "3. Tab. Metformin 500mg BD after meals\n"
        "4. Follow-up 3-Photo capture scheduled for Day 21"
    )
    draw.text((36, chat_y + 44), orders, font=get_font(11), fill=TEXT_WHITE, spacing=5)

    # Call End & Prescribe Buttons
    btn_y = chat_y + 195
    draw.rounded_rectangle([20, btn_y, W - 20, btn_y + 52], radius=12, fill=BLUE_ACCENT)
    draw.text((W//2, btn_y + 26), "Download Digitally Signed Prescription (ABDM) ->", font=get_font(12, bold=True), fill=TEXT_WHITE, anchor="mm")

    return wrap_in_phone_mockup(img)

# 7. Screen: Option 4 - Neuropathy Foot Map & 30-Day Trajectory
def build_screen_monofilament_trajectory():
    img, draw = create_base_screen()

    # Header
    draw.text((24, 55), "DIABETIC NEUROPATHY DOSSIER", font=get_font(11, bold=True), fill=PURPLE)
    draw.text((24, 76), "10-Point Sensory Mapping & Curve", font=get_font(18, bold=True), fill=TEXT_WHITE)
    draw.text((24, 102), "Semmes-Weinstein 10g Monofilament Protocol", font=get_font(11), fill=TEXT_MUTED)

    # Foot Anatomy & 10-Point Diagram Card
    foot_y = 125
    draw.rounded_rectangle([20, foot_y, W - 20, foot_y + 280], radius=16, fill=CARD_BG, outline=CARD_BORDER, width=1)
    draw.text((36, foot_y + 18), "PLANTAR SENSITIVITY PROFILE (RIGHT FOOT)", font=get_font(11, bold=True), fill=TEXT_MUTED)

    # Foot silhouette
    fx = W // 2
    fy = foot_y + 145
    # Draw heel & ball of foot
    draw.ellipse([fx - 55, fy - 80, fx + 55, fy + 40], fill=CARD_SUB, outline=CARD_BORDER, width=2)
    draw.ellipse([fx - 38, fy + 20, fx + 38, fy + 95], fill=CARD_SUB, outline=CARD_BORDER, width=2)

    # 10 Test Points
    points = [
        (fx - 28, fy - 65, "1", RED_ACCENT),  # Hallux (Loss of sensation)
        (fx - 8, fy - 68, "2", RED_ACCENT),   # 3rd toe
        (fx + 16, fy - 62, "3", EMERALD),     # 5th toe
        (fx - 34, fy - 35, "4", RED_ACCENT),  # 1st metatarsal head (Ulcer site!)
        (fx, fy - 35, "5", RED_ACCENT),       # 3rd metatarsal head
        (fx + 32, fy - 35, "6", EMERALD),     # 5th metatarsal head
        (fx - 24, fy + 5, "7", EMERALD),      # Medial midfoot
        (fx + 24, fy + 5, "8", EMERALD),      # Lateral midfoot
        (fx - 14, fy + 55, "9", EMERALD),     # Medial heel
        (fx + 14, fy + 55, "10", EMERALD),    # Lateral heel
    ]
    for px, py, num, col in points:
        draw.ellipse([px - 11, py - 11, px + 11, py + 11], fill=col)
        draw.text((px, py), num, font=get_font(10, bold=True), fill=TEXT_WHITE, anchor="mm")

    # Legend
    draw.rounded_rectangle([36, foot_y + 235, W - 36, foot_y + 265], radius=6, fill=CARD_SUB)
    draw.text((48, foot_y + 250), "● Normal Sensation (6/10)", font=get_font(10, bold=True), fill=EMERALD, anchor="lm")
    draw.text((W - 48, foot_y + 250), "● Sensory Deficit (4/10)", font=get_font(10, bold=True), fill=RED_ACCENT, anchor="rm")

    # 30-Day Wound Regression Curve Card
    traj_y = foot_y + 295
    draw.rounded_rectangle([20, traj_y, W - 20, traj_y + 210], radius=16, fill=CARD_BG, outline=CARD_BORDER, width=1)
    draw.text((36, traj_y + 18), "30-DAY WOUND AREA REGRESSION (cm²)", font=get_font(11, bold=True), fill=TEXT_MUTED)

    # Line chart representation
    cx0, cy0 = 50, traj_y + 155
    cx1, cy1 = W - 50, traj_y + 60
    # Axes
    draw.line([cx0, cy0, cx1, cy0], fill=CARD_BORDER, width=1)
    draw.line([cx0, cy0, cx0, cy1], fill=CARD_BORDER, width=1)

    chart_pts = [
        (cx0, cy0 - 75, "5.2 cm² (Day 1)"),
        (cx0 + 80, cy0 - 58, "4.7 cm² (Day 7)"),
        (cx0 + 170, cy0 - 45, "4.1 cm² (Day 14)"),
        (cx0 + 260, cy0 - 32, "3.84 cm² (Day 21)"),
        (cx1, cy0 - 15, "Target: 2.1 cm²"),
    ]
    for i in range(len(chart_pts) - 1):
        x1, y1, _ = chart_pts[i]
        x2, y2, _ = chart_pts[i+1]
        draw.line([x1, y1, x2, y2], fill=EMERALD, width=3)
        draw.ellipse([x1 - 4, y1 - 4, x1 + 4, y1 + 4], fill=EMERALD)
    draw.ellipse([chart_pts[-1][0] - 4, chart_pts[-1][1] - 4, chart_pts[-1][0] + 4, chart_pts[-1][1] + 4], fill=AMBER)

    draw.text((cx0, cy0 + 12), "Day 1", font=get_font(9), fill=TEXT_MUTED)
    draw.text((cx0 + 120, cy0 + 12), "Day 14", font=get_font(9), fill=TEXT_MUTED)
    draw.text((cx0 + 240, cy0 + 12), "Day 21 (Today)", font=get_font(9, bold=True), fill=EMERALD)
    draw.text((cx1 - 20, cy0 + 12), "Day 30", font=get_font(9), fill=TEXT_MUTED)

    draw.text((36, traj_y + 180), "Clinical Trend: Steady Epithelial Contraction (-26.1% Overall)", font=get_font(10.5, bold=True), fill=EMERALD)

    # Action Button
    btn_y = traj_y + 225
    draw.rounded_rectangle([20, btn_y, W - 20, btn_y + 52], radius=12, fill=BLUE_ACCENT)
    draw.text((W//2, btn_y + 26), "Export Full Longitudinal Neuropathy Report ->", font=get_font(12, bold=True), fill=TEXT_WHITE, anchor="mm")

    return wrap_in_phone_mockup(img)

# 8. Screen: ASHA Field Worker Offline Queue & Sync
def build_screen_asha_offline_queue():
    img, draw = create_base_screen()

    # Header
    draw.text((24, 55), "ASHA FIELD WORKER PORTAL", font=get_font(11, bold=True), fill=AMBER)
    draw.text((24, 76), "Offline Queue & Sync Engine", font=get_font(18, bold=True), fill=TEXT_WHITE)
    draw.text((24, 102), "Sector: Debra Rural · ASHA Worker: Priya Das", font=get_font(11), fill=TEXT_MUTED)

    # Sync Status Card
    sync_y = 125
    draw.rounded_rectangle([20, sync_y, W - 20, sync_y + 140], radius=16, fill=CARD_BG, outline=AMBER, width=2)
    draw.text((36, sync_y + 18), "LOCAL SQLITE ENCRYPTED QUEUE", font=get_font(11, bold=True), fill=AMBER)
    draw.text((36, sync_y + 44), "3 Clinical Sessions Pending Sync", font=get_font(18, bold=True), fill=TEXT_WHITE)
    draw.text((36, sync_y + 74), "Encrypted via SQLCipher (AES-256 GCM) on device storage", font=get_font(10.5), fill=TEXT_MUTED)

    # Network condition pill
    draw.rounded_rectangle([36, sync_y + 98, 220, sync_y + 124], radius=6, fill=AMBER_BG)
    draw.text((128, sync_y + 111), "NETWORK: 2G / EDGE DETECTED", font=get_font(9.5, bold=True), fill=AMBER, anchor="mm")

    # Queue Items
    q_y = sync_y + 155
    draw.rounded_rectangle([20, q_y, W - 20, q_y + 310], radius=16, fill=CARD_BG, outline=CARD_BORDER, width=1)
    draw.text((36, q_y + 18), "PENDING CLINICAL DATA PACKETS", font=get_font(11, bold=True), fill=TEXT_MUTED)

    items = [
        ("PAT-KGP-005 · Tapan Roy (62M)", "3 Photos + Wagner 2 Suspected · Debra Sub-center", "Ready to Push (12.4 MB)", AMBER),
        ("PAT-KGP-006 · Gita Mallick (55F)", "3 Photos + Neuropathy Screening · Debra Sub-center", "Ready to Push (14.1 MB)", AMBER),
        ("PAT-KGP-007 · Biren Mahato (70M)", "3 Photos + Ulcer Measurement · Keshpur Outpost", "Ready to Push (11.8 MB)", AMBER),
    ]
    iy = q_y + 46
    for title, sub, stat, col in items:
        draw.rounded_rectangle([32, iy, W - 32, iy + 74], radius=10, fill=CARD_SUB, outline=CARD_BORDER, width=1)
        draw.text((44, iy + 14), title, font=get_font(11.5, bold=True), fill=TEXT_WHITE)
        draw.text((44, iy + 34), sub, font=get_font(10), fill=TEXT_MUTED)
        draw.text((44, iy + 52), stat, font=get_font(9.5, bold=True), fill=col)
        iy += 84

    # One-Touch Sync Button
    btn_y = q_y + 325
    draw.rounded_rectangle([20, btn_y, W - 20, btn_y + 58], radius=12, fill=EMERALD)
    draw.text((W//2, btn_y + 29), "Sync All Sessions with Apex Master (FastAPI) ->", font=get_font(13, bold=True), fill=TEXT_WHITE, anchor="mm")

    draw.text((W//2, btn_y + 78), "Automatic retry on link drop · Zero packet duplication", font=get_font(10), fill=TEXT_DIM, anchor="mm")

    return wrap_in_phone_mockup(img)

# ── Main Orchestration ───────────────────────────────────────────────────────
def generate_all_mockups():
    print("Generating photorealistic phone and tablet mockups...")

    # 1. Real Phone Screenshot: Doctor Command Hub
    p_hub = os.path.join("real_screenshots", "media_1790880676182.png")
    if os.path.exists(p_hub):
        im = Image.open(p_hub)
        res = wrap_in_phone_mockup(im)
        res.save(os.path.join(OUT_DIR, "mockup_doctor_command_hub.png"))
        print("Generated: mockup_doctor_command_hub.png (from real screenshot)")

    # 2. Real Phone Screenshot: Patient Wound Detail
    p_wound = os.path.join("real_screenshots", "media_1790876415329.png")
    if os.path.exists(p_wound):
        im = Image.open(p_wound)
        res = wrap_in_phone_mockup(im)
        res.save(os.path.join(OUT_DIR, "mockup_patient_wound_detail.png"))
        print("Generated: mockup_patient_wound_detail.png (from real screenshot)")

    # 3. Real Phone Screenshot: Camera Telemetry HUD
    p_cam = os.path.join("real_screenshots", "media_1790876425291.png")
    if os.path.exists(p_cam):
        im = Image.open(p_cam)
        res = wrap_in_phone_mockup(im)
        res.save(os.path.join(OUT_DIR, "mockup_camera_telemetry_hud.png"))
        print("Generated: mockup_camera_telemetry_hud.png (from real screenshot)")

    # 4. Real Tablet / Desktop Screenshot: Tablet Hub
    p_tab = os.path.join("real_screenshots", "media_1790882283619.png")
    if os.path.exists(p_tab):
        im = Image.open(p_tab)
        res = wrap_in_tablet_mockup(im)
        res.save(os.path.join(OUT_DIR, "mockup_tablet_command_hub.png"))
        print("Generated: mockup_tablet_command_hub.png (from real tablet screenshot)")

    # 5. Real Clinical Photo: Annotated Segmentation
    p_ann = os.path.join("stored_photos", "PAT_KGP_01_VIS_004_measurement_annotated_20261001_200842.jpg")
    if os.path.exists(p_ann):
        # Create a professional medical panel around it
        ann_im = Image.open(p_ann).convert("RGBA")
        ann_w, ann_h = ann_im.size
        # target panel size
        panel_w = 700
        panel_h = int(ann_h * (panel_w / ann_w)) + 90
        panel = Image.new("RGBA", (panel_w, panel_h), CARD_BG)
        p_draw = ImageDraw.Draw(panel)
        # title
        p_draw.text((20, 16), "AI CLINICAL SEGMENTATION & MM CALIBRATION [ACTIVE]", font=get_font(12, bold=True), fill=EMERALD)
        p_draw.text((20, 36), "Model: Mask R-CNN ResNet-50 · Calibration Target: Indian 1-Rupee Coin (24.0mm)", font=get_font(10), fill=TEXT_MUTED)
        p_draw.text((panel_w - 20, 26), "Area: 3.84 cm² (99.1% IoU)", font=get_font(12, bold=True), fill=TEXT_WHITE, anchor="rm")
        # paste image
        ann_resized = ann_im.resize((panel_w, panel_h - 60), Image.Resampling.LANCZOS)
        panel.paste(ann_resized, (0, 60))
        panel.save(os.path.join(OUT_DIR, "mockup_clinical_ai_segmentation.png"))
        print("Generated: mockup_clinical_ai_segmentation.png (from real clinical photo)")

    # 6. Real Clinical Photo: Lighting Quality Telemetry
    p_qual = os.path.join("real_screenshots", "media_1790872914085.png")
    if os.path.exists(p_qual):
        q_im = Image.open(p_qual).convert("RGBA")
        q_w, q_h = q_im.size
        panel_w = 640
        panel_h = int(q_h * (panel_w / q_w)) + 70
        panel = Image.new("RGBA", (panel_w, panel_h), CARD_BG)
        p_draw = ImageDraw.Draw(panel)
        p_draw.text((20, 16), "REAL-TIME PHOTOMETRIC QUALITY & BLUR TELEMETRY", font=get_font(12, bold=True), fill=BLUE_LIGHT)
        p_draw.text((20, 36), "ISO 400 · Shutter 1/120s · Laplacian Variance: 284 (PASSED)", font=get_font(10), fill=TEXT_MUTED)
        q_resized = q_im.resize((panel_w, panel_h - 55), Image.Resampling.LANCZOS)
        panel.paste(q_resized, (0, 55))
        panel.save(os.path.join(OUT_DIR, "mockup_photo_telemetry_quality.png"))
        print("Generated: mockup_photo_telemetry_quality.png")

    # 7. Rendered Screens in Phone Chassis
    screen_login = build_screen_login()
    screen_login.save(os.path.join(OUT_DIR, "mockup_portal_login.png"))
    print("Generated: mockup_portal_login.png")

    screen_3photo = build_screen_3photo_lock()
    screen_3photo.save(os.path.join(OUT_DIR, "mockup_3photo_checklist.png"))
    print("Generated: mockup_3photo_checklist.png (Bug Fix #1)")

    screen_diag = build_screen_doctor_diagnosis()
    screen_diag.save(os.path.join(OUT_DIR, "mockup_doctor_manual_diagnosis.png"))
    print("Generated: mockup_doctor_manual_diagnosis.png (Bug Fix #2)")

    screen_refl = build_screen_doctor_reflection()
    screen_refl.save(os.path.join(OUT_DIR, "mockup_doctor_reflection.png"))
    print("Generated: mockup_doctor_reflection.png (Bug Fix #3)")

    screen_heal = build_screen_healing_journey()
    screen_heal.save(os.path.join(OUT_DIR, "mockup_healing_journey.png"))
    print("Generated: mockup_healing_journey.png (Option 1)")

    screen_tele = build_screen_teleconsult()
    screen_tele.save(os.path.join(OUT_DIR, "mockup_teleconsult_room.png"))
    print("Generated: mockup_teleconsult_room.png (Option 2)")

    screen_mono = build_screen_monofilament_trajectory()
    screen_mono.save(os.path.join(OUT_DIR, "mockup_monofilament_trajectory.png"))
    print("Generated: mockup_monofilament_trajectory.png (Option 4)")

    screen_asha = build_screen_asha_offline_queue()
    screen_asha.save(os.path.join(OUT_DIR, "mockup_asha_offline_queue.png"))
    print("Generated: mockup_asha_offline_queue.png (ASHA Queue)")

    print("All photorealistic mockups successfully generated in manual_assets/!")

if __name__ == "__main__":
    generate_all_mockups()
