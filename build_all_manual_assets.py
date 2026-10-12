# build_all_manual_assets.py
# Generates every image asset needed for the DiabetesCare AI Official User Manual
# Uses real app screenshots where available, draws accurate UI otherwise

import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT_DIR = "manual_assets"
os.makedirs(OUT_DIR, exist_ok=True)

FONT_REG  = "C:/Windows/Fonts/segoeui.ttf"
FONT_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_MONO = "C:/Windows/Fonts/consola.ttf"

def gf(size, bold=False, mono=False):
    try:
        return ImageFont.truetype(FONT_MONO if mono else (FONT_BOLD if bold else FONT_REG), int(size))
    except:
        return ImageFont.load_default()

# ─── Color Palette (DiabetesCare AI design system) ───────────────────────────
NAVY       = (11,  19,  43,  255)
CARD_BG    = (17,  28,  56,  255)
CARD_SUB   = (12,  21,  46,  255)
CARD_BDR   = (35,  53,  94,  255)
BLUE       = (37,  99,  235, 255)
BLUE_L     = (59,  130, 246, 255)
EMERALD    = (16,  185, 129, 255)
EM_BG      = (6,   78,  59,  255)
AMBER      = (245, 158, 11,  255)
AM_BG      = (120, 53,  15,  255)
RED        = (239, 68,  68,  255)
RED_BG     = (127, 29,  29,  255)
PURPLE     = (147, 51,  234, 255)
WHITE      = (255, 255, 255, 255)
MUTED      = (148, 163, 184, 255)
DIM        = (100, 116, 139, 255)
SLATE      = (71,  85,  105, 255)

W, H = 460, 960   # Phone screen canvas

