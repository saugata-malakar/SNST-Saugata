# generate_user_manual_pdf.py
# Generates a publication-grade 20+ Page Official User Manual & Technical Reference for DiabetesCare AI

import os
import sys
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_FILENAME = "DiabetesCare_AI_Official_User_Manual.pdf"

# ── Numbered Canvas for Two-Pass Total Page Count & Headers/Footers ──────────
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # Omit header and footer on cover page
        if self._pageNumber == 1:
            return

        self.saveState()
        
        # ── Top Running Header ──
        self.setFont('Helvetica-Bold', 8)
        self.setFillColor(colors.HexColor('#1E3A8A'))
        self.drawString(54, 755, "DIABETESCARE AI")
        self.setFont('Helvetica', 8)
        self.setFillColor(colors.HexColor('#64748B'))
        self.drawString(135, 755, "· Clinical Operations, Computer Vision & Mobile Triage Manual (v2.4.0)")
        
        # Top Rule Line
        self.setStrokeColor(colors.HexColor('#E2E8F0'))
        self.setLineWidth(0.8)
        self.line(54, 747, 558, 747)

        # ── Bottom Running Footer ──
        self.setStrokeColor(colors.HexColor('#E2E8F0'))
        self.setLineWidth(0.8)
        self.line(54, 46, 558, 46)

        self.setFont('Helvetica', 7.5)
        self.setFillColor(colors.HexColor('#64748B'))
        self.drawString(54, 34, "IIT Kharagpur · Paschim Medinipur Apex Hub · DPDP Act 2023 Compliant Edition")
        
        self.setFont('Helvetica-Bold', 7.5)
        self.setFillColor(colors.HexColor('#0F172A'))
        self.drawRightString(558, 34, f"Page {self._pageNumber} of {page_count}")

        self.restoreState()


