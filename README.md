# 🩺 DiabetesCare AI v4.0 — Master Platform Repository (`SNST-Saugata`)

[![Vercel Deployment](https://img.shields.io/badge/Vercel-Live%20Production-success?style=for-the-badge&logo=vercel)](https://doctor-dashboard-mu.vercel.app/)
[![GitHub Mobile App](https://img.shields.io/badge/GitHub-Mobile--app--Updated-181717?style=for-the-badge&logo=github)](https://github.com/saugata-malakar/Mobile-app-Updated)
[![GitHub Master Repo](https://img.shields.io/badge/GitHub-SNST--Saugata-181717?style=for-the-badge&logo=github)](https://github.com/saugata-malakar/SNST-Saugata)
[![Android APK v4.0](https://img.shields.io/badge/Download%20APK-v4.0.0%20Signed-blue?style=for-the-badge&logo=android)](https://github.com/saugata-malakar/SNST-Saugata/raw/main/DiabetesCareAI.apk)
[![Play Store AAB](https://img.shields.io/badge/Play%20Store%20AAB-v4.0.0%20Ready-34A853?style=for-the-badge&logo=googleplay)](https://github.com/saugata-malakar/Mobile-app-Updated/raw/main/play_store_assets/DiabetesCareAI-v4.0.0.aab)
[![User Manual](https://img.shields.io/badge/User%20Manual-23%20Pages%20PDF-red?style=for-the-badge&logo=adobeacrobatreader)](https://github.com/saugata-malakar/SNST-Saugata/blob/main/DiabetesCare_AI_Official_User_Manual.pdf)

Master workspace for **DiabetesCare AI (v4.0.0)** developed with **IIT Kharagpur (SMST)** and **Midnapore Medical College & Hospital (MMCH)**.

---

## 🌐 Direct Links & Downloads

| Resource | Link | Details |
|---|---|---|
| 📲 **Android Release APK (v4.0.0)** | **[DiabetesCareAI.apk (28.27 MB)](https://github.com/saugata-malakar/SNST-Saugata/raw/main/DiabetesCareAI.apk)** | Signed Android release APK (`com.iitkgp.diabetescareai`, `versionCode 4`). |
| 🛍️ **Google Play Store App Bundle** | **[DiabetesCareAI-v4.0.0.aab (27.57 MB)](https://github.com/saugata-malakar/Mobile-app-Updated/raw/main/play_store_assets/DiabetesCareAI-v4.0.0.aab)** | Signed `.aab` release bundle + Play Console assets in `Mobile-app-Updated/play_store_assets/`. |
| 🚀 **Live Website & Admin Panel** | **[doctor-dashboard-mu.vercel.app](https://doctor-dashboard-mu.vercel.app/)** | Doctor, Field Collector (ASHA/ICDS/CHO), Moderator, and Admin web portals. |
| 🛡️ **Privacy Policy URL** | **[doctor-dashboard-mu.vercel.app/privacy-policy.html](https://doctor-dashboard-mu.vercel.app/privacy-policy.html)** | DPDP Act 2023 & Google Play compliant Privacy Policy. |
| 📑 **Official User Manual PDF** | **[DiabetesCare_AI_Official_User_Manual.pdf](https://github.com/saugata-malakar/SNST-Saugata/blob/main/DiabetesCare_AI_Official_User_Manual.pdf)** | Complete 23-page clinical operations manual. |
| 📦 **Mobile & Website Production Repo** | **[github.com/saugata-malakar/Mobile-app-Updated](https://github.com/saugata-malakar/Mobile-app-Updated)** | Production FastAPI backend, React Native mobile app, React/Vite website, and Play Store kit. |

---

## 🔑 4-Role + Patient Workflow, Admin Verification Gate & Seeded Accounts

All newly registered accounts (**Doctor**, **ASHA / ICDS / CHO**, **Moderator**, **Admin**, **Patient**) require **Admin verification (`✓ Verify & Approve`)** before they can sign in, across both the **Mobile App** and **Website**. Pre-seeded accounts support multi-identifier login (**Email, Phone, Username, or Worker ID + Password**):

* **Doctor (`doctor@demo.in` / `DOC_IITKGP_01` / `9831000001` · `doctor123`)**: Patient details + 3 photos (camera or system image upload) + optional medical reports + mandatory 1–2 line clinical note → AI quality check → `₹80` (+ `₹20` helper). Also validates Moderator-approved ASHA records (`₹30`).
* **ASHA / ICDS / CHO (`asha@demo.in` / `ASHA_WB_0042` / `9831000002` · `asha123`)**: Patient details + 3 photos (no diagnosis/medication) → AI quality check → Moderator review → Doctor validation → `₹50`.
* **Moderator (`moderator@demo.in` / `MOD_MMCH_01` / `9831000004` · `mod123`)**: Reviews ASHA/ICDS/CHO submissions (3 photos + vitals + AI score) → Approve (`₹20`) or Reject with reason.
* **Admin (`admin@hospital.in` / `ADMIN_MMCH_01` / `9831000005` · `admin123`)**: Full all-access Admin Panel — verify/approve or reject any pending new registration, switch directly into Doctor/Field/Moderator/Patient portals, inspect all submissions & photos, override decisions, and manage `₹` payouts.
* **Patient (`patient@demo.in` / `PAT_KGP_01` / `9831000007` · `patient123`)**: View longitudinal wound journey, prescriptions & follow-up status.

See [`Mobile-app-Updated/README.md`](Mobile-app-Updated/README.md) and [`Mobile-app-Updated/play_store_assets/PLAY_STORE_DEPLOYMENT_GUIDE.md`](Mobile-app-Updated/play_store_assets/PLAY_STORE_DEPLOYMENT_GUIDE.md) for full developer & Play Store publishing instructions.