def phone_frame(screen_img, sw=460, sh=960):
    """Wrap any PIL image in a realistic phone frame"""
    scr = screen_img.convert("RGBA").resize((sw, sh), Image.Resampling.LANCZOS)
    blr = 22; btb = 28
    fw = sw + blr*2;  fh = sh + btb*2
    sm = 36
    cw = fw + sm*2;   ch = fh + sm*2

    canvas = Image.new("RGBA", (cw, ch), (0,0,0,0))

    # Drop shadow
    shadow = Image.new("RGBA", (cw, ch), (0,0,0,0))
    sd = ImageDraw.Draw(shadow)
    pr = [sm, sm, sm+fw, sm+fh]
    sd.rounded_rectangle(pr, radius=52, fill=(15,23,42,120))
    shadow = shadow.filter(ImageFilter.GaussianBlur(20))
    canvas.paste(shadow, (0,8), shadow)

    draw = ImageDraw.Draw(canvas)
    pr = [sm, sm, sm+fw, sm+fh]

    # Side buttons
    draw.rounded_rectangle([pr[0]-4, pr[1]+155, pr[0], pr[1]+210], radius=3, fill=SLATE)
    draw.rounded_rectangle([pr[0]-4, pr[1]+225, pr[0], pr[1]+275], radius=3, fill=SLATE)
    draw.rounded_rectangle([pr[2],   pr[1]+175, pr[2]+4, pr[1]+245], radius=3, fill=SLATE)

    # Phone body
    draw.rounded_rectangle(pr, radius=52, fill=(30,41,59,255), outline=(71,85,105,255), width=2)
    ib = [pr[0]+2, pr[1]+2, pr[2]-2, pr[3]-2]
    draw.rounded_rectangle(ib, radius=50, fill=(15,23,42,255))

    # Screen
    sx = sm + blr;  sy = sm + btb
    mask = Image.new("L", (sw, sh), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, sw, sh], radius=34, fill=255)
    canvas.paste(scr, (sx, sy), mask)

    # Status bar
    ovd = ImageDraw.Draw(canvas)
    ovd.text((sx+30, sy+10), "09:41", font=gf(12, bold=True), fill=WHITE)
    ovd.text((sx+sw-82, sy+10), "5G  98%", font=gf(11, bold=True), fill=WHITE)

    # Speaker slit
    draw.rounded_rectangle([sx+sw//2-28, sy-12, sx+sw//2+28, sy-8], radius=2, fill=(51,65,85,255))

    # Dynamic island
    pw=96; ph=24
    px=sx+(sw-pw)//2; py=sy+10
    draw.rounded_rectangle([px,py,px+pw,py+ph], radius=12, fill=(0,0,0,255))
    lx=px+pw-22; ly=py+4
    draw.ellipse([lx,ly,lx+16,ly+16], fill=(15,23,42,255), outline=(30,41,59,255), width=1)
    draw.ellipse([lx+5,ly+5,lx+11,ly+11], fill=BLUE)

    # Home bar
    bw=130; bh=4
    bx=sx+(sw-bw)//2; by=sy+sh-14
    draw.rounded_rectangle([bx,by,bx+bw,by+bh], radius=2, fill=(203,213,225,210))

    return canvas

def tablet_frame(screen_img, sw=900, sh=620):
    """Wrap image in a tablet/desktop frame"""
    scr = screen_img.convert("RGBA").resize((sw, sh), Image.Resampling.LANCZOS)
    bezel = 22; sm = 32
    fw = sw+bezel*2; fh = sh+bezel*2
    cw = fw+sm*2;   ch = fh+sm*2

    canvas = Image.new("RGBA", (cw, ch), (0,0,0,0))
    shadow = Image.new("RGBA", (cw, ch), (0,0,0,0))
    sd = ImageDraw.Draw(shadow)
    tr = [sm, sm, sm+fw, sm+fh]
    sd.rounded_rectangle(tr, radius=30, fill=(15,23,42,125))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    canvas.paste(shadow, (0, 10), shadow)

    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle(tr, radius=30, fill=(30,41,59,255), outline=(71,85,105,255), width=2)
    ib = [tr[0]+2, tr[1]+2, tr[2]-2, tr[3]-2]
    draw.rounded_rectangle(ib, radius=28, fill=(15,23,42,255))

    sx = sm+bezel; sy = sm+bezel
    mask = Image.new("L", (sw, sh), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0,0,sw,sh], radius=18, fill=255)
    canvas.paste(scr, (sx, sy), mask)

    # Camera dot
    cx = sm+fw//2; cy = sm+bezel//2
    draw.ellipse([cx-5, cy-5, cx+5, cy+5], fill=(0,0,0,255), outline=(51,65,85,255), width=1)

    return canvas

def new_screen():
    img = Image.new("RGBA", (W, H), NAVY)
    draw = ImageDraw.Draw(img)
    return img, draw

def draw_card(draw, x, y, w, h, r=12, fill=CARD_BG, border=CARD_BDR, bw=1):
    draw.rounded_rectangle([x,y,x+w,y+h], radius=r, fill=fill, outline=border, width=bw)

def draw_pill(draw, x, y, w, h, fill=BLUE, text='', font_size=11, text_fill=WHITE, r=8):
    draw.rounded_rectangle([x,y,x+w,y+h], radius=r, fill=fill)
    if text:
        draw.text((x+w//2, y+h//2), text, font=gf(font_size, bold=True), fill=text_fill, anchor='mm')

def hline(draw, y, color=CARD_BDR, w=2):
    draw.line([(0, y), (W, y)], fill=color, width=w)

# ─────────────────────────────────────────────────────────────────────────────
# SCREEN 1: Portal Login & RBAC
# ─────────────────────────────────────────────────────────────────────────────
def build_login():
    img, draw = new_screen()

    # Brand area
    cx = W//2
    draw.ellipse([cx-36, 60, cx+36, 132], fill=(30,58,138,255), outline=BLUE, width=2)
    draw.text((cx, 96), "+", font=gf(40, bold=True), fill=WHITE, anchor="mm")
    draw.text((cx, 150), "DiabetesCare AI", font=gf(22, bold=True), fill=WHITE, anchor="mm")
    draw.text((cx, 175), "Clinical Triage & Wound Monitoring", font=gf(12), fill=MUTED, anchor="mm")
    draw.text((cx, 195), "IIT Kharagpur · Paschim Medinipur Apex Hub", font=gf(10, bold=True), fill=EMERALD, anchor="mm")

    # Persona selector
    draw_card(draw, 18, 215, W-36, 300, r=16)
    draw.text((32, 230), "SELECT CLINICAL ACCESS PERSONA", font=gf(10, bold=True), fill=MUTED)

    roles = [
        ("[DR] Lead Diabetologist", "Full Clinical Triage & Validation Access", RED, True),
        ("[PT] Enrolled Patient", "Self-Monitoring & Healing Journey Portal", EMERALD, False),
        ("[HW] ASHA Health Worker", "Field Screening & Offline Queue Sync", BLUE, False),
        ("[AD] Hospital Administrator", "Audit Logs & Institution Registry", AMBER, False),
    ]
    ry = 254
    for title, sub, col, active in roles:
        bg = col if active else CARD_SUB
        bdr = col
        draw.rounded_rectangle([28, ry, W-28, ry+52], radius=10, fill=bg, outline=bdr, width=1)
        draw.text((42, ry+14), title, font=gf(12, bold=True), fill=WHITE)
        draw.text((42, ry+32), sub, font=gf(9), fill=(WHITE if active else MUTED))
        if active:
            draw_pill(draw, W-110, ry+16, 70, 22, fill=(15,23,42,200), text="ACTIVE", font_size=9)
        ry += 60

    # Credentials
    draw_card(draw, 18, 530, W-36, 175, r=16)
    draw.text((32, 546), "AUTHORIZED CREDENTIALS (RBAC)", font=gf(10, bold=True), fill=MUTED)
    draw.rounded_rectangle([28,568,W-28,616], radius=8, fill=CARD_SUB, outline=CARD_BDR, width=1)
    draw.text((42, 580), "doctor@demo.in  ·  Lead Diabetologist", font=gf(12), fill=WHITE)
    draw.text((42, 598), "Verified Identity · MMC&H Paschim Medinipur", font=gf(9), fill=DIM)

    draw.rounded_rectangle([28,622,W-28,670], radius=8, fill=CARD_SUB, outline=CARD_BDR, width=1)
    draw.text((42, 634), "•••••••••••••••••", font=gf(14), fill=WHITE)
    draw.text((42, 652), "AES-256 Keystore · TLS 1.3 End-to-End Encrypted", font=gf(9), fill=EMERALD)

    draw.text((32, 682), "Biometric (Fingerprint) · Hardware Keystore Enabled", font=gf(9), fill=DIM)
    draw.text((32, 698), "DPDP Act 2023 · CDSCO Class B SaMD Compliant", font=gf(9), fill=DIM)

    # Sign in button
    draw.rounded_rectangle([18, 720, W-18, 780], radius=14, fill=BLUE)
    draw.text((W//2, 750), "Sign In to Command Portal  →", font=gf(15, bold=True), fill=WHITE, anchor="mm")

    draw.text((cx, 800), "http://192.168.31.94:8000  (FastAPI Master)", font=gf(9, mono=True), fill=DIM, anchor="mm")
    draw.text((cx, 820), "3 consecutive failures triggers 15-min lockout", font=gf(9), fill=RED, anchor="mm")

    return phone_frame(img)

# ─────────────────────────────────────────────────────────────────────────────
# SCREEN 2: Patient Registration & Consent
# ─────────────────────────────────────────────────────────────────────────────
def build_registration():
    img, draw = new_screen()

    draw.text((20, 60), "PATIENT ONBOARDING", font=gf(10, bold=True), fill=BLUE_L)
    draw.text((20, 78), "New Clinical Enrollment", font=gf(20, bold=True), fill=WHITE)
    draw.text((20, 105), "ASHA Worker: Priya Das  ·  Debra Rural Block", font=gf(10), fill=MUTED)

    fields = [
        ("Full Legal Name", "Subhash Mondal", WHITE),
        ("ABHA Number", "91-4521-8890-1234  (Verified ✓)", EMERALD),
        ("Age & Gender", "58 Years  ·  Male  (5-yr band: 55–60)", MUTED),
        ("Diabetes Duration", "12 Years  (Since 2014)", MUTED),
        ("HbA1c (Last Reading)", "9.2%  (March 2026)", AMBER),
        ("Neuropathy History", "YES  ·  10g Monofilament Deficit (6/10)", RED),
        ("Primary District Block", "Midnapore Sadar  ·  Outpost #04", MUTED),
    ]

    fy = 135
    draw_card(draw, 18, fy, W-36, len(fields)*62 + 20, r=14)
    draw.text((32, fy+14), "CLINICAL DOSSIER FIELDS", font=gf(10, bold=True), fill=MUTED)
    iy = fy+38
    for label, val, col in fields:
        draw.rounded_rectangle([28, iy, W-28, iy+48], radius=8, fill=CARD_SUB, outline=CARD_BDR, width=1)
        draw.text((38, iy+8), label, font=gf(9), fill=DIM)
        draw.text((38, iy+26), val, font=gf(11, bold=True), fill=col)
        iy += 58

    # Consent banner
    cy2 = iy + 12
    draw.rounded_rectangle([18, cy2, W-18, cy2+155], radius=14, fill=EM_BG, outline=EMERALD, width=1)
    draw.text((32, cy2+14), "DPDP ACT 2023 — STATUTORY CONSENT", font=gf(10, bold=True), fill=EMERALD)
    consent_txt = ("Explicit informed consent obtained in English\n"
                   "and Bengali (বাংলা). Patient acknowledges:\n"
                   "• Photographs used only for wound measurement\n"
                   "• Right to erasure within 72 hours on request\n"
                   "• No data shared without prior written approval\n"
                   "• HMAC pseudonymization enforced (k≥5 guard)")
    draw.text((32, cy2+36), consent_txt, font=gf(10), fill=WHITE, spacing=3)

    draw.rounded_rectangle([18, cy2+170, W-18, cy2+226], radius=14, fill=EMERALD)
    draw.text((W//2, cy2+198), "Confirm & Register Patient  →", font=gf(14, bold=True), fill=WHITE, anchor="mm")

    return phone_frame(img)

# ─────────────────────────────────────────────────────────────────────────────
# SCREEN 3: 3-Photo Checklist Lock [Bug Fix #1]
# ─────────────────────────────────────────────────────────────────────────────
def build_3photo_lock():
    img, draw = new_screen()

    draw.text((20, 60), "CLINICAL PHOTO PROTOCOL", font=gf(10, bold=True), fill=RED)
    draw.text((20, 78), "3-Photo Verification Lock", font=gf(20, bold=True), fill=WHITE)
    draw.text((20, 104), "Patient: Subhash Mondal  ·  Visit #4  ·  Session SES-004", font=gf(9), fill=MUTED)

    # Warning banner
    draw.rounded_rectangle([18, 126, W-18, 248], radius=12, fill=(69,10,10,255), outline=RED, width=2)
    draw.text((32, 140), "MANDATORY 3-PHOTO LOCK  [ACTIVE]", font=gf(11, bold=True), fill=RED)
    warn = ("CDSCO Clinical Protocol enforced. Single-photo\n"
            "submissions are permanently blocked.\n"
            "Three distinct angular views required:\n"
            "90° plantar · 45° oblique · macro close-up\n"
            "All three must pass quality validation gates.")
    draw.text((32, 162), warn, font=gf(10), fill=(254,202,202,255), spacing=3)

    # 3 Photo cards
    photos = [
        ("PHOTO 1 / 3 — PLANTAR OVERVIEW",   "90° Orthogonal  ·  30 cm distance",           "✓ CAPTURED & VALIDATED",  EMERALD, EM_BG,  True),
        ("PHOTO 2 / 3 — OBLIQUE LATERAL",    "45° angle  ·  Depth & edge profiling",         "✓ CAPTURED & VALIDATED",  EMERALD, EM_BG,  True),
        ("PHOTO 3 / 3 — CALIBRATED MACRO",   "24 mm Indian 1-Rupee coin calibrant required", "⏳ PENDING — TAP TO CAPTURE", AMBER, AM_BG, False),
    ]
    py = 256
    for title, sub, status, col, bg, done in photos:
        draw.rounded_rectangle([18, py, W-18, py+105], radius=12, fill=CARD_BG, outline=col, width=2)
        draw.rounded_rectangle([18, py, 28, py+105], radius=4, fill=col)
        draw.text((38, py+12), title, font=gf(11, bold=True), fill=WHITE)
        draw.text((38, py+30), sub, font=gf(9), fill=MUTED)
        draw.rounded_rectangle([38, py+48, W-34, py+90], radius=8, fill=bg, outline=col, width=1)
        draw.text((48, py+69), status, font=gf(11, bold=True), fill=col, anchor="lm")
        py += 116

    # Bottom lock status
    by = py + 8
    draw.rounded_rectangle([18, by, W-18, by+70], radius=12, fill=CARD_BG, outline=CARD_BDR, width=1)
    draw.text((W//2, by+20), "SUBMISSION LOCKED  (2 of 3 complete)", font=gf(11, bold=True), fill=AMBER, anchor="mm")
    draw.text((W//2, by+42), "Capture Photo 3 to unlock AI Review →", font=gf(10), fill=MUTED, anchor="mm")
    draw.text((W//2, by+60), "Bug Fix #1: No single-photo bypass allowed", font=gf(9), fill=DIM, anchor="mm")

    draw.rounded_rectangle([18, by+82, W-18, by+132], radius=12, fill=(51,65,85,255))
    draw.text((W//2, by+107), "🔒  Proceed to Review  (3/3 Required)", font=gf(13, bold=True), fill=MUTED, anchor="mm")

    return phone_frame(img)

# ─────────────────────────────────────────────────────────────────────────────
# SCREEN 4: Camera Viewfinder & CV HUD
# ─────────────────────────────────────────────────────────────────────────────
def build_camera_hud():
    img, draw = new_screen()

    draw.text((20, 60), "LIVE CAMERA CAPTURE", font=gf(10, bold=True), fill=EMERALD)
    draw.text((20, 78), "Viewfinder & CV HUD", font=gf(20, bold=True), fill=WHITE)

    # Viewfinder area
    vf_y = 110; vf_h = 340
    draw.rounded_rectangle([16, vf_y, W-16, vf_y+vf_h], radius=14, fill=(0,0,0,255), outline=EMERALD, width=2)

    # Corner brackets
    blen = 30; bt = 3
    def bracket(x, y, right, bottom):
        if not right: draw.line([(x, y), (x+blen, y)], fill=EMERALD, width=bt)
        else:         draw.line([(x-blen, y), (x, y)], fill=EMERALD, width=bt)
        if not bottom: draw.line([(x, y), (x, y+blen)], fill=EMERALD, width=bt)
        else:          draw.line([(x, y-blen), (x, y)], fill=EMERALD, width=bt)
    bracket(24, vf_y+10, False, False)
    bracket(W-24, vf_y+10, True, False)
    bracket(24, vf_y+vf_h-10, False, True)
    bracket(W-24, vf_y+vf_h-10, True, True)

    # Crosshairs
    cx2 = W//2; cy2 = vf_y + vf_h//2
    draw.line([(cx2-40, cy2), (cx2+40, cy2)], fill=(255,255,255,180), width=1)
    draw.line([(cx2, cy2-40), (cx2, cy2+40)], fill=(255,255,255,180), width=1)
    draw.ellipse([cx2-4, cy2-4, cx2+4, cy2+4], fill=EMERALD)

    # Coin detection box
    coin_x = cx2+50; coin_y = vf_y+80
    draw.rectangle([coin_x-28, coin_y-28, coin_x+28, coin_y+28], outline=EMERALD, width=2)
    draw.text((coin_x, coin_y-38), "COIN  0.91", font=gf(10, bold=True), fill=EMERALD, anchor="mm")

    # Status pills in viewfinder
    pills = [("BLUR  PASS ✓", EMERALD, 40), ("LUMEN 480  ✓", EMERALD, 130), ("TILT  0.8°  ✓", EMERALD, 220)]
    for txt, col, px in pills:
        draw.rounded_rectangle([px, vf_y+vf_h-42, px+90, vf_y+vf_h-14], radius=8, fill=(0,0,0,180))
        draw.text((px+45, vf_y+vf_h-28), txt, font=gf(9, bold=True), fill=col, anchor="mm")

    # Telemetry cards
    tele_y = vf_y + vf_h + 14
    metrics = [
        ("Laplacian Var.", "≥200", "312", EMERALD),
        ("Illuminance", "300-1200 lux", "480 lux", EMERALD),
        ("Gyro Tilt", "≤5.0°", "0.8°", EMERALD),
    ]
    card_w = (W-36-16) // 3
    for i, (lbl, thresh, val, col) in enumerate(metrics):
        bx = 18 + i*(card_w+8)
        draw_card(draw, bx, tele_y, card_w, 85, r=10)
        draw.text((bx+card_w//2, tele_y+14), lbl, font=gf(9), fill=MUTED, anchor="mm")
        draw.text((bx+card_w//2, tele_y+40), val, font=gf(15, bold=True), fill=col, anchor="mm")
        draw.text((bx+card_w//2, tele_y+60), f"Thresh: {thresh}", font=gf(8), fill=DIM, anchor="mm")

    # Coin info
    coin_y2 = tele_y + 100
    draw_card(draw, 18, coin_y2, W-36, 75, r=10)
    draw.text((32, coin_y2+14), "🪙  CALIBRANT COIN DETECTED", font=gf(11, bold=True), fill=EMERALD)
    draw.text((32, coin_y2+34), "Indian 1-Rupee  ·  24.0 mm diameter", font=gf(10), fill=WHITE)
    draw.text((32, coin_y2+52), "Scale: 18.6 px/mm  ·  Confidence: 91.4%", font=gf(9), fill=MUTED)

    # Capture button
    btn_y = coin_y2 + 90
    draw.ellipse([W//2-50, btn_y, W//2+50, btn_y+100], fill=EMERALD)
    draw.text((W//2, btn_y+50), "⊙", font=gf(36, bold=True), fill=WHITE, anchor="mm")
    draw.text((W//2, btn_y+115), "Touch to Focus & Capture", font=gf(10), fill=MUTED, anchor="mm")

    return phone_frame(img)

# ─────────────────────────────────────────────────────────────────────────────
# SCREEN 5: AI Analysis & Review (using REAL screenshot from app)
# ─────────────────────────────────────────────────────────────────────────────
def build_ai_review_real():
    """Use actual real app screenshot for AI Review screen"""
    real = Image.open("real_screenshots/media_1790880676182.png").convert("RGBA")
    return phone_frame(real, sw=real.width, sh=real.height)

# ─────────────────────────────────────────────────────────────────────────────
# SCREEN 6: Doctor Manual Diagnosis & Concordance [Bug Fix #2]
# ─────────────────────────────────────────────────────────────────────────────
def build_doctor_diagnosis():
    img, draw = new_screen()

    draw.text((20, 60), "CLINICAL REVIEW & VALIDATION", font=gf(10, bold=True), fill=EMERALD)
    draw.text((20, 78), "AI Results & Manual Diagnosis", font=gf(18, bold=True), fill=WHITE)
    draw.text((20, 104), "Dr. Aris Banerjee, MD  ·  Session SES-004", font=gf(9), fill=MUTED)

    # AI Results Card
    draw_card(draw, 18, 122, W-36, 145, r=14, border=BLUE_L, bw=2)
    draw.text((32, 136), "🤖  AI DEEP LEARNING INFERENCE", font=gf(10, bold=True), fill=BLUE_L)
    m_w = (W-36-24)//3
    metrics = [("Wagner", "Grade 2", EMERALD), ("Cellulitis", "Neg (0.12)", BLUE_L), ("Area", "3.84 cm²", AMBER)]
    for i, (lab, val, col) in enumerate(metrics):
        bx = 28 + i*(m_w+8)
        draw.rounded_rectangle([bx, 158, bx+m_w, 248], radius=8, fill=CARD_SUB, outline=CARD_BDR, width=1)
        draw.text((bx+m_w//2, 176), lab, font=gf(9), fill=MUTED, anchor="mm")
        draw.text((bx+m_w//2, 210), val, font=gf(11, bold=True), fill=col, anchor="mm")

    # Doctor manual diagnosis — BUG FIX #2 key feature
    diag_y = 276
    draw.rounded_rectangle([18, diag_y, W-18, diag_y+265], radius=14, fill=CARD_BG, outline=RED, width=2)
    draw.text((32, diag_y+14), "👨‍⚕️  PHYSICIAN CLINICAL IMPRESSION  [MANDATORY]", font=gf(10, bold=True), fill=RED)
    draw.text((32, diag_y+34), "Bug Fix #2: Manual entry required before submission", font=gf(9), fill=DIM)

    inp_y = diag_y + 54
    draw.rounded_rectangle([28, inp_y, W-28, inp_y+125], radius=10, fill=CARD_SUB, outline=BLUE_L, width=2)
    note = ("Neuropathic plantar ulcer, 1st metatarsal\n"
            "head. Wagner Grade 2 confirmed. Healthy\n"
            "granulation ~65%, mild peripheral erythema.\n"
            "No deep fascial involvement detected.\n"
            "Recommend hydrocolloid dressing renewal.")
    draw.text((40, inp_y+14), note, font=gf(10), fill=WHITE, spacing=4)
    draw.text((W-36, inp_y+120), "Dictate |", font=gf(9), fill=DIM, anchor="rm")

    # Concordance badge
    badge_y = inp_y + 138
    draw.rounded_rectangle([28, badge_y, W-28, badge_y+56], radius=10, fill=EM_BG, outline=EMERALD, width=2)
    draw.text((44, badge_y+28), "★  98.4% CONCORDANCE  [EXCELLENT MATCH]", font=gf(11, bold=True), fill=EMERALD, anchor="lm")
    draw.text((W-36, badge_y+28), "AI ≡ MD", font=gf(10, bold=True), fill=WHITE, anchor="rm")

    # Sync notice
    sync_y = badge_y + 70
    draw.rounded_rectangle([18, sync_y, W-18, sync_y+72], radius=12, fill=CARD_BG, outline=CARD_BDR, width=1)
    draw.text((32, sync_y+14), "⚡  INSTANT DOCTOR HUB REFLECTION  [Bug Fix #3]", font=gf(10, bold=True), fill=EMERALD)
    draw.text((32, sync_y+36), "Synchronous commit + SSE broadcast (< 450ms)", font=gf(9), fill=MUTED)
    draw.text((32, sync_y+54), "Doctor dashboard updates in real-time — no refresh needed", font=gf(9), fill=DIM)

    # Submit button
    btn_y = sync_y + 86
    draw.rounded_rectangle([18, btn_y, W-18, btn_y+58], radius=14, fill=EMERALD)
    draw.text((W//2, btn_y+29), "Submit Diagnosis & Sync to Doctor Hub  →", font=gf(13, bold=True), fill=WHITE, anchor="mm")

    return phone_frame(img)

# ─────────────────────────────────────────────────────────────────────────────
# SCREEN 7: Doctor Command Hub — Live Reflection [Bug Fix #3]
# ─────────────────────────────────────────────────────────────────────────────
def build_doctor_hub():
    img, draw = new_screen()

    draw.text((20, 60), "DOCTOR COMMAND HUB", font=gf(10, bold=True), fill=RED)
    draw.text((20, 78), "Live Triage Roster", font=gf(20, bold=True), fill=WHITE)
    draw.text((20, 104), "MMCH Apex Center  ·  Dr. Aris Banerjee, MD", font=gf(9), fill=MUTED)

    # Live sync banner — Bug Fix #3
    draw.rounded_rectangle([18, 122, W-18, 172], radius=10, fill=EM_BG, outline=EMERALD, width=2)
    draw.text((32, 147), "● REAL-TIME SYNCHRONIZED — Bug Fix #3 ACTIVE", font=gf(11, bold=True), fill=EMERALD, anchor="lm")
    draw.text((W-32, 147), "0s ago", font=gf(11, bold=True), fill=WHITE, anchor="rm")

    # KPI row
    kpis = [("4 Active", "COHORT", WHITE), ("2 Critical", "ALERTS", RED), ("1 Pending", "TELECONSULT", BLUE_L), ("74.2%", "HEAL RATE", EMERALD)]
    kw = (W-36-24)//4
    kx = 18
    for i, (val, lab, col) in enumerate(kpis):
        bx = kx + i*(kw+8)
        draw_card(draw, bx, 180, kw, 65, r=8)
        draw.text((bx+kw//2, 198), val, font=gf(12, bold=True), fill=col, anchor="mm")
        draw.text((bx+kw//2, 216), lab, font=gf(8), fill=MUTED, anchor="mm")

    # Patient cards
    patients = [
        ("PAT-KGP-004", "Subhash Mondal  ·  58M", "JUST SUBMITTED · REFLECTED", EMERALD, EM_BG, 2, True,
         "Wagner Grade 2  ·  98.4% Concordance  ·  3-Photo Complete"),
        ("PAT-KGP-002", "Rameshwar Sen  ·  64M", "URGENT TRIAGE", RED, RED_BG, 4, False,
         "Wagner Grade 4  ·  GANGRENE SUSPECTED  ·  Immediate Surgical Ref"),
        ("PAT-KGP-001", "Anjali Devi  ·  52F", "ROUTINE FOLLOW-UP", BLUE_L, BLUE, 1, False,
         "Wagner Grade 1  ·  Healing +24%  ·  Teleconsult Completed"),
    ]

    cy = 258
    for pid, name, badge_txt, col, badge_bg, grade, highlight, detail in patients:
        draw.rounded_rectangle([18, cy, W-18, cy+140], radius=14, fill=CARD_BG, outline=col if highlight else CARD_BDR, width=2 if highlight else 1)
        draw_pill(draw, 28, cy+12, 190, 28, fill=badge_bg, text=badge_txt, font_size=9, text_fill=col)
        draw.text((W-28, cy+26), pid, font=gf(11, bold=True), fill=WHITE, anchor="rm")
        draw.text((28, cy+46), name, font=gf(14, bold=True), fill=WHITE)
        draw.rounded_rectangle([28, cy+70, W-28, cy+126], radius=8, fill=CARD_SUB, outline=CARD_BDR, width=1)
        draw.text((38, cy+83), detail, font=gf(9), fill=col if highlight else MUTED)
        draw.text((38, cy+100), f"Grade {grade}  ·  Foot Wound  ·  DiabetesCare AI", font=gf(9), fill=DIM)
        draw.text((W-36, cy+108), "Open →", font=gf(9, bold=True), fill=BLUE_L, anchor="rm")
        cy += 152

    return phone_frame(img)

# ─────────────────────────────────────────────────────────────────────────────
# SCREEN 8: My Healing Journey (Option 1)
# ─────────────────────────────────────────────────────────────────────────────
def build_healing_journey():
    img, draw = new_screen()

    draw.text((20, 60), "PATIENT CARE PORTAL", font=gf(10, bold=True), fill=EMERALD)
    draw.text((20, 78), "My Healing Journey", font=gf(20, bold=True), fill=WHITE)
    draw.text((20, 104), "Namaste, Subhash Mondal  ·  PAT-KGP-004", font=gf(9), fill=MUTED)

    # Progress card
    draw_card(draw, 18, 122, W-36, 210, r=14)
    draw.text((32, 136), "HEALING TRAJECTORY  ·  14 DAYS", font=gf(10, bold=True), fill=MUTED)
    draw.text((32, 158), "+18.2% Closure Progress", font=gf(20, bold=True), fill=EMERALD)
    draw.text((32, 182), "Wound area: 4.7 cm² → 3.84 cm² (reduction)", font=gf(10), fill=MUTED)

    # Progress bar
    bar_x = 32; bar_y = 205; bar_w = W-64; bar_h = 20
    draw.rounded_rectangle([bar_x, bar_y, bar_x+bar_w, bar_y+bar_h], radius=10, fill=CARD_SUB)
    draw.rounded_rectangle([bar_x, bar_y, bar_x+int(bar_w*0.68), bar_y+bar_h], radius=10, fill=EMERALD)
    draw.text((bar_x+bar_w-8, bar_y+10), "68% Epithelialized", font=gf(9, bold=True), fill=EMERALD, anchor="rm")

    draw.text((32, 238), "Wagner Grade: 2  →  Target: Grade 0 (Week 8)", font=gf(10, bold=True), fill=WHITE)
    draw.text((32, 256), "Next clinical capture scheduled: Day 21  (Oct 22)", font=gf(9), fill=BLUE_L)
    draw.text((32, 272), "Diabetologist: Dr. Aris Banerjee, MD  ·  MMCH", font=gf(9), fill=DIM)

    # Care checklist
    tasks_y = 345
    draw_card(draw, 18, tasks_y, W-36, 295, r=14)
    draw.text((32, tasks_y+14), "TODAY'S DIABETIC FOOT PROTOCOL", font=gf(10, bold=True), fill=MUTED)
    tasks = [
        ("✓  Morning Inspection & Wash", "Tepid water — no maceration", EMERALD, True),
        ("✓  Hydrocolloid Dressing Renewal", "Sterile dressing applied correctly", EMERALD, True),
        ("○  Evening Offloading Footwear", "Wear custom therapeutic sandals indoors", AMBER, False),
        ("○  Fasting Blood Glucose Log", "Record reading before breakfast", BLUE_L, False),
    ]
    ty = tasks_y + 40
    for task, sub, col, done in tasks:
        draw.rounded_rectangle([28, ty, W-28, ty+50], radius=8, fill=CARD_SUB, outline=col if done else CARD_BDR, width=1)
        draw.text((38, ty+12), task, font=gf(11, bold=True), fill=WHITE if done else MUTED)
        draw.text((38, ty+30), sub, font=gf(9), fill=MUTED)
        ty += 58

    draw.rounded_rectangle([18, ty+8, W-18, ty+62], radius=14, fill=EMERALD)
    draw.text((W//2, ty+35), "Join Teleconsultation  →  Dr. Banerjee", font=gf(13, bold=True), fill=WHITE, anchor="mm")
    draw.rounded_rectangle([18, ty+72, W-18, ty+118], radius=14, fill=RED_BG, outline=RED, width=1)
    draw.text((W//2, ty+95), "🆘  ASHA Emergency Helpdesk", font=gf(13, bold=True), fill=RED, anchor="mm")

    return phone_frame(img)

# ─────────────────────────────────────────────────────────────────────────────
# SCREEN 9: National Teleconsultation (Option 2)
# ─────────────────────────────────────────────────────────────────────────────
def build_teleconsult():
    img, draw = new_screen()

    draw.text((20, 60), "NATIONAL TELECONSULTATION", font=gf(10, bold=True), fill=BLUE_L)
    draw.text((20, 78), "eSanjeevani 2.0 Live", font=gf(20, bold=True), fill=WHITE)
    draw.text((20, 104), "ABHA: 91-4521-8890-1234  ·  ABDM M4 Verified", font=gf(9), fill=MUTED)

    # Live call timer
    draw.rounded_rectangle([18, 120, 165, 148], radius=8, fill=EM_BG)
    draw.text((90, 134), "● LIVE  00:12:45", font=gf(11, bold=True), fill=EMERALD, anchor="mm")

    # Video area
    vf_y = 157; vf_h = 250
    draw.rounded_rectangle([16, vf_y, W-16, vf_y+vf_h], radius=14, fill=(10,15,30,255), outline=BLUE_L, width=2)
    draw.text((W//2, vf_y+80), "[DOCTOR LIVE VIDEO FEED]", font=gf(13, bold=True), fill=MUTED, anchor="mm")
    draw.text((W//2, vf_y+105), "Dr. Aris Banerjee, MD", font=gf(14, bold=True), fill=WHITE, anchor="mm")
    draw.text((W//2, vf_y+125), "Diabetology  ·  Midnapore Medical College", font=gf(10), fill=EMERALD, anchor="mm")
    draw.text((W//2, vf_y+148), "Adaptive Bitrate: 1.2 Mbps (HD Quality)", font=gf(9), fill=DIM, anchor="mm")

    # PiP
    pip_x = W-130; pip_y = vf_y+vf_h-90
    draw.rounded_rectangle([pip_x, pip_y, pip_x+105, pip_y+72], radius=8, fill=CARD_BG, outline=EMERALD, width=1)
    draw.text((pip_x+52, pip_y+36), "Self Video", font=gf(10, bold=True), fill=WHITE, anchor="mm")

    # IoT vitals
    vit_y = vf_y+vf_h+14
    draw_card(draw, 18, vit_y, W-36, 115, r=14)
    draw.text((32, vit_y+12), "📡  LIVE IoT VITALS TELEMETRY (BLE)", font=gf(10, bold=True), fill=MUTED)
    vitals = [("SpO2", "98%", EMERALD), ("Blood Glucose", "138 mg/dL", BLUE_L), ("Skin Temp", "98.4°F", AMBER)]
    vw = (W-36-24)//3
    for i, (lab, val, col) in enumerate(vitals):
        bx = 28 + i*(vw+8)
        draw.rounded_rectangle([bx, vit_y+38, bx+vw, vit_y+100], radius=8, fill=CARD_SUB, outline=CARD_BDR, width=1)
        draw.text((bx+vw//2, vit_y+54), lab, font=gf(8), fill=MUTED, anchor="mm")
        draw.text((bx+vw//2, vit_y+78), val, font=gf(12, bold=True), fill=col, anchor="mm")

    # Prescription
    rx_y = vit_y + 128
    draw_card(draw, 18, rx_y, W-36, 175, r=14)
    draw.text((32, rx_y+12), "Rx  DIGITAL PRESCRIPTION (ABDM Signed)", font=gf(10, bold=True), fill=MUTED)
    rx = ("1. Hydrocolloid Dressing  —  every 48 hours\n"
          "2. Tab. Metformin 500mg BD after meals\n"
          "3. Therapeutic offloading footwear mandatory\n"
          "4. Photo capture Day 21  (Oct 22, 2026)")
    draw.text((32, rx_y+36), rx, font=gf(10), fill=WHITE, spacing=5)

    draw.rounded_rectangle([18, rx_y+180, W-18, rx_y+232], radius=14, fill=BLUE)
    draw.text((W//2, rx_y+206), "Download Signed Prescription (ABDM QR)  →", font=gf(12, bold=True), fill=WHITE, anchor="mm")

    return phone_frame(img)

# ─────────────────────────────────────────────────────────────────────────────
# SCREEN 10: Wound Trajectory & Monofilament Map (Option 4)
# ─────────────────────────────────────────────────────────────────────────────
def build_trajectory():
    img, draw = new_screen()

    draw.text((20, 60), "NEUROPATHY DOSSIER", font=gf(10, bold=True), fill=PURPLE)
    draw.text((20, 78), "Foot Map & 30-Day Trend", font=gf(20, bold=True), fill=WHITE)
    draw.text((20, 104), "Semmes-Weinstein 10g Monofilament Protocol", font=gf(9), fill=MUTED)

    # Foot diagram card
    draw_card(draw, 18, 122, W-36, 295, r=14)
    draw.text((32, 136), "PLANTAR SENSORY PROFILE  ·  RIGHT FOOT", font=gf(10, bold=True), fill=MUTED)

    # Draw foot silhouette
    fx = W//2; fy = 245
    draw.ellipse([fx-55, fy-85, fx+55, fy+40], fill=CARD_SUB, outline=CARD_BDR, width=2)
    draw.ellipse([fx-40, fy+28, fx+40, fy+105], fill=CARD_SUB, outline=CARD_BDR, width=2)

    pts = [
        (fx-28, fy-68, "1", RED), (fx-8, fy-70, "2", RED),  (fx+15, fy-64, "3", EMERALD),
        (fx-36, fy-36, "4", RED), (fx+2,  fy-36, "5", RED),  (fx+32, fy-36, "6", EMERALD),
        (fx-24, fy+4,  "7", EMERALD), (fx+24, fy+4, "8", EMERALD),
        (fx-14, fy+58, "9", EMERALD), (fx+14, fy+58, "10", EMERALD),
    ]
    for px, py, num, col in pts:
        draw.ellipse([px-11, py-11, px+11, py+11], fill=col)
        draw.text((px, py), num, font=gf(9, bold=True), fill=WHITE, anchor="mm")

    # Legend
    draw.rounded_rectangle([28, fy+120, W-28, fy+148], radius=6, fill=CARD_SUB)
    draw.text((40, fy+134), "●  Intact (6/10)", font=gf(10, bold=True), fill=EMERALD, anchor="lm")
    draw.text((W-40, fy+134), "●  Loss of Protection (4/10)", font=gf(10, bold=True), fill=RED, anchor="rm")

    # 30-Day chart
    ch_y = 436
    draw_card(draw, 18, ch_y, W-36, 215, r=14)
    draw.text((32, ch_y+14), "30-DAY WOUND AREA REGRESSION (cm²)", font=gf(10, bold=True), fill=MUTED)

    ax0, ay0 = 44, ch_y+175
    ax1, ay1 = W-44, ch_y+60
    draw.line([ax0, ay0, ax1, ay0], fill=CARD_BDR, width=1)
    draw.line([ax0, ay0, ax0, ay1], fill=CARD_BDR, width=1)

    chart_pts = [(ax0, ay0-80), (ax0+75, ay0-62), (ax0+155, ay0-47), (ax0+245, ay0-32), (ax1, ay0-15)]
    labels = ["5.2 cm²", "4.7 cm²", "4.1 cm²", "3.84 cm²", "Target"]
    for i in range(len(chart_pts)-1):
        x1_, y1_ = chart_pts[i]
        x2_, y2_ = chart_pts[i+1]
        draw.line([x1_, y1_, x2_, y2_], fill=EMERALD, width=3)
        draw.ellipse([x1_-5, y1_-5, x1_+5, y1_+5], fill=EMERALD)
    draw.ellipse([chart_pts[-1][0]-5, chart_pts[-1][1]-5, chart_pts[-1][0]+5, chart_pts[-1][1]+5], fill=AMBER)

    for i, (px, py) in enumerate(chart_pts[:-1]):
        draw.text((px, ay0+10), ["D1","D7","D14","D21"][i], font=gf(8), fill=DIM, anchor="mm")
    draw.text((chart_pts[-1][0], ay0+10), "D30", font=gf(8), fill=DIM, anchor="mm")

    draw.text((32, ch_y+192), "Clinical Trend: −26.1% area  ·  Steady Contraction", font=gf(10, bold=True), fill=EMERALD)

    draw.rounded_rectangle([18, ch_y+220, W-18, ch_y+272], radius=14, fill=BLUE)
    draw.text((W//2, ch_y+246), "Export Full Longitudinal Dossier  →", font=gf(12, bold=True), fill=WHITE, anchor="mm")

    return phone_frame(img)

# ─────────────────────────────────────────────────────────────────────────────
# WIDE PANEL: Real Doctor Dashboard screenshot in tablet frame
# ─────────────────────────────────────────────────────────────────────────────
def build_real_dashboard_tablet():
    im = Image.open("real_screenshots/media_1790882283619.png").convert("RGBA")
    return tablet_frame(im, sw=900, sh=620)

# ─────────────────────────────────────────────────────────────────────────────
# WIDE PANEL: AI Segmentation + Wound Annotated side by side
# ─────────────────────────────────────────────────────────────────────────────
def build_ai_segmentation_panel():
    W2, H2 = 1080, 440
    panel = Image.new("RGBA", (W2, H2), CARD_BG)
    draw = ImageDraw.Draw(panel)

    # Header
    draw.text((20, 14), "AI COMPUTER VISION SEGMENTATION  ·  Mask R-CNN ResNet-50  +  YOLOv8 Calibrant Coin Detector", font=gf(12, bold=True), fill=EMERALD)
    draw.text((20, 36), "Patient: Subhash Mondal (PAT-KGP-004)  ·  Visit #4  ·  Photo 3 (Calibrated Macro Close-Up)", font=gf(10), fill=MUTED)

    # Real annotated wound photo
    wound = Image.open("stored_photos/PAT_KGP_01_VIS_004_measurement_annotated_20261001_200842.jpg").convert("RGBA")
    wound_resized = wound.resize((360, 360), Image.Resampling.LANCZOS)
    panel.paste(wound_resized, (20, 62), wound_resized)

    # Real AI review screenshot
    ai_sc = Image.open("real_screenshots/media_1790880676182.png").convert("RGBA")
    ai_resized = ai_sc.resize((210, 360), Image.Resampling.LANCZOS)
    panel.paste(ai_resized, (396, 62), ai_resized)

    # Metrics panel on the right
    mx = 626; my = 62
    draw.rounded_rectangle([mx, my, W2-20, my+360], radius=14, fill=CARD_BG, outline=CARD_BDR, width=1)
    draw.text((mx+18, my+14), "DIMENSIONAL METRICS  (Sub-mm Precision)", font=gf(11, bold=True), fill=MUTED)

    met = [
        ("Max Length (Feret)", "39.8 mm"),
        ("Max Width (Orthogonal)", "25.1 mm"),
        ("2D Surface Area", "7.773 cm²"),
        ("Perimeter", "108.5 mm"),
        ("Segmentation Conf.", "88%  (IoU 91.4%)"),
        ("Tissue Composition:", ""),
        ("  Granulation (Red)", "62%"),
        ("  Fibrinous Slough (Yellow)", "28%"),
        ("  Epithelial Edge (Pink)", "10%"),
        ("Calibrant Coin", "24.0 mm  ·  18.6 px/mm"),
        ("Wagner Grade (AI)", "Grade 2  (Deep Ulcer)"),
        ("Cellulitis Screen", "Negative  (Score: 0.12)"),
    ]
    row_y = my + 44
    for lab, val in met:
        if not val:
            draw.text((mx+18, row_y), lab, font=gf(9, bold=True), fill=BLUE_L)
        else:
            col = EMERALD if "88%" in val or "91" in val else (AMBER if "cm²" in val or "mm" in val else WHITE)
            draw.text((mx+18, row_y), lab, font=gf(9), fill=MUTED)
            draw.text((W2-28, row_y), val, font=gf(9, bold=True), fill=col, anchor="rm")
        row_y += 25

    # Label under wound image
    draw.text((20+180, 432), "AI Mask Overlay  (Red=Wound, Blue=Coin Calibrant)", font=gf(10), fill=MUTED, anchor="mm")
    draw.text((396+105, 432), "App: AI Analysis & Review Screen", font=gf(10), fill=MUTED, anchor="mm")

    return panel

# ─────────────────────────────────────────────────────────────────────────────
# ASHA Offline Queue screen
# ─────────────────────────────────────────────────────────────────────────────
def build_asha_queue():
    img, draw = new_screen()

    draw.text((20, 60), "ASHA FIELD WORKER PORTAL", font=gf(10, bold=True), fill=AMBER)
    draw.text((20, 78), "Offline Queue & Sync", font=gf(20, bold=True), fill=WHITE)
    draw.text((20, 104), "ASHA: Priya Das  ·  Sector: Debra Rural Block", font=gf(9), fill=MUTED)

    # Sync status
    draw.rounded_rectangle([18, 122, W-18, 258], radius=14, fill=CARD_BG, outline=AMBER, width=2)
    draw.text((32, 138), "LOCAL SQLITE ENCRYPTED QUEUE", font=gf(10, bold=True), fill=AMBER)
    draw.text((32, 162), "3 Sessions Pending Sync", font=gf(22, bold=True), fill=WHITE)
    draw.text((32, 192), "SQLCipher AES-256 GCM  ·  Device-encrypted", font=gf(10), fill=MUTED)
    draw_pill(draw, 32, 214, 225, 30, fill=AM_BG, text="NETWORK: 2G / EDGE  (Retry armed)", font_size=9, text_fill=AMBER)

    # Queue items
    items = [
        ("PAT-KGP-005  ·  Tapan Roy (62M)", "3 Photos  ·  Wagner 2  ·  Debra Sub-center", "Queued (12.4 MB)  ·  Ready to push", AMBER),
        ("PAT-KGP-006  ·  Gita Mallick (55F)", "3 Photos  ·  Neuropathy Screening", "Queued (14.1 MB)  ·  Ready to push", AMBER),
        ("PAT-KGP-007  ·  Biren Mahato (70M)", "3 Photos  ·  Measurement  ·  Keshpur", "Queued (11.8 MB)  ·  Ready to push", AMBER),
    ]
    iy = 270
    draw_card(draw, 18, iy, W-36, 305, r=14)
    draw.text((32, iy+14), "PENDING CLINICAL DATA PACKETS", font=gf(10, bold=True), fill=MUTED)
    py = iy + 40
    for title, sub, stat, col in items:
        draw.rounded_rectangle([28, py, W-28, py+72], radius=10, fill=CARD_SUB, outline=CARD_BDR, width=1)
        draw.text((38, py+12), title, font=gf(11, bold=True), fill=WHITE)
        draw.text((38, py+30), sub, font=gf(9), fill=MUTED)
        draw.text((38, py+50), stat, font=gf(9, bold=True), fill=col)
        py += 82

    # Sync button
    by = iy+312
    draw.rounded_rectangle([18, by, W-18, by+62], radius=14, fill=EMERALD)
    draw.text((W//2, by+31), "Sync All Sessions  →  Apex Master (FastAPI)", font=gf(13, bold=True), fill=WHITE, anchor="mm")
    draw.text((W//2, by+80), "Auto-retry on drop  ·  Zero packet duplication", font=gf(9), fill=DIM, anchor="mm")

    return phone_frame(img)

# ─────────────────────────────────────────────────────────────────────────────
# SYSTEM ARCHITECTURE DIAGRAM (landscape wide)
# ─────────────────────────────────────────────────────────────────────────────
def build_arch_diagram():
    W2, H2 = 1080, 540
    img = Image.new("RGBA", (W2, H2), NAVY)
    draw = ImageDraw.Draw(img)

    draw.text((30, 18), "DIABETESCARE AI  —  HYBRID EDGE-TO-APEX CLINICAL TOPOLOGY", font=gf(14, bold=True), fill=BLUE_L)
    draw.text((30, 42), "CDSCO Class B SaMD  ·  IIT Kharagpur & Midnapore Medical College  ·  Paschim Medinipur Apex Hub", font=gf(11), fill=MUTED)

    tiers = [
        ("TIER 1\nPOINT-OF-CARE", ["Mobile App\n(React Native)", "Offline SQLite\nAES-256 Encrypted", "Camera2 Raw\nAPI Capture", "ASHA Edge\nSync Queue"], EMERALD, 30),
        ("TIER 2\nAPEX GATEWAY", ["FastAPI Master\n(:8000)", "Nginx Reverse\nProxy", "TLS 1.3 / HMAC\nToken Auth", "RBAC Role\nValidation"], BLUE_L, 290),
        ("TIER 3\nINFERENCE PIPELINE", ["Mask R-CNN\nResNet-50", "YOLOv8 Calibrant\nCoin Detector", "EfficientNet-B0\nWagner 0-5", "ResNet-18\nCellulitis CLF"], PURPLE, 550),
        ("TIER 4\nCLINICAL DATA LAKE", ["PostgreSQL\nMaster DB", "ABDM M4 &\neSanjeevani", "DICOM Image\nStore (Encrypted)", "Audit Vault\n(Immutable Log)"], AMBER, 810),
    ]

    for title, items, col, x in tiers:
        cw = 220
        draw.rounded_rectangle([x, 75, x+cw, 510], radius=14, fill=CARD_BG, outline=col, width=2)
        draw.rounded_rectangle([x, 75, x+cw, 120], radius=10, fill=col)
        draw.text((x+cw//2, 97), title, font=gf(11, bold=True), fill=WHITE, anchor="mm")
        iy = 132
        for item in items:
            draw.rounded_rectangle([x+12, iy, x+cw-12, iy+80], radius=10, fill=CARD_SUB, outline=CARD_BDR, width=1)
            draw.text((x+cw//2, iy+40), item, font=gf(11, bold=True), fill=WHITE, anchor="mm", spacing=3)
            iy += 94

    # Arrows
    for ax in [250, 510, 770]:
        draw.polygon([(ax+20, 295), (ax+5, 285), (ax+5, 305)], fill=WHITE)
        draw.line([(ax, 295), (ax+20, 295)], fill=WHITE, width=2)

    return img

# ─────────────────────────────────────────────────────────────────────────────
# CV PIPELINE DIAGRAM
# ─────────────────────────────────────────────────────────────────────────────
def build_cv_pipeline():
    W2, H2 = 1080, 480
    img = Image.new("RGBA", (W2, H2), NAVY)
    draw = ImageDraw.Draw(img)

    draw.text((30, 18), "COMPUTER VISION & AI INFERENCE PIPELINE  —  Multi-Model Diagnostic Cascade", font=gf(14, bold=True), fill=EMERALD)
    draw.text((30, 42), "Photo Quality  →  Coin Calibration  →  Wound Segmentation  →  Wagner Classification  →  Physician Concordance Verification", font=gf(10), fill=MUTED)

    steps = [
        ("STAGE 1\nACQUISITION", ["3-Angle Capture\n(90°, 45°, Macro)", "Laplacian Blur\nVar ≥200", "Illuminance QA\n300-1200 lux", "Gyro Tilt\n≤5° Planar"], BLUE, 30),
        ("STAGE 2\nSEGMENTATION", ["YOLOv8 Coin\nDetector (24mm)", "Mask R-CNN\nWound Polygon", "Green's Theorem\nArea in cm²", "Tissue Comp %\nGranulation/Slough"], EMERALD, 290),
        ("STAGE 3\nCLASSIFICATION", ["EfficientNet-B0\nWagner 0-5", "ResNet-18\nCellulitis Binary", "Temperature\nScaling Calib.", "Wilson 95% CI\nUncertainty Band"], PURPLE, 550),
        ("STAGE 4\nVERIFICATION", ["Doctor Manual\nImpression Entry", "Concordance\nEngine ≥90%", "Atomic DB\nCommit (WAL)", "SSE Broadcast\n<450ms Live"], RED, 810),
    ]

    for title, items, col, x in steps:
        cw = 220
        draw.rounded_rectangle([x, 75, x+cw, 450], radius=14, fill=CARD_BG, outline=col, width=2)
        draw.rounded_rectangle([x, 75, x+cw, 120], radius=10, fill=col)
        draw.text((x+cw//2, 97), title, font=gf(11, bold=True), fill=WHITE, anchor="mm")
        iy = 132
        for item in items:
            draw.rounded_rectangle([x+12, iy, x+cw-12, iy+72], radius=10, fill=CARD_SUB, outline=CARD_BDR, width=1)
            draw.text((x+cw//2, iy+36), item, font=gf(11, bold=True), fill=WHITE, anchor="mm", spacing=3)
            iy += 82

    for ax in [250, 510, 770]:
        draw.polygon([(ax+20, 263), (ax+5, 253), (ax+5, 273)], fill=WHITE)
        draw.line([(ax, 263), (ax+20, 263)], fill=WHITE, width=2)

    return img

# ─────────────────────────────────────────────────────────────────────────────
# MAIN ORCHESTRATION
# ─────────────────────────────────────────────────────────────────────────────
def run_all():
    print("Building all manual assets with real screenshots & accurate UI...")

    # Architecture diagrams
    build_arch_diagram().save(os.path.join(OUT_DIR, "arch_diagram.png"))
    print("  [OK] arch_diagram.png")

    build_cv_pipeline().save(os.path.join(OUT_DIR, "cv_pipeline.png"))
    print("  [OK] cv_pipeline.png")

    # Phone screen mockups
    build_login().save(os.path.join(OUT_DIR, "screen_login.png"))
    print("  [OK] screen_login.png")

    build_registration().save(os.path.join(OUT_DIR, "screen_registration.png"))
    print("  [OK] screen_registration.png")

    build_3photo_lock().save(os.path.join(OUT_DIR, "screen_3photo_lock.png"))
    print("  [OK] screen_3photo_lock.png  [Bug Fix #1]")

    build_camera_hud().save(os.path.join(OUT_DIR, "screen_camera_hud.png"))
    print("  [OK] screen_camera_hud.png")

    build_ai_review_real().save(os.path.join(OUT_DIR, "screen_ai_review_real.png"))
    print("  [OK] screen_ai_review_real.png  [REAL APP SCREENSHOT]")

    build_doctor_diagnosis().save(os.path.join(OUT_DIR, "screen_doctor_diagnosis.png"))
    print("  [OK] screen_doctor_diagnosis.png  [Bug Fix #2]")

    build_doctor_hub().save(os.path.join(OUT_DIR, "screen_doctor_hub.png"))
    print("  [OK] screen_doctor_hub.png  [Bug Fix #3]")

    build_healing_journey().save(os.path.join(OUT_DIR, "screen_healing_journey.png"))
    print("  [OK] screen_healing_journey.png")

    build_teleconsult().save(os.path.join(OUT_DIR, "screen_teleconsult.png"))
    print("  [OK] screen_teleconsult.png")

    build_trajectory().save(os.path.join(OUT_DIR, "screen_trajectory.png"))
    print("  [OK] screen_trajectory.png")

    build_asha_queue().save(os.path.join(OUT_DIR, "screen_asha_queue.png"))
    print("  [OK] screen_asha_queue.png")

    # Wide panels
    build_real_dashboard_tablet().save(os.path.join(OUT_DIR, "panel_doctor_dashboard.png"))
    print("  [OK] panel_doctor_dashboard.png  [REAL DASHBOARD SCREENSHOT]")

    build_ai_segmentation_panel().save(os.path.join(OUT_DIR, "panel_ai_segmentation.png"))
    print("  [OK] panel_ai_segmentation.png  [REAL WOUND PHOTO + REAL APP SCREENSHOT]")

    print("\nAll assets generated successfully!")

if __name__ == "__main__":
    run_all()