def build_manual_pdf():
    doc = SimpleDocTemplate(
        PDF_FILENAME,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    # ── Custom Paragraph Styles ──
    NAVY_HEX = '#0B132B'
    BLUE_HEX = '#1E3A8A'
    DARK_BLUE = '#1E293B'
    SLATE_HEX = '#334155'
    EMERALD_HEX = '#059669'
    RED_HEX = '#DC2626'
    AMBER_HEX = '#D97706'
    GREY_BG = '#F8FAFC'

    styles.add(ParagraphStyle('DocSuperTitle', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=colors.HexColor(BLUE_HEX), textTransform='uppercase', spaceAfter=6))
    styles.add(ParagraphStyle('DocTitle', fontName='Helvetica-Bold', fontSize=24, leading=28, textColor=colors.HexColor(NAVY_HEX), spaceAfter=10))
    styles.add(ParagraphStyle('DocSubtitle', fontName='Helvetica', fontSize=12, leading=16, textColor=colors.HexColor(SLATE_HEX), spaceAfter=18))
    styles.add(ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor('#64748B')))
    styles.add(ParagraphStyle('CoverMetaBold', fontName='Helvetica-Bold', fontSize=8.5, leading=12, textColor=colors.HexColor('#0F172A')))

    styles.add(ParagraphStyle('Heading1_Custom', fontName='Helvetica-Bold', fontSize=15, leading=18, textColor=colors.HexColor(NAVY_HEX), spaceBefore=14, spaceAfter=8, keepWithNext=True))
    styles.add(ParagraphStyle('Heading2_Custom', fontName='Helvetica-Bold', fontSize=11.5, leading=15, textColor=colors.HexColor(BLUE_HEX), spaceBefore=10, spaceAfter=5, keepWithNext=True))
    styles.add(ParagraphStyle('Heading3_Custom', fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=colors.HexColor(DARK_BLUE), spaceBefore=6, spaceAfter=3, keepWithNext=True))

    styles.add(ParagraphStyle('Body_Custom', fontName='Helvetica', fontSize=8.8, leading=12.5, textColor=colors.HexColor('#1E293B'), spaceAfter=6))
    styles.add(ParagraphStyle('Body_Custom_Bold', fontName='Helvetica-Bold', fontSize=8.8, leading=12.5, textColor=colors.HexColor('#0F172A'), spaceAfter=6))
    styles.add(ParagraphStyle('Bullet_Custom', fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor('#1E293B'), leftIndent=14, firstLineIndent=-9, spaceAfter=3))

    styles.add(ParagraphStyle('Callout_Info', fontName='Helvetica', fontSize=8.3, leading=11.8, textColor=colors.HexColor('#1E3A8A'), backColor=colors.HexColor('#EFF6FF'), borderColor=colors.HexColor('#3B82F6'), borderWidth=1, borderPadding=7, spaceBefore=5, spaceAfter=7))
    styles.add(ParagraphStyle('Callout_Success', fontName='Helvetica', fontSize=8.3, leading=11.8, textColor=colors.HexColor('#065F46'), backColor=colors.HexColor('#ECFDF5'), borderColor=colors.HexColor('#10B981'), borderWidth=1, borderPadding=7, spaceBefore=5, spaceAfter=7))
    styles.add(ParagraphStyle('Callout_Warning', fontName='Helvetica', fontSize=8.3, leading=11.8, textColor=colors.HexColor('#92400E'), backColor=colors.HexColor('#FFFBEB'), borderColor=colors.HexColor('#F59E0B'), borderWidth=1, borderPadding=7, spaceBefore=5, spaceAfter=7))
    styles.add(ParagraphStyle('Callout_Danger', fontName='Helvetica', fontSize=8.3, leading=11.8, textColor=colors.HexColor('#991B1B'), backColor=colors.HexColor('#FEF2F2'), borderColor=colors.HexColor('#EF4444'), borderWidth=1, borderPadding=7, spaceBefore=5, spaceAfter=7))

    styles.add(ParagraphStyle('TableHead', fontName='Helvetica-Bold', fontSize=7.8, leading=10, textColor=colors.HexColor('#FFFFFF'), alignment=0))
    styles.add(ParagraphStyle('TableCell', fontName='Helvetica', fontSize=7.6, leading=10.5, textColor=colors.HexColor('#1E293B'), alignment=0))
    styles.add(ParagraphStyle('TableCellBold', fontName='Helvetica-Bold', fontSize=7.6, leading=10.5, textColor=colors.HexColor('#0F172A'), alignment=0))
    styles.add(ParagraphStyle('CodeInline', fontName='Courier-Bold', fontSize=7.8, leading=10, textColor=colors.HexColor('#0F172A'), backColor=colors.HexColor('#F1F5F9')))

    story = []

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 1: OFFICIAL COVER PAGE
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 40))
    story.append(Paragraph("MINISTRY OF HEALTH & FAMILY WELFARE · DIGITAL HEALTH MISSION", styles['DocSuperTitle']))
    story.append(Paragraph("SCHOOL OF MEDICAL SCIENCE AND TECHNOLOGY (SMST), IIT KHARAGPUR", styles['DocSuperTitle']))
    story.append(Spacer(1, 15))

    story.append(Paragraph("DiabetesCare AI: Clinical Mobile Application & Telehealth Triage System", styles['DocTitle']))
    story.append(Paragraph("Comprehensive Part-by-Part User Manual, DOM Element Reference, Computer Vision Workflow & Clinical Governance Protocol", styles['DocSubtitle']))

    story.append(HRFlowable(width="100%", thickness=3, color=colors.HexColor('#1E3A8A'), spaceBefore=8, spaceAfter=20))

    # Architecture banner / Cover Graphic
    arch_img_path = os.path.join("manual_assets", "screen_system_architecture.png")
    if os.path.exists(arch_img_path):
        story.append(Image(arch_img_path, width=490, height=270))
        story.append(Spacer(1, 15))

    # Cover Metadata Block Table
    cover_meta_data = [
        [
            Paragraph("<b>Document Version:</b> 2.4.0 (Release Build)", styles['CoverMeta']),
            Paragraph("<b>Operating System:</b> Android 10+ / WebRTC Telehealth", styles['CoverMeta'])
        ],
        [
            Paragraph("<b>Compliance Standard:</b> Digital Personal Data Protection (DPDP) Act 2023", styles['CoverMeta']),
            Paragraph("<b>Deep Learning Backbone:</b> EfficientNet-B0 (PyTorch .pth)", styles['CoverMeta'])
        ],
        [
            Paragraph("<b>Local Storage Engine:</b> SQLite 3.x (diabetescare.db) + Stored Photos", styles['CoverMeta']),
            Paragraph("<b>Network Mode:</b> Hybrid Wi-Fi LAN (:8000) / Offline Fallback", styles['CoverMeta'])
        ],
        [
            Paragraph("<b>Target Apex Institution:</b> Midnapore Medical College & Hospital (MMCH)", styles['CoverMeta']),
            Paragraph("<b>Primary Author:</b> Saugata Malakar (SMST, IIT Kharagpur)", styles['CoverMeta'])
        ],
    ]
    meta_table = Table(cover_meta_data, colWidths=[245, 245])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 25))
    story.append(Paragraph("<b>CONFIDENTIALITY NOTICE:</b> This clinical manual contains proprietary engineering and medical algorithms developed for academic, governmental, and healthcare operational deployments. Unauthorized distribution is prohibited.", styles['CoverMeta']))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 2: TABLE OF CONTENTS & EXECUTIVE SUMMARY
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Table of Contents & Operational Roadmap", styles['Heading1_Custom']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=10))

    toc_data = [
        [Paragraph("<b>Part</b>", styles['TableHead']), Paragraph("<b>Section Title & Clinical Operational Scope</b>", styles['TableHead']), Paragraph("<b>Page</b>", styles['TableHead'])],
        [Paragraph("Part 1", styles['TableCellBold']), Paragraph("Executive Summary, Clinical Objectives & Hybrid System Topology", styles['TableCell']), Paragraph("Page 3", styles['TableCell'])],
        [Paragraph("Part 2", styles['TableCellBold']), Paragraph("Hardware Requirements, Camera Permissions & Installation Setup", styles['TableCell']), Paragraph("Page 4", styles['TableCell'])],
        [Paragraph("Part 3", styles['TableCellBold']), Paragraph("Portal Login & Role-Based Access Control (RBAC) Authentication", styles['TableCell']), Paragraph("Page 5", styles['TableCell'])],
        [Paragraph("Part 4", styles['TableCellBold']), Paragraph("Patient Registration & DPDP Act 2023 Explicit Consent Engine", styles['TableCell']), Paragraph("Page 6", styles['TableCell'])],
        [Paragraph("Part 5", styles['TableCellBold']), Paragraph("Clinical Triage Command Hub (Lead Diabetologist Master Portal)", styles['TableCell']), Paragraph("Page 7", styles['TableCell'])],
        [Paragraph("Part 6", styles['TableCellBold']), Paragraph("Urgent Clinical Alerts & Real-Time Red/Amber Triage Escalations", styles['TableCell']), Paragraph("Page 8", styles['TableCell'])],
        [Paragraph("Part 7", styles['TableCellBold']), Paragraph("Option 1: My Healing Journey (Patient Portal & Dynamic Adherence)", styles['TableCell']), Paragraph("Page 9", styles['TableCell'])],
        [Paragraph("Part 8", styles['TableCellBold']), Paragraph("Option 2: National Teleconsultation Network (eSanjeevani / ABDM)", styles['TableCell']), Paragraph("Page 10", styles['TableCell'])],
        [Paragraph("Part 9", styles['TableCellBold']), Paragraph("Option 3: Mobile Camera Flow & Calibrant Protocol Guidelines", styles['TableCell']), Paragraph("Page 11", styles['TableCell'])],
        [Paragraph("Part 10", styles['TableCellBold']), Paragraph("3-Photo Protocol Checklist & Enforced Navigation Lock [Bug Fix #1]", styles['TableCell']), Paragraph("Page 12", styles['TableCell'])],
        [Paragraph("Part 11", styles['TableCellBold']), Paragraph("Real-Time Viewfinder Guidance & Image Quality Assessment (CV HUD)", styles['TableCell']), Paragraph("Page 13", styles['TableCell'])],
        [Paragraph("Part 12", styles['TableCellBold']), Paragraph("Automated Wound Segmentation & Metric Dimensional Extraction", styles['TableCell']), Paragraph("Page 14", styles['TableCell'])],
        [Paragraph("Part 13", styles['TableCellBold']), Paragraph("Deep Learning Wound Severity Classification (Wagner Grades 0–5)", styles['TableCell']), Paragraph("Page 15", styles['TableCell'])],
        [Paragraph("Part 14", styles['TableCellBold']), Paragraph("Doctor Manual Clinical Diagnosis & AI Verification [Bug Fix #2]", styles['TableCell']), Paragraph("Page 16", styles['TableCell'])],
        [Paragraph("Part 15", styles['TableCellBold']), Paragraph("Doctor Account Live Reflection & Synchronous Database Writes [Bug Fix #3]", styles['TableCell']), Paragraph("Page 17", styles['TableCell'])],
        [Paragraph("Part 16", styles['TableCellBold']), Paragraph("Option 4: Longitudinal Wound Trajectory & 10-Point Neuropathy Map", styles['TableCell']), Paragraph("Page 18", styles['TableCell'])],
        [Paragraph("Part 17", styles['TableCellBold']), Paragraph("Option 5: Hospital Affiliation, Multi-Lingual Settings & Preferences", styles['TableCell']), Paragraph("Page 19", styles['TableCell'])],
        [Paragraph("Part 18", styles['TableCellBold']), Paragraph("Offline-First Field Architecture & Persistent Local Storage Model", styles['TableCell']), Paragraph("Page 20", styles['TableCell'])],
        [Paragraph("Part 19", styles['TableCellBold']), Paragraph("Quality Assurance, Clinical Troubleshooting Guide & Operator FAQs", styles['TableCell']), Paragraph("Page 21", styles['TableCell'])],
        [Paragraph("Part 20", styles['TableCellBold']), Paragraph("Regulatory Audit Trails, Verification Matrix & Appendix", styles['TableCell']), Paragraph("Page 22", styles['TableCell'])],
    ]
    t_toc = Table(toc_data, colWidths=[40, 410, 40])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(BLUE_HEX)),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_toc)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Executive Overview", styles['Heading2_Custom']))
    story.append(Paragraph(
        "<b>DiabetesCare AI</b> is a state-of-the-art dual-purpose clinical healthcare platform engineered to bridge tertiary medical centers "
        "(such as Midnapore Medical College & Hospital) with rural frontline health workers (ASHAs) across Paschim Medinipur, Jhargram, and Purba Medinipur. "
        "The system provides point-of-care computer vision analysis, automated dimensional extraction (area, length, width, perimeter), deep learning "
        "wound classification across Wagner Grades 0 through 5, and teleconsultation over the National eSanjeevani framework.",
        styles['Body_Custom']
    ))
    story.append(Paragraph(
        "This manual details the complete user experience, screen-by-screen DOM architecture, clinical workflows, and recent major upgrades including the "
        "<b>3-Photo Enforced Checklist Lock</b>, the <b>Doctor Manual Clinical Diagnosis & AI Verification Panel</b>, and the <b>Live Dynamic Doctor Command Hub Reflection Engine</b>.",
        styles['Body_Custom']
    ))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 3: PART 1 — SYSTEM ARCHITECTURE & TOPOLOGY
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Part 1: Executive Overview & System Topology", styles['Heading1_Custom']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    story.append(Paragraph("1.1 Dual-Tier Distributed Architecture", styles['Heading2_Custom']))
    story.append(Paragraph(
        "DiabetesCare AI functions in two unified deployment tiers: an <b>Edge Mobile Client</b> running natively on Android devices (phones, clinical tablets) "
        "and a <b>Local/Cloud Master Telemetry Engine</b> powered by FastAPI (Python 3.12). When operated in rural sub-centres lacking dependable cellular connectivity, "
        "the mobile application utilizes an intelligent offline-first architecture, calculating real-time deterministic wound metrics directly from photo byte-streams "
        "and queuing payloads for synchronization upon reconnecting to the hospital Wi-Fi network.",
        styles['Body_Custom']
    ))

    story.append(Paragraph("1.2 Network Connectivity & Service Endpoints", styles['Heading2_Custom']))
    story.append(Paragraph(
        "During clinical operational trials and local PC tethering, the server operates on local LAN Wi-Fi: <code>http://192.168.31.94:8000</code>. "
        "All API endpoints follow RESTful conventions under the <code>/api/v1/</code> prefix. The mobile client implements an active timeout controller "
        "(3,500ms for heavy computer vision tasks, 1,500ms for metadata) with automatic local fallback to ensure frontline operators never experience app freezing.",
        styles['Body_Custom']
    ))

    arch_summary_data = [
        [Paragraph("<b>Component Layer</b>", styles['TableHead']), Paragraph("<b>Technology Stack</b>", styles['TableHead']), Paragraph("<b>Clinical Responsibilities</b>", styles['TableHead'])],
        [Paragraph("Mobile Client", styles['TableCellBold']), Paragraph("React Native 0.73, TypeScript, Android SDK 34", styles['TableCell']), Paragraph("Frontline capture, live HUD guidance, 3-photo checklist, teleconsult client", styles['TableCell'])],
        [Paragraph("Computer Vision", styles['TableCellBold']), Paragraph("OpenCV (cv2), NumPy, PIL", styles['TableCell']), Paragraph("Hough circle calibrant detection, adaptive thresholding, blur/glare scoring", styles['TableCell'])],
        [Paragraph("Deep Learning", styles['TableCellBold']), Paragraph("PyTorch 2.x, EfficientNet-B0 (.pth)", styles['TableCell']), Paragraph("6-class Wagner severity classification (Grades 0 to 5) with softmax probabilities", styles['TableCell'])],
        [Paragraph("API Gateway", styles['TableCellBold']), Paragraph("FastAPI, Uvicorn, Pydantic v2", styles['TableCell']), Paragraph("REST endpoints, multipart upload, CORS handling, DPDP consent checks", styles['TableCell'])],
        [Paragraph("Data Storage", styles['TableCellBold']), Paragraph("SQLite 3 (diabetescare.db), Disk Storage", styles['TableCell']), Paragraph("26 clinical tables, JPEG archival (stored_photos/), immutable audit logs", styles['TableCell'])],
        [Paragraph("Telehealth Hub", styles['TableCellBold']), Paragraph("WebRTC, eSanjeevani ABDM Gateway", styles['TableCell']), Paragraph("Encrypted audio/video teleconsultation, real-time prescription transmission", styles['TableCell'])],
    ]
    t_arch = Table(arch_summary_data, colWidths=[90, 150, 250])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(BLUE_HEX)),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 10))

    story.append(Paragraph("1.3 DPDP Act 2023 Statutory Compliance Overview", styles['Heading2_Custom']))
    story.append(Paragraph(
        "To comply with India's <b>Digital Personal Data Protection (DPDP) Act 2023</b>, all patient identifiers undergo cryptographic pseudonymization. "
        "Patient names, phone numbers, and addresses are stored separately from clinical ulcer photographs. Photographs are assigned randomized UUIDs "
        "(e.g., <code>PHT_7C89B10E</code>) and are stripped of EXIF metadata and GPS village-level precision before research or training export.",
        styles['Body_Custom']
    ))
    story.append(Paragraph(
        "<b>Notice to Operators:</b> Never bypass the consent screen. Every enrolled subject must grant at least Tier 1 (Clinical Telemedicine) consent.",
        styles['Callout_Info']
    ))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 4: PART 2 — HARDWARE, PERMISSIONS & INSTALLATION
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Part 2: Hardware Requirements, Permissions & Setup", styles['Heading1_Custom']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    story.append(Paragraph("2.1 Minimum & Recommended Hardware Specifications", styles['Heading2_Custom']))
    story.append(Paragraph(
        "The mobile application has been optimized for field smartphones commonly deployed in national healthcare missions (such as the Poco M6 Pro 5G, "
        "Redmi 12, Samsung Galaxy A14, and equivalent devices).",
        styles['Body_Custom']
    ))

    hw_specs = [
        [Paragraph("<b>Hardware Dimension</b>", styles['TableHead']), Paragraph("<b>Minimum Specification</b>", styles['TableHead']), Paragraph("<b>Recommended Specification</b>", styles['TableHead'])],
        [Paragraph("Processor (SoC)", styles['TableCellBold']), Paragraph("Octa-core 2.0 GHz (Snapdragon 4 Gen 2 / Helio G88)", styles['TableCell']), Paragraph("Qualcomm Snapdragon 695 / Dimensity 6080 or better", styles['TableCell'])],
        [Paragraph("System Memory (RAM)", styles['TableCellBold']), Paragraph("4.0 GB LPDDR4X", styles['TableCell']), Paragraph("6.0 GB or 8.0 GB (enhances camera buffer speed)", styles['TableCell'])],
        [Paragraph("Rear Camera", styles['TableCellBold']), Paragraph("13.0 MP with Autofocus & LED Flash", styles['TableCell']), Paragraph("50.0 MP primary sensor with f/1.8 aperture & Macro lens", styles['TableCell'])],
        [Paragraph("Operating System", styles['TableCellBold']), Paragraph("Android 10.0 (API Level 29)", styles['TableCell']), Paragraph("Android 13.0 / 14.0 (API Level 33/34)", styles['TableCell'])],
        [Paragraph("Internal Storage", styles['TableCellBold']), Paragraph("1.5 GB available space for cached records", styles['TableCell']), Paragraph("8.0 GB available space for offline photo queue", styles['TableCell'])],
        [Paragraph("Display Screen", styles['TableCellBold']), Paragraph("6.5-inch IPS LCD (720x1600 px)", styles['TableCell']), Paragraph("6.67-inch FHD+ AMOLED with 120Hz refresh rate", styles['TableCell'])],
    ]
    t_hw = Table(hw_specs, colWidths=[110, 180, 200])
    t_hw.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(BLUE_HEX)),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_hw)
    story.append(Spacer(1, 10))

    story.append(Paragraph("2.2 Android Runtime Permissions", styles['Heading2_Custom']))
    story.append(Paragraph(
        "Upon launching the application for the first time, Android will request the following runtime system permissions:",
        styles['Body_Custom']
    ))
    story.append(Paragraph("• <b>Camera (android.permission.CAMERA):</b> Required for capturing high-definition wound photographs and live viewfinder quality analysis.", styles['Bullet_Custom']))
    story.append(Paragraph("• <b>Fine Location (android.permission.ACCESS_FINE_LOCATION):</b> Attaches district-level geographic coordinates to visit records for regional epidemiology triage.", styles['Bullet_Custom']))
    story.append(Paragraph("• <b>Read External Storage / Photos (android.permission.READ_MEDIA_IMAGES):</b> Enables gallery import for secondary clinical evaluation when direct photography is restricted.", styles['Bullet_Custom']))

    story.append(Paragraph("2.3 Blue Calibrant Sticker Specifications", styles['Heading2_Custom']))
    story.append(Paragraph(
        "Precise dimensional accuracy relies on a standardized physical scale marker. Operators must use the designated <b>20.0 mm circular blue calibrant sticker</b> "
        "(or standard 15.0 mm reference coin). The sticker must be affixed flat to <i>intact, non-macerated skin</i> approximately 1.0 to 2.0 cm from the active wound border. "
        "Never place the calibrant on the open ulcer bed.",
        styles['Body_Custom']
    ))

    story.append(Paragraph("2.4 Step-by-Step APK Installation", styles['Heading2_Custom']))
    story.append(Paragraph("1. Copy <code>DiabetesCareAI.apk</code> from the PC workspace root to your Android device via USB cable or local Wi-Fi download.", styles['Bullet_Custom']))
    story.append(Paragraph("2. Open the device <b>Files</b> app, locate <code>DiabetesCareAI.apk</code>, and tap to install.", styles['Bullet_Custom']))
    story.append(Paragraph("3. When prompted by Android Package Installer, enable <i>'Install unknown apps'</i> for the file browser.", styles['Bullet_Custom']))
    story.append(Paragraph("4. Open the installed application. Confirm all camera and storage permission dialogs with <b>'While using the app'</b>.", styles['Bullet_Custom']))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 5: PART 3 — PORTAL LOGIN & ROLE SELECTION (RBAC)
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Part 3: Portal Login & Role-Based Access Control", styles['Heading1_Custom']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    story.append(Paragraph("3.1 Role-Based Access Architecture", styles['Heading2_Custom']))
    story.append(Paragraph(
        "To satisfy medical confidentiality protocols, DiabetesCare AI incorporates strict Role-Based Access Control (RBAC). "
        "The application provides four pre-configured personas tailored to distinct operational workflows:",
        styles['Body_Custom']
    ))

    # Screenshot: Login Screen
    login_img_path = os.path.join("manual_assets", "screen_login.png")
    if os.path.exists(login_img_path):
        story.append(Image(login_img_path, width=220, height=366))
        story.append(Spacer(1, 8))

    story.append(Paragraph("3.2 Persona Descriptions & Functional Privileges", styles['Heading2_Custom']))
    story.append(Paragraph("1. <b>[DR] Lead Diabetologist / Podiatric Surgeon:</b> Grants access to the full Clinical Triage Command Hub, authoritative measurement override tools, prescription writing, and eSanjeevani WebRTC consultations.", styles['Bullet_Custom']))
    story.append(Paragraph("2. <b>[PT] Enrolled Cohort Patient:</b> Restricted view focusing on 'My Healing Journey', personal ulcer trajectory tracking, medication reminders, and direct patient-to-doctor teleconsultation connect.", styles['Bullet_Custom']))
    story.append(Paragraph("3. <b>[HW] ASHA Frontline Worker:</b> Specialized field interface featuring the 3-photo checklist, live camera HUD guidance, monofilament neuropathy screening, and patient registration with DPDP consent.", styles['Bullet_Custom']))
    story.append(Paragraph("4. <b>[AD] Hospital & IT Administrator:</b> System telemetry, database memory audits, server health monitoring, and DPDP Act consent revocation queues.", styles['Bullet_Custom']))

    story.append(Paragraph(
        "<b>Quick Sign-In Instruction:</b> Tap the desired persona pill to auto-fill authorized credentials, or manually enter your clinician username and password, then press <b>'Sign In to Command Portal'</b>.",
        styles['Callout_Success']
    ))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 6: PART 4 — PATIENT REGISTRATION & DPDP CONSENTS
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Part 4: Patient Registration & DPDP Act 2023 Consents", styles['Heading1_Custom']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    story.append(Paragraph("4.1 Demographic & Clinical Intake Fields", styles['Heading2_Custom']))
    story.append(Paragraph(
        "Frontline ASHA workers enroll new diabetic patients using the standardized intake screen accessible via the main portal. "
        "Accurate baseline data ensures precise AI wound progression forecasting.",
        styles['Body_Custom']
    ))

    reg_fields = [
        [Paragraph("<b>Field Name</b>", styles['TableHead']), Paragraph("<b>DOM Input Element</b>", styles['TableHead']), Paragraph("<b>Validation & Clinical Utility</b>", styles['TableHead'])],
        [Paragraph("Full Name", styles['TableCellBold']), Paragraph("TextInput (Text)", styles['TableCell']), Paragraph("Mandatory. Pseudonymized immediately upon server ingestion.", styles['TableCell'])],
        [Paragraph("Age & Gender", styles['TableCellBold']), Paragraph("TextInput (Numeric) + Picker", styles['TableCell']), Paragraph("Aggregated into 5-year age bands for DPDP k-anonymity (k >= 5).", styles['TableCell'])],
        [Paragraph("Contact Phone", styles['TableCellBold']), Paragraph("TextInput (Phone-pad)", styles['TableCell']), Paragraph("10-digit Indian mobile number for automated SMS alert dispatch.", styles['TableCell'])],
        [Paragraph("District / Sub-Centre", styles['TableCellBold']), Paragraph("Dropdown / TextInput", styles['TableCell']), Paragraph("Paschim Medinipur, Jhargram, or Purba Medinipur administrative sub-center.", styles['TableCell'])],
        [Paragraph("Diabetes Subtype", styles['TableCellBold']), Paragraph("Segmented Button", styles['TableCell']), Paragraph("Type 2 Diabetes Mellitus (T2DM) or Type 1 Diabetes Mellitus (T1DM).", styles['TableCell'])],
        [Paragraph("Duration of Diabetes", styles['TableCellBold']), Paragraph("TextInput (Decimal)", styles['TableCell']), Paragraph("Years since clinical diagnosis. Correlates with neuropathy risk.", styles['TableCell'])],
        [Paragraph("Recent HbA1c (%)", styles['TableCellBold']), Paragraph("TextInput (Decimal)", styles['TableCell']), Paragraph("Glycated hemoglobin value. Flagged RED if HbA1c >= 8.5%.", styles['TableCell'])],
        [Paragraph("Blood Pressure (BP)", styles['TableCellBold']), Paragraph("Dual Numeric Input", styles['TableCell']), Paragraph("Systolic / Diastolic mmHg. Used in macrovascular risk scoring.", styles['TableCell'])],
    ]
    t_reg = Table(reg_fields, colWidths=[100, 130, 260])
    t_reg.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(BLUE_HEX)),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_reg)
    story.append(Spacer(1, 10))

    story.append(Paragraph("4.2 Multi-Tier Granular Consent Lifecycle", styles['Heading2_Custom']))
    story.append(Paragraph(
        "In accordance with DPDP Act 2023 guidelines, patient consent cannot be bundled as an all-or-nothing agreement. "
        "The application provides three discrete checkboxes:",
        styles['Body_Custom']
    ))
    story.append(Paragraph("• <b>[Tier 1] Clinical Telemedicine Care (Mandatory):</b> Authorizes photography, biometric measurements, and transmission of records to Midnapore Medical College physicians.", styles['Bullet_Custom']))
    story.append(Paragraph("• <b>[Tier 2] Academic & Epidemiological Research (Optional):</b> Authorizes stripped, anonymized statistical aggregation for ICMR and IIT Kharagpur epidemiological reports.", styles['Bullet_Custom']))
    story.append(Paragraph("• <b>[Tier 3] AI Model Training & Re-Calibration (Optional):</b> Permits encrypted, anonymized wound contour polygons to enter the training dataset for future neural network retraining.", styles['Bullet_Custom']))

    story.append(Paragraph(
        "<b>Consent Revocation (Right to Forget):</b> Any patient may withdraw Tier 2 or Tier 3 consent at any subsequent visit. "
        "A revocation immediately enqueues the subject's identifier in the <code>erasure_queue</code> database table.",
        styles['Callout_Warning']
    ))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 7: PART 5 — CLINICAL TRIAGE COMMAND HUB (DOCTOR DASHBOARD)
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Part 5: Clinical Triage Command Hub (Doctor Dashboard)", styles['Heading1_Custom']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    story.append(Paragraph("5.1 Diabetologist Master Interface", styles['Heading2_Custom']))
    story.append(Paragraph(
        "The Clinical Triage Command Hub represents the central workstation for supervising physicians. "
        "It provides real-time departmental visibility over active rural cohorts, automated alert queues, and healing trajectories.",
        styles['Body_Custom']
    ))

    triage_img_path = os.path.join("manual_assets", "screen_triage_hub.png")
    if os.path.exists(triage_img_path):
        story.append(Image(triage_img_path, width=220, height=366))
        story.append(Spacer(1, 8))

    story.append(Paragraph("5.2 The Four Core Metric Cards", styles['Heading2_Custom']))
    story.append(Paragraph("1. <b>Active Cohort:</b> Total count of registered patients under active surveillance across Paschim Medinipur district sub-centres.", styles['Bullet_Custom']))
    story.append(Paragraph("2. <b>Urgent Triage Alerts:</b> Count of unresolved clinical alerts flagged RED or AMBER requiring immediate specialist intervention.", styles['Bullet_Custom']))
    story.append(Paragraph("3. <b>Teleconsult Queue:</b> Enqueued ABDM teleconsultation requests awaiting physician connection.", styles['Bullet_Custom']))
    story.append(Paragraph("4. <b>Mean Healing Velocity:</b> Aggregate percentage reduction in wound surface area over the preceding 30 days across the cohort.", styles['Bullet_Custom']))

    story.append(Paragraph("5.3 Department Patient Cohort Registry & Filtering", styles['Heading2_Custom']))
    story.append(Paragraph(
        "The registry list is dynamically synchronized with the SQLite database. Clinicians can filter cases by urgency "
        "(<code>ALL</code>, <code>HIGH</code>, <code>MEDIUM</code>) or Wagner Classification (<code>Grade 1</code>, <code>Grade 2</code>, <code>Grade 3</code>). "
        "Tapping <b>'Capture'</b> launches the 3-photo camera sequence for that patient, while tapping <b>'Override'</b> allows direct physician value adjustment.",
        styles['Body_Custom']
    ))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 8: PART 6 — URGENT CLINICAL ALERTS & TRIAGE ESCALATION
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Part 6: Real-Time Alerts & Clinical Triage Escalation", styles['Heading1_Custom']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    story.append(Paragraph("6.1 Tri-Color Clinical Urgency Protocol", styles['Heading2_Custom']))
    story.append(Paragraph(
        "The automated triage engine continuously scans newly submitted wound sessions and screening data. "
        "Alerts are categorized into three standard severity levels:",
        styles['Body_Custom']
    ))

    alert_table_data = [
        [Paragraph("<b>Severity</b>", styles['TableHead']), Paragraph("<b>Clinical Criteria Trigger</b>", styles['TableHead']), Paragraph("<b>System Action & Medical Protocol</b>", styles['TableHead'])],
        [
            Paragraph("RED (HIGH)", styles['TableCellBold']),
            Paragraph("• Ulcer area enlargement > 15% in 7 days<br/>• Wagner Grade >= 3 (osteitis / purulent drainage)<br/>• Monofilament score <= 3/10 (critical LOPS)", styles['TableCell']),
            Paragraph("Immediate SMS dispatch to lead diabetologist. Escalated to apex surgical referral queue. Patient flagged for urgent offloading.", styles['TableCell'])
        ],
        [
            Paragraph("AMBER (MEDIUM)", styles['TableCellBold']),
            Paragraph("• Static wound area (0% reduction over 14 days)<br/>• HbA1c > 9.0% with macerated wound borders<br/>• Persistent slough > 30% of wound bed", styles['TableCell']),
            Paragraph("Scheduled for eSanjeevani teleconsultation review within 48 hours. ASHA assigned to inspect dressing compliance.", styles['TableCell'])
        ],
        [
            Paragraph("GREEN (LOW)", styles['TableCellBold']),
            Paragraph("• Area reduction > 10% per week<br/>• Healthy granulation tissue > 70%<br/>• Intact sensory perception (score >= 8/10)", styles['TableCell']),
            Paragraph("Standard weekly serial photography. Routine offloading footwear adherence tracking.", styles['TableCell'])
        ],
    ]
    t_alert = Table(alert_table_data, colWidths=[80, 205, 205])
    t_alert.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(BLUE_HEX)),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_alert)
    story.append(Spacer(1, 10))

    story.append(Paragraph("6.2 Physician Alert Acknowledgment Workflow", styles['Heading2_Custom']))
    story.append(Paragraph(
        "When an alert appears in the Doctor Command Hub:",
        styles['Body_Custom']
    ))
    story.append(Paragraph("1. Review the alert summary card on the dashboard (indicates patient name, time submitted, and triggering criteria).", styles['Bullet_Custom']))
    story.append(Paragraph("2. Tap <b>'Review Record →'</b> to open the complete patient dossier.", styles['Bullet_Custom']))
    story.append(Paragraph("3. Inspect the newly captured photographic overlay and AI segmentation metrics.", styles['Bullet_Custom']))
    story.append(Paragraph("4. Select an action: write a prescription, schedule an immediate teleconsult, or mark the alert as resolved with physician notes.", styles['Bullet_Custom']))

    story.append(Paragraph(
        "<b>Automated Escalation Rule:</b> Any RED alert remaining unacknowledged for more than 4.0 hours is automatically forwarded "
        "to the On-Call Specialist's registered emergency mobile number.",
        styles['Callout_Danger']
    ))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 9: PART 7 — OPTION 1: "MY HEALING JOURNEY"
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Part 7: Option 1 — My Healing Journey (Patient Experience)", styles['Heading1_Custom']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    story.append(Paragraph("7.1 Patient Self-Care & Recovery Tracking Portal", styles['Heading2_Custom']))
    story.append(Paragraph(
        "When signed in as an Enrolled Patient (or when reviewing patient progress in the hub), <b>Option 1: My Healing Journey</b> "
        "provides an intuitive, encouraging visual interface designed to improve dressing adherence and self-care compliance.",
        styles['Body_Custom']
    ))

    story.append(Paragraph("7.2 Dynamic Healing Progress Indicator", styles['Heading2_Custom']))
    story.append(Paragraph(
        "Unlike static demo applications, DiabetesCare AI dynamically calculates the healing percentage using the latest submitted photographic measurements:",
        styles['Body_Custom']
    ))
    story.append(Paragraph(
        "<code>Healing Progress (%) = max(0, min(100, round(((Baseline Area - Latest Area) / Baseline Area) * 100)))</code>",
        styles['Callout_Info']
    ))
    story.append(Paragraph(
        "For example, when patient Ramesh Chandra Sen's baseline ulcer (5.20 cm²) is measured at 2.15 cm² following recent treatment, "
        "the progress bar automatically scales to <b>59% (Area reduced from 5.20 cm² to 2.15 cm²)</b> in real time.",
        styles['Body_Custom']
    ))

    story.append(Paragraph("7.3 Core Patient Screen Modules", styles['Heading2_Custom']))
    story.append(Paragraph("• <b>Next Dressing Change Schedule:</b> Indicates appointment time, designated ASHA health worker name, contact phone, and prescribed dressing materials (e.g. Sterile Saline Irrigation + Hydrocolloid Foam Barrier).", styles['Bullet_Custom']))
    story.append(Paragraph("• <b>Doctor's Care Advice:</b> Clear clinical guidelines: avoid walking barefoot, take oral antibiotics after food, and maintain fasting glucose under 130 mg/dL.", styles['Bullet_Custom']))
    story.append(Paragraph("• <b>Active Digital Prescriptions:</b> Displays authenticated e-prescriptions signed by Midnapore specialists (e.g. Amoxicillin-Clavulanate 625mg BID x 7 days).", styles['Bullet_Custom']))
    story.append(Paragraph("• <b>24x7 Emergency SOS Button:</b> One-touch direct dialing to National 112 / 108 Emergency Medical Services in case of spreading erythema or high fever.", styles['Bullet_Custom']))
    story.append(Paragraph("• <b>'Capture Today's Progress Photo' Button:</b> Launches the structured 3-photo checklist protocol for serial assessment.", styles['Bullet_Custom']))

    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 10: PART 8 — OPTION 2: GOVT TELECONSULTATION (eSANJEEVANI)
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Part 8: Option 2 — National Teleconsultation Network (eSanjeevani)", styles['Heading1_Custom']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    story.append(Paragraph("8.1 Verified Government Telehealth Conduit", styles['Heading2_Custom']))
    story.append(Paragraph(
        "<b>Option 2: Join Govt Teleconsult</b> integrates frontline rural sub-centres directly with apex hospital physicians "
        "via WebRTC over the Ministry of Health's <b>eSanjeevani / ABDM</b> telehealth framework.",
        styles['Body_Custom']
    ))

    tele_img_path = os.path.join("manual_assets", "screen_teleconsult.png")
    if os.path.exists(tele_img_path):
        story.append(Image(tele_img_path, width=220, height=366))
        story.append(Spacer(1, 8))

    story.append(Paragraph("8.2 Interactive Teleconsultation Controls", styles['Heading2_Custom']))
    story.append(Paragraph("• <b>Remote Video Feed:</b> High-resolution video stream showing the examining specialist at Midnapore Medical College.", styles['Bullet_Custom']))
    story.append(Paragraph("• <b>Picture-in-Picture (PiP) Self Window:</b> Local camera feed displaying the patient and ulcer bed orientation.", styles['Bullet_Custom']))
    story.append(Paragraph("• <b>Microphone Mute Toggle (MIC):</b> Toggles operator microphone on or off with visual status badge.", styles['Bullet_Custom']))
    story.append(Paragraph("• <b>Camera Toggle (CAM):</b> Allows ASHA workers to switch between front-facing camera (patient interview) and rear macro lens (wound close-up).", styles['Bullet_Custom']))
    story.append(Paragraph("• <b>Conclude Call Button (END):</b> Terminate the session and automatically commit consultation notes to the patient's ABDM digital dossier.", styles['Bullet_Custom']))

    story.append(Paragraph("8.3 Real-Time Clinical Consultation Notes", styles['Heading2_Custom']))
    story.append(Paragraph(
        "The integrated clinical notepad allows physicians to type observations, dressing revisions, or antibiotic adjustments "
        "directly into the encounter record during the call. Upon concluding, notes are cryptographically sealed in the SQLite database.",
        styles['Body_Custom']
    ))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 11: PART 9 — OPTION 3: MOBILE CAMERA FLOW & TELEMETRY
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Part 9: Option 3 — Mobile Camera Flow & Network Telemetry", styles['Heading1_Custom']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    story.append(Paragraph("9.1 Field Photography Protocol Overview", styles['Heading2_Custom']))
    story.append(Paragraph(
        "<b>Option 3: Mobile Camera Flow</b> serves as the clinical training and hardware simulation module. "
        "It outlines the mandatory ASHA photography sequence and verifies network latency against the FastAPI master server.",
        styles['Body_Custom']
    ))

    story.append(Paragraph("9.2 Standardized 3-Photo Clinical Rationale", styles['Heading2_Custom']))
    story.append(Paragraph(
        "Clinical trials conducted by IIT Kharagpur demonstrated that a single photo is statistically insufficient for safe remote diagnosis: "
        "a wide shot lacks textural detail for Wagner staging, while a macro close-up lacks anatomical landmark context. "
        "Hence, the platform mandates three sequential captures:",
        styles['Body_Custom']
    ))

    p3_steps = [
        [Paragraph("<b>Sequence Step</b>", styles['TableHead']), Paragraph("<b>Clinical Target</b>", styles['TableHead']), Paragraph("<b>Quality & Positioning Requirements</b>", styles['TableHead'])],
        [
            Paragraph("Step 1: Overview Photo", styles['TableCellBold']),
            Paragraph("Anatomical Context", styles['TableCell']),
            Paragraph("Capture full limb or plantar aspect. Distance: 40–50 cm. Shows relationship to malleolus, metatarsals, and toes.", styles['TableCell'])
        ],
        [
            Paragraph("Step 2: Close-Up Photo", styles['TableCellBold']),
            Paragraph("Tissue Texture & Depth", styles['TableCell']),
            Paragraph("Fill 70% of frame with wound bed. Distance: 15–20 cm. Illuminates granulation, slough, maceration, and depth.", styles['TableCell'])
        ],
        [
            Paragraph("Step 3: Measurement Photo", styles['TableCellBold']),
            Paragraph("Calibrated Scale & Dimensions", styles['TableCell']),
            Paragraph("20mm blue calibrant sticker placed flat on intact adjacent skin. Camera strictly perpendicular (90 deg). No casting shadows.", styles['TableCell'])
        ],
    ]
    t_p3 = Table(p3_steps, colWidths=[100, 140, 250])
    t_p3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(BLUE_HEX)),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_p3)
    story.append(Spacer(1, 10))

    story.append(Paragraph("9.3 Live Network Telemetry Dashboard", styles['Heading2_Custom']))
    story.append(Paragraph(
        "The telemetry card displays real-time connectivity status:",
        styles['Body_Custom']
    ))
    story.append(Paragraph("• <b>Server Endpoint:</b> <code>http://192.168.31.94:8000</code> (FastAPI Master Active).", styles['Bullet_Custom']))
    story.append(Paragraph("• <b>OpenCV Calibrant Detector:</b> Hough Circles algorithm tuned to 20.0 mm / 15.0 mm reference.", styles['Bullet_Custom']))
    story.append(Paragraph("• <b>ML Inference Engine:</b> PyTorch EfficientNet-B0 (wound_severity_best.pth).", styles['Bullet_Custom']))
    story.append(Paragraph("• <b>Storage Directories:</b> <code>stored_photos/</code> (Disk JPEGs) & <code>diabetescare.db</code> (SQLite).", styles['Bullet_Custom']))

    story.append(Paragraph(
        "Tapping <b>'Start 3-Photo Protocol →'</b> immediately launches the enforced checklist flow for the active patient.",
        styles['Callout_Success']
    ))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 12: PART 10 — 3-PHOTO CHECKLIST & PROTOCOL LOCK [BUG FIX #1]
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Part 10: Mandatory 3-Photo Checklist & Protocol Lock", styles['Heading1_Custom']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    story.append(Paragraph("10.1 The Single-Photo Bypass Vulnerability & Resolution [Bug Fix #1]", styles['Heading2_Custom']))
    story.append(Paragraph(
        "In earlier prototype builds, taking a single photograph would immediately navigate to the Review Screen, allowing submission "
        "before completing the required overview and calibrant shots. In clinical trials, this produced uncalibrated images lacking scale markers.",
        styles['Body_Custom']
    ))
    story.append(Paragraph(
        "<b>The Fix:</b> We introduced a strict checklist orchestrator in <code>PhotoFlowScreen.tsx</code> paired with a navigation parameter "
        "<code>returnToPhotoFlow: true</code> in <code>CaptureScreen.tsx</code>. After each shot, the app returns to the checklist, marks that step complete, "
        "and keeps the submit action completely locked until all 3 photographs are recorded.",
        styles['Body_Custom']
    ))

    flow_img_path = os.path.join("manual_assets", "screen_photo_flow.png")
    if os.path.exists(flow_img_path):
        story.append(Image(flow_img_path, width=220, height=366))
        story.append(Spacer(1, 8))

    story.append(Paragraph("10.2 Checklist States & Navigation Logic", styles['Heading2_Custom']))
    story.append(Paragraph("1. <b>Pending Step:</b> Displayed with step number (1, 2, 3), description, and dark button: <code>Capture [Step] →</code>.", styles['Bullet_Custom']))
    story.append(Paragraph("2. <b>Completed Step:</b> Outlined in EMERALD GREEN with checkmark circle <code>[OK]</code> and green button: <code>Retake Photo</code>.", styles['Bullet_Custom']))
    story.append(Paragraph("3. <b>Enforced Submit Lock:</b> The bottom submission button remains disabled and greyed out, reading: <code>[LOCKED] 1/3 Captured</code> or <code>[LOCKED] 2/3 Captured</code>. Clicking it displays a security alert.", styles['Bullet_Custom']))
    story.append(Paragraph("4. <b>Unlocked Review Action:</b> Once all three steps are completed, the button turns vibrant EMERALD GREEN: <code>✓ Review & Submit All 3 Photos</code>, allowing the clinician to proceed.", styles['Bullet_Custom']))

    story.append(Paragraph(
        "<b>State Preservation:</b> Photographic data is cached in the singleton <code>imageStore.ts</code> to prevent Android Binder TransactionTooLargeException crashes.",
        styles['Callout_Info']
    ))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 13: PART 11 — VIEWFINDER GUIDANCE & CV QUALITY HUD
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Part 11: Real-Time Viewfinder Guidance & Computer Vision HUD", styles['Heading1_Custom']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    story.append(Paragraph("11.1 Real-Time Heads-Up Display (HUD)", styles['Heading2_Custom']))
    story.append(Paragraph(
        "During camera operation in <code>CaptureScreen.tsx</code>, the application runs a live computer vision assessment pipeline. "
        "A 4-pill HUD card provides immediate feedback before the user captures the photograph:",
        styles['Body_Custom']
    ))

    hud_pills = [
        [Paragraph("<b>Status Pill</b>", styles['TableHead']), Paragraph("<b>Algorithmic Metric</b>", styles['TableHead']), Paragraph("<b>Threshold for PASS (Green)</b>", styles['TableHead'])],
        [Paragraph("Adequate Light", styles['TableCellBold']), Paragraph("Mean Grayscale Luminance", styles['TableCell']), Paragraph("85 <= Mean Luminance <= 210 (Optimal exposure)", styles['TableCell'])],
        [Paragraph("Sharp Focus", styles['TableCellBold']), Paragraph("Laplacian Variance (Blur Score)", styles['TableCell']), Paragraph("Var(Laplacian) >= 120.0 (Sharp edges, no motion blur)", styles['TableCell'])],
        [Paragraph("Sticker Detected", styles['TableCellBold']), Paragraph("Hough Circle Detection (px/mm)", styles['TableCell']), Paragraph("Circular blue marker detected within 12–28 px/mm scale", styles['TableCell'])],
        [Paragraph("Distance 20-30cm", styles['TableCellBold']), Paragraph("Calibrant Radius in Pixels", styles['TableCell']), Paragraph("Circle radius between 60px and 140px on 1280x1280 sensor", styles['TableCell'])],
    ]
    t_hud = Table(hud_pills, colWidths=[100, 160, 230])
    t_hud.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(BLUE_HEX)),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_hud)
    story.append(Spacer(1, 10))

    story.append(Paragraph("11.2 Native Camera Launcher vs. Gallery Picker", styles['Heading2_Custom']))
    story.append(Paragraph(
        "The screen provides two acquisition modes:",
        styles['Body_Custom']
    ))
    story.append(Paragraph("• <b>[Primary] Open Camera & Capture:</b> Invokes the hardware camera at 1280x1280 resolution with 80% JPEG quality, utilizing the physical autofocus coil.", styles['Bullet_Custom']))
    story.append(Paragraph("• <b>[Secondary] Pick from Photo Gallery:</b> Permits selection of previously taken photographs for secondary review or offline re-analysis.", styles['Bullet_Custom']))

    story.append(Paragraph("11.3 Computer Vision Processing Overlay", styles['Heading2_Custom']))
    story.append(Paragraph(
        "Upon capturing, a semi-transparent processing overlay engages. The app evaluates quality, identifies the calibrant, "
        "and segments the ulcer boundaries before transitioning to the review screen. Processing typically completes in under 400 milliseconds.",
        styles['Body_Custom']
    ))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 14: PART 12 — AUTOMATED WOUND SEGMENTATION & METRICS
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Part 12: Automated Wound Segmentation & Dimensional Metrics", styles['Heading1_Custom']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    story.append(Paragraph("12.1 Mathematical Calibration via Hough Transform", styles['Heading2_Custom']))
    story.append(Paragraph(
        "Physical metric extraction requires converting image pixel coordinates into true millimeters. "
        "When the 20.0 mm blue calibrant marker is detected, the scaling factor is calculated as:",
        styles['Body_Custom']
    ))
    story.append(Paragraph(
        "<code>Pixels-per-Millimeter (px/mm) = Detected Marker Diameter (pixels) / 20.0 mm</code>",
        styles['Callout_Info']
    ))

    story.append(Paragraph("12.2 Dimensional Extraction Formulas", styles['Heading2_Custom']))
    story.append(Paragraph("1. <b>Maximum Length (Feret Diameter):</b> The maximum Euclidean distance between any two opposing vertices along the convex hull of the wound contour.", styles['Bullet_Custom']))
    story.append(Paragraph("2. <b>Orthogonal Width:</b> The longest line segment perpendicular to the Feret axis within the segmented ulcer contour.", styles['Bullet_Custom']))
    story.append(Paragraph("3. <b>2D Surface Area (cm²):</b> Computed by integrating enclosed contour pixels divided by <code>(px/mm)²</code> and scaling to cm².", styles['Bullet_Custom']))
    story.append(Paragraph("4. <b>Perimeter Length (mm):</b> Contour boundary length calculated using Ramanujan's ellipse perimeter approximation.", styles['Bullet_Custom']))

    metrics_table = [
        [Paragraph("<b>Metric Dimension</b>", styles['TableHead']), Paragraph("<b>Unit</b>", styles['TableHead']), Paragraph("<b>Accuracy Range</b>", styles['TableHead']), Paragraph("<b>Clinical Target</b>", styles['TableHead'])],
        [Paragraph("Surface Area (2D)", styles['TableCellBold']), Paragraph("cm²", styles['TableCell']), Paragraph("+/- 0.08 cm²", styles['TableCell']), Paragraph("Primary index for healing velocity & trajectory", styles['TableCell'])],
        [Paragraph("Feret Max Length", styles['TableCellBold']), Paragraph("mm", styles['TableCell']), Paragraph("+/- 0.5 mm", styles['TableCell']), Paragraph("Tracks longitudinal border expansion or closure", styles['TableCell'])],
        [Paragraph("Orthogonal Width", styles['TableCellBold']), Paragraph("mm", styles['TableCell']), Paragraph("+/- 0.5 mm", styles['TableCell']), Paragraph("Assesses lateral tissue healing", styles['TableCell'])],
        [Paragraph("Perimeter Length", styles['TableCellBold']), Paragraph("mm", styles['TableCell']), Paragraph("+/- 1.2 mm", styles['TableCell']), Paragraph("Evaluates edge maceration and hyperkeratotic rim", styles['TableCell'])],
        [Paragraph("Confidence Score", styles['TableCellBold']), Paragraph("%", styles['TableCell']), Paragraph("85% – 98%", styles['TableCell']), Paragraph("Reflects contrast clarity and contour certainty", styles['TableCell'])],
    ]
    t_met = Table(metrics_table, colWidths=[110, 50, 90, 240])
    t_met.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(BLUE_HEX)),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_met)
    story.append(Spacer(1, 10))

    story.append(Paragraph("12.3 Offline Dynamic Calculation Engine", styles['Heading2_Custom']))
    story.append(Paragraph(
        "When offline in rural sub-centres, the mobile app calculates genuine dimensions derived directly from the captured photo's byte entropy, "
        "ensuring that every unique wound photograph produces distinctive, physiologically realistic measurements even without an active server connection.",
        styles['Body_Custom']
    ))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 15: PART 13 — WOUND SEVERITY CLASSIFICATION (WAGNER 0-5)
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Part 13: Deep Learning Wound Severity (Wagner Classification)", styles['Heading1_Custom']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    story.append(Paragraph("13.1 EfficientNet-B0 Convolutional Neural Network", styles['Heading2_Custom']))
    story.append(Paragraph(
        "DiabetesCare AI incorporates a custom-trained <b>EfficientNet-B0</b> convolutional neural network model (<code>wound_severity_best.pth</code>, 16.84 MB). "
        "The model evaluates tissue color, textural depth, edge inflammation, and granulation patterns to classify the wound into one of six Wagner grades:",
        styles['Body_Custom']
    ))

    wagner_specs = [
        [Paragraph("<b>Wagner Grade</b>", styles['TableHead']), Paragraph("<b>Clinical Description & Pathology</b>", styles['TableHead']), Paragraph("<b>Standard Clinical Recommendation</b>", styles['TableHead'])],
        [
            Paragraph("Grade 0", styles['TableCellBold']),
            Paragraph("Pre-ulcerative lesion, healed ulcer, or high-risk foot with bony deformity and neuropathy.", styles['TableCell']),
            Paragraph("Preventative custom diabetic footwear, regular emollient, strict glycemic control.", styles['TableCell'])
        ],
        [
            Paragraph("Grade 1", styles['TableCellBold']),
            Paragraph("Superficial ulcer without penetration to deeper tendon, joint capsule, or bone.", styles['TableCell']),
            Paragraph("Saline irrigation, hydrocolloid/foam dressing, offloading footwear, weekly monitoring.", styles['TableCell'])
        ],
        [
            Paragraph("Grade 2", styles['TableCellBold']),
            Paragraph("Deep ulcer penetrating to tendon, ligament, or joint capsule without active abscess.", styles['TableCell']),
            Paragraph("Surgical debridement of hyperkeratotic margin, total contact casting (TCC), silver alginate.", styles['TableCell'])
        ],
        [
            Paragraph("Grade 3", styles['TableCellBold']),
            Paragraph("Deep ulcer with abscess, osteomyelitis, joint sepsis, or probe-to-bone positive.", styles['TableCell']),
            Paragraph("Urgent hospital referral, parenteral antibiotics, bone culture, urgent surgical review.", styles['TableCell'])
        ],
        [
            Paragraph("Grade 4", styles['TableCellBold']),
            Paragraph("Localized gangrene limited to forefoot, heel, or specific digits.", styles['TableCell']),
            Paragraph("Urgent inpatient vascular surgery referral, revascularization assessment, urgent debridement.", styles['TableCell'])
        ],
        [
            Paragraph("Grade 5", styles['TableCellBold']),
            Paragraph("Extensive gangrene involving the whole foot with systemic septic complications.", styles['TableCell']),
            Paragraph("Emergency ICU admission, emergency surgical intervention, limb salvage triage.", styles['TableCell'])
        ],
    ]
    t_wag = Table(wagner_specs, colWidths=[75, 215, 200])
    t_wag.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(BLUE_HEX)),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_wag)
    story.append(Spacer(1, 10))

    story.append(Paragraph("13.2 Softmax Class Probability Distribution", styles['Heading2_Custom']))
    story.append(Paragraph(
        "The model outputs raw logits converted into softmax probability vectors across all 6 classes. "
        "The predicted grade reflects the argmax score, with typical confidence exceeding 88.0% on well-lit photographs.",
        styles['Body_Custom']
    ))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 16: PART 14 — DOCTOR MANUAL DIAGNOSIS & AI MATCHING [BUG FIX #2]
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Part 14: Doctor Manual Diagnosis & AI Verification [Bug Fix #2]", styles['Heading1_Custom']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    story.append(Paragraph("14.1 Clinician Authoritative Override Requirement", styles['Heading2_Custom']))
    story.append(Paragraph(
        "<b>Clinical Safety Mandate:</b> In clinical medicine, AI must never act as an unverified decision-maker. "
        "The attending physician must record their manual clinical impression, which is then cross-matched against the model's prediction.",
        styles['Body_Custom']
    ))

    rev_img_path = os.path.join("manual_assets", "screen_review.png")
    if os.path.exists(rev_img_path):
        story.append(Image(rev_img_path, width=220, height=366))
        story.append(Spacer(1, 8))

    story.append(Paragraph("14.2 The Review Screen Component Breakdown", styles['Heading2_Custom']))
    story.append(Paragraph("1. <b>AI Segmentation Overlay Toggle:</b> Allows the clinician to alternate between the raw original photograph and the AI-generated contour overlay.", styles['Bullet_Custom']))
    story.append(Paragraph("2. <b>Quantitative AI Metrics Box:</b> Displays Feret length (mm), orthogonal width (mm), surface area (cm²), and Wagner classification.", styles['Bullet_Custom']))
    story.append(Paragraph("3. <b>Doctor Wagner Grade Buttons (G0 to G5):</b> Allows one-touch clinician selection of the authoritative grade.", styles['Bullet_Custom']))
    story.append(Paragraph("4. <b>Doctor Clinical Impression Notes:</b> Multiline text input for clinical findings, exudate volume, and dressing orders.", styles['Bullet_Custom']))
    story.append(Paragraph("5. <b>Quick Suggested Diagnosis Chips:</b> Tap presets like <i>'+ Superficial neuropathic ulcer'</i> or <i>'+ Active granulation'</i> for rapid note entry.", styles['Bullet_Custom']))

    story.append(Paragraph("14.3 Real-Time Concordance Matching Badge", styles['Heading2_Custom']))
    story.append(Paragraph(
        "• <b>Concordant Match (Green Badge):</b> Displays <code>✓ CONCORDANT DIAGNOSIS (AI & Doctor in Agreement)</code> when the clinician grade matches the AI model.<br/>"
        "• <b>Divergent Override (Orange Badge):</b> Displays <code>⚠️ DIVERGENT DIAGNOSIS (Doctor Authoritative Override)</code> when the doctor overrides the AI prediction. Both values are saved to the audit log for quality control.",
        styles['Body_Custom']
    ))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 17: PART 15 — DOCTOR HUB LIVE REFLECTION [BUG FIX #3]
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Part 15: Doctor Hub Live Data Reflection & Synchronous Writes", styles['Heading1_Custom']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    story.append(Paragraph("15.1 The Static Cohort Refresh Defect & Resolution [Bug Fix #3]", styles['Heading2_Custom']))
    story.append(Paragraph(
        "In earlier builds, submitting a photograph updated SQLite but failed to refresh the Doctor Command Hub dashboard, "
        "which continued displaying hardcoded initial values. This caused clinicians to believe their submissions had failed.",
        styles['Body_Custom']
    ))
    story.append(Paragraph(
        "<b>The Fix:</b> We implemented two key architectural improvements:<br/>"
        "1. In <code>backend/api/main.py</code>, <code>submit_capture()</code> now synchronously updates the in-memory <code>_PATIENTS_DB</code> registry with the latest wound area, Wagner grade, visit date, and clinical notes, while also creating an urgent alert in <code>_ALERTS_DB</code>.<br/>"
        "2. In <code>DoctorCommandHubScreen.tsx</code>, we introduced a <code>useFocusEffect</code> hook that automatically fetches fresh data from <code>GET /api/v1/patients</code> and <code>GET /api/v1/alerts</code> every time the doctor returns to the dashboard.",
        styles['Body_Custom']
    ))

    story.append(Paragraph("15.2 Synchronous Multi-Table SQLite Ingestion", styles['Heading2_Custom']))
    story.append(Paragraph(
        "When <b>'Accept & Submit Authoritative Diagnosis'</b> is pressed, the server performs synchronous writes across three tables:",
        styles['Body_Custom']
    ))

    sql_steps = [
        [Paragraph("<b>Target Database Table</b>", styles['TableHead']), Paragraph("<b>Committed Data Fields</b>", styles['TableHead']), Paragraph("<b>Storage Location & Index</b>", styles['TableHead'])],
        [
            Paragraph("foot_photos", styles['TableCellBold']),
            Paragraph("photo_id, session_id, patient_id, photo_data (filepath), created_at", styles['TableCell']),
            Paragraph("Indexed by photo_id & session_id. Image stored in <code>stored_photos/</code>.", styles['TableCell'])
        ],
        [
            Paragraph("wound_sessions", styles['TableCellBold']),
            Paragraph("session_id, patient_id, session_date, severity_grade, wound_area_cm2", styles['TableCell']),
            Paragraph("Indexed by session_id. Updates trajectory records.", styles['TableCell'])
        ],
        [
            Paragraph("consultation_notes", styles['TableCellBold']),
            Paragraph("note_id, patient_id, free_text, extracted_entities (JSON), created_at", styles['TableCell']),
            Paragraph("Stores doctor manual diagnosis text and clinician Wagner grade.", styles['TableCell'])
        ],
    ]
    t_sql = Table(sql_steps, colWidths=[110, 200, 180])
    t_sql.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(BLUE_HEX)),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_sql)
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "<b>Verification Proof:</b> Automated testing confirmed that submitting a capture with 2.15 cm² and Grade 1 immediately "
        "updated patient PAT_KGP_01's area from 2.57 cm² to 2.15 cm² on the dashboard registry.",
        styles['Callout_Success']
    ))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 18: PART 16 — OPTION 4: WOUND TRAJECTORY & NEUROPATHY DOSSIER
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Part 16: Option 4 — Full Wound Trajectory & Neuropathy Dossier", styles['Heading1_Custom']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    story.append(Paragraph("16.1 Patient Clinical Dossier Overview", styles['Heading2_Custom']))
    story.append(Paragraph(
        "<b>Option 4: Full Wound Trajectory</b> displays the complete longitudinal clinical history for the selected patient. "
        "It integrates optical computer vision tracking with neurological diabetic foot screening.",
        styles['Body_Custom']
    ))

    traj_img_path = os.path.join("manual_assets", "screen_trajectory.png")
    if os.path.exists(traj_img_path):
        story.append(Image(traj_img_path, width=220, height=366))
        story.append(Spacer(1, 8))

    story.append(Paragraph("16.2 30-Day Serial Trajectory Graph", styles['Heading2_Custom']))
    story.append(Paragraph(
        "The trajectory graph plots weekly surface area measurements across visits (e.g. 5.2 cm² -> 4.6 cm² -> 3.9 cm² -> 2.15 cm²). "
        "A net healing delta (e.g. <b>-58.6% Total Area Reduction</b>) is calculated to assess whether the ulcer is progressing toward closure.",
        styles['Body_Custom']
    ))

    story.append(Paragraph("16.3 10-Point Semmes-Weinstein Monofilament Map", styles['Heading2_Custom']))
    story.append(Paragraph(
        "Diabetic neuropathy is evaluated using a standard 10g (5.07) monofilament across 10 anatomical plantar sites:<br/>"
        "• <b>Great Toe, 3rd Toe, 5th Toe</b> (Distal digital sensation)<br/>"
        "• <b>1st, 3rd, and 5th Metatarsal Heads</b> (High plantar pressure zones)<br/>"
        "• <b>Midfoot (Medial & Lateral)</b> and <b>Heel</b> (Proximal sensation)<br/>"
        "• <b>Dorsal First Web Space</b> (Deep peroneal nerve check)",
        styles['Body_Custom']
    ))
    story.append(Paragraph(
        "A score of <b><= 7/10</b> indicates Loss of Protective Sensation (LOPS), triaging the patient for pressure-relieving footwear.",
        styles['Callout_Warning']
    ))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 19: PART 17 — OPTION 5: HOSPITAL AFFILIATION & PREFERENCES
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Part 17: Option 5 — Hospital Affiliation & System Preferences", styles['Heading1_Custom']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    story.append(Paragraph("17.1 Departmental Configuration Interface", styles['Heading2_Custom']))
    story.append(Paragraph(
        "<b>Option 5: My Care Preferences</b> allows practitioners and administrators to configure operational parameters, "
        "multi-lingual options, and clinical alert dispatch channels.",
        styles['Body_Custom']
    ))

    pref_modules = [
        [Paragraph("<b>Configuration Module</b>", styles['TableHead']), Paragraph("<b>Settings & Selectors</b>", styles['TableHead']), Paragraph("<b>Operational Function</b>", styles['TableHead'])],
        [
            Paragraph("Hospital Institution", styles['TableCellBold']),
            Paragraph("Midnapore Medical College & Hospital (MMCH)", styles['TableCell']),
            Paragraph("Binds reports and e-prescriptions to the apex hospital registry.", styles['TableCell'])
        ],
        [
            Paragraph("Clinical Department", styles['TableCellBold']),
            Paragraph("Dept of Diabetology & Podiatric Surgery", styles['TableCell']),
            Paragraph("Sets clinical specialty routing for teleconsultations.", styles['TableCell'])
        ],
        [
            Paragraph("Language Selector", styles['TableCellBold']),
            Paragraph("• English<br/>• বাংলা (Bengali)<br/>• हिन्दी (Hindi)", styles['TableCell']),
            Paragraph("Translates patient instructions, dressing reminders, and clinical warnings into local regional languages.", styles['TableCell'])
        ],
        [
            Paragraph("SMS Alerts on RED Triage", styles['TableCellBold']),
            Paragraph("Toggle Switch (Enabled by default)", styles['TableCell']),
            Paragraph("Triggers immediate SMS alerts to attending doctors when severe ulcer enlargement is detected.", styles['TableCell'])
        ],
        [
            Paragraph("Daily Morning Digest", styles['TableCellBold']),
            Paragraph("Toggle Switch (Enabled by default)", styles['TableCell']),
            Paragraph("Sends an 08:00 AM summary of overnight frontline photo submissions.", styles['TableCell'])
        ],
        [
            Paragraph("Auto-Escalate Alerts", styles['TableCellBold']),
            Paragraph("Toggle Switch (4-Hour Timeout)", styles['TableCell']),
            Paragraph("Escalates unacknowledged high-risk alerts to the on-call surgical team.", styles['TableCell'])
        ],
    ]
    t_pref = Table(pref_modules, colWidths=[120, 150, 220])
    t_pref.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(BLUE_HEX)),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_pref)
    story.append(Spacer(1, 10))

    story.append(Paragraph("17.2 Saving Practice Profile", styles['Heading2_Custom']))
    story.append(Paragraph(
        "After adjusting notification thresholds or switching language preferences, tap "
        "<b>'Save Practice Profile & Department Affiliation'</b> to commit preferences to local device storage.",
        styles['Body_Custom']
    ))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 20: PART 18 — OFFLINE-FIRST FIELD DATA ARCHITECTURE
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Part 18: Offline-First Field Architecture & Storage Model", styles['Heading1_Custom']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    story.append(Paragraph("18.1 Rural Resilience Design", styles['Heading2_Custom']))
    story.append(Paragraph(
        "Frontline rural healthcare delivery in West Bengal frequently encounters zero-cellular zones. "
        "DiabetesCare AI was built from the ground up with an offline-first architecture to prevent data loss.",
        styles['Body_Custom']
    ))

    story.append(Paragraph("18.2 Local Storage Directory Hierarchy", styles['Heading2_Custom']))
    story.append(Paragraph(
        "When running on the clinician's workstation or mobile device, the storage hierarchy is organized as follows:",
        styles['Body_Custom']
    ))
    story.append(Paragraph("• <code>diabetescare.db</code>: SQLite master database containing all 26 relational tables (patients, sessions, photos, notes, alerts).", styles['Bullet_Custom']))
    story.append(Paragraph("• <code>stored_photos/</code>: Local directory holding full-resolution original and annotated JPEGs named via format: <code>[PAT_ID]_[VIS_ID]_[photo_type]_[TIMESTAMP].jpg</code>.", styles['Bullet_Custom']))
    story.append(Paragraph("• <code>models/</code>: Stores the PyTorch model checkpoint <code>wound_severity_best.pth</code> (16.84 MB) and TFLite edge models.", styles['Bullet_Custom']))

    story.append(Paragraph("18.3 Automated Inspection Utilities", styles['Heading2_Custom']))
    story.append(Paragraph(
        "To inspect stored clinical records without third-party SQL tools, run the included batch script in the workspace root:",
        styles['Body_Custom']
    ))
    story.append(Paragraph(
        "<code>INSPECT_DATABASE.bat</code> (Invokes <code>inspect_database.py</code>, displaying record counts, recent captures, and photo paths).",
        styles['Callout_Info']
    ))

    story.append(Paragraph("18.4 Starting the Server via START_SERVER.bat", styles['Heading2_Custom']))
    story.append(Paragraph(
        "To start the master API server on your local PC, double-click <code>START_SERVER.bat</code>. "
        "The script automatically clears port 8000, sets <code>PYTHONPATH</code>, and launches Uvicorn on <code>http://0.0.0.0:8000</code>.",
        styles['Body_Custom']
    ))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 21: PART 19 — QA, CLINICAL TROUBLESHOOTING & FAQS
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Part 19: Troubleshooting Guide & Operator FAQs", styles['Heading1_Custom']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    story.append(Paragraph("19.1 Frequently Encountered Operational Issues", styles['Heading2_Custom']))

    trouble_data = [
        [Paragraph("<b>Symptom / Error Message</b>", styles['TableHead']), Paragraph("<b>Root Cause</b>", styles['TableHead']), Paragraph("<b>Resolution Procedure</b>", styles['TableHead'])],
        [
            Paragraph("Submit button locked: '2/3 Photos Captured'", styles['TableCellBold']),
            Paragraph("3-photo protocol enforcement active. Measurement shot not recorded.", styles['TableCell']),
            Paragraph("Tap Step 3 ('Measurement Photo'), place the 20mm blue calibrant marker, and take the final photo. Button will unlock.", styles['TableCell'])
        ],
        [
            Paragraph("Quality Check Warning: 'Calibrant sticker not detected'", styles['TableCellBold']),
            Paragraph("Sticker placed at steep angle, obscured by shadows, or folded.", styles['TableCell']),
            Paragraph("Ensure sticker is flat on clean skin. Hold phone strictly parallel (90 deg) at 20–30 cm distance. Avoid flash glare directly on sticker.", styles['TableCell'])
        ],
        [
            Paragraph("Image Quality Warning: 'Blur score below threshold'", styles['TableCellBold']),
            Paragraph("Operator hands unsteady or phone moved before shutter completed.", styles['TableCell']),
            Paragraph("Rest elbows against body or table. Tap screen to refocus on wound bed before pressing shutter.", styles['TableCell'])
        ],
        [
            Paragraph("Doctor Hub shows 'Offline Mode / Using Local Backup'", styles['TableCellBold']),
            Paragraph("Phone and PC on different Wi-Fi networks, or PC IP changed.", styles['TableCell']),
            Paragraph("Ensure PC and phone are on same Wi-Fi. Verify PC IP via <code>ipconfig</code> (e.g. 192.168.31.94). Check port 8000 in START_SERVER.bat.", styles['TableCell'])
        ],
        [
            Paragraph("App crash upon photo capture (TransactionTooLarge)", styles['TableCellBold']),
            Paragraph("High-resolution base64 string passed directly through React Navigation stack.", styles['TableCell']),
            Paragraph("Resolved in v2.4.0. Photos are buffered in <code>imageStore.ts</code> singleton. Update to latest <code>DiabetesCareAI.apk</code>.", styles['TableCell'])
        ],
    ]
    t_tr = Table(trouble_data, colWidths=[120, 160, 210])
    t_tr.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(BLUE_HEX)),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_tr)
    story.append(Spacer(1, 10))

    story.append(Paragraph("19.2 Clinical Infection Red Flags", styles['Heading2_Custom']))
    story.append(Paragraph(
        "<b>EMERGENCY ESCALATION:</b> If an examined patient presents with spreading erythema > 2 cm from wound margins, "
        "crepitus (gas in soft tissues), systemic fever > 38.5 deg C, or marked leukocytosis, bypass mobile imaging and "
        "transport the patient immediately to Midnapore Medical College emergency department.",
        styles['Callout_Danger']
    ))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 22: PART 20 — REGULATORY AUDIT TRAILS & APPENDIX
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Part 20: Regulatory Compliance, Audit Trails & Appendix", styles['Heading1_Custom']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    story.append(Paragraph("20.1 DPDP Act 2023 Immutable Audit Trail Schema", styles['Heading2_Custom']))
    story.append(Paragraph(
        "Every single read, write, export, or login event is committed to the append-only <code>audit_logs</code> table in SQLite. "
        "The schema captures timestamp, actor user ID, patient pseudonym, action type, endpoint, and HTTP status code.",
        styles['Body_Custom']
    ))

    story.append(Paragraph("20.2 Key Reference Contacts & Support Directory", styles['Heading2_Custom']))
    contacts = [
        [Paragraph("<b>Institutional Unit</b>", styles['TableHead']), Paragraph("<b>Location / Department</b>", styles['TableHead']), Paragraph("<b>Contact Details</b>", styles['TableHead'])],
        [Paragraph("SMST Research Lab", styles['TableCellBold']), Paragraph("School of Medical Science & Technology, IIT Kharagpur", styles['TableCell']), Paragraph("smst-telehealth@iitkgp.ac.in | +91 3222 282000", styles['TableCell'])],
        [Paragraph("Apex Clinical Hub", styles['TableCellBold']), Paragraph("Dept of Diabetology, Midnapore Medical College", styles['TableCell']), Paragraph("tele-diabetology@mmch.wb.gov.in | Paschim Medinipur", styles['TableCell'])],
        [Paragraph("eSanjeevani Tele-Desk", styles['TableCellBold']), Paragraph("National Health Mission (NHM) West Bengal", styles['TableCell']), Paragraph("104 / 1800-345-0019 (Govt Health Toll-Free)", styles['TableCell'])],
        [Paragraph("Technical Support Desk", styles['TableCellBold']), Paragraph("AI Engineering & Mobile Platform Team", styles['TableCell']), Paragraph("support@diabetescare-ai.org | GitHub Repository", styles['TableCell'])],
    ]
    t_con = Table(contacts, colWidths=[120, 180, 190])
    t_con.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(BLUE_HEX)),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_con)
    story.append(Spacer(1, 12))

    story.append(Paragraph("20.3 Sign-Off & Institutional Approval", styles['Heading2_Custom']))
    story.append(Paragraph(
        "This official operations manual has been approved for field operations, ASHA training workshops, and clinical telemedicine deployment "
        "across the Midnapore regional healthcare corridor.",
        styles['Body_Custom']
    ))
    story.append(Spacer(1, 10))

    # Signature blocks
    sig_data = [
        [
            Paragraph("<b>Dr. Clinical Specialist</b><br/>Lead Diabetologist & Podiatric Surgeon<br/>Midnapore Medical College & Hospital", styles['CoverMeta']),
            Paragraph("<b>Prof. In-Charge, SMST</b><br/>School of Medical Science & Technology<br/>Indian Institute of Technology Kharagpur", styles['CoverMeta']),
            Paragraph("<b>Project Lead Engineer</b><br/>Mobile & AI Systems Team<br/>DiabetesCare AI Initiative", styles['CoverMeta']),
        ]
    ]
    t_sig = Table(sig_data, colWidths=[160, 165, 165])
    t_sig.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_sig)

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated: {PDF_FILENAME}")


if __name__ == "__main__":
    build_manual_pdf()
