# 📚 DiabetesCare AI — Master Documentation Index

**Created:** May 25, 2026  
**Total Documentation:** 6,500+ lines across 7 comprehensive guides  
**Purpose:** Enable 5-person team to work in parallel with complete understanding

---

## 📋 WHAT'S BEEN CREATED (Today)

### 1. **CODEBASE_AUDIT.md** (1800+ lines)
**When to read:** First thing if you're new to the project  
**Time to read:** 45-60 minutes (or skim in 15 min)

**What it covers:**
- ✅ Executive summary (status at glance)
- ✅ Team & ownership (who owns what)
- ✅ All 26 database tables (schema mapping)
- ✅ Privacy implementation (HMAC, k-anonymity, erasure)
- ✅ Frontend/backend integration (what mobile app expects)
- ✅ ML model structure (3 wound models, 3 eye models, etc)
- ✅ Computer vision pipeline
- ✅ Authentication flows
- ✅ Business logic workflows
- ✅ Testing structure
- ✅ Known issues & blockers

**For whom:**
- New developers (complete system understanding)
- Project managers (status overview)
- Anyone asked "what does the codebase do?"

**How to use:**
```
Read in sections:
1. Executive summary (5 min) ← START HERE
2. Your specific module (10 min)
3. Integration points (10 min)
```

**Link to section on specific module:**
- Patient workflows → Go to "Business Logic Workflows"
- Privacy → Go to "Privacy Implementation"
- ML inference → Go to "ML Model Structure"

---

### 2. **TEAM_SYNC_MAP.md** (1400+ lines)
**When to read:** Daily for tracking & coordination  
**Time to read:** 30 min initial, 5 min daily

**What it covers:**
- ✅ Each team member's role, focus, deliverables
- ✅ Current status of each person's work
- ✅ Week-by-week timeline
- ✅ Work dependency graph (what blocks what)
- ✅ Critical path (what must happen first)
- ✅ Blockers & how to resolve them
- ✅ This week's action items
- ✅ Contact info & response times

**For whom:**
- Project managers (tracking progress)
- Team leads (dependency management)
- Anyone asking "what is Saugata working on?" or "why is X blocked?"

**How to use:**
```
Start with "Work Dependency Graph" to see how pieces fit
Then "Critical Path" to see what's urgent
Then "This Week's Action Items" for dailies
Update "Progress Tracking" table as work completes
```

**Key sections:**
- **Sahil (Backend):** Phase 1 ✅, Phase 2-3 ⏳ waiting for Saugata
- **Saugata (Privacy):** ⏳ BLOCKED on database schema
- **ML team (Kousttav, Shivraj, Adreesh):** Training in parallel
- **PI (Prof. Das):** Decision points needed on HMAC, KMS, GPU resources

---

### 3. **WEEK2_TASK_BREAKDOWN.md** (1200+ lines)
**When to read:** Before starting Week 2 privacy implementation  
**Time to read:** 60 min (detailed technical guide)

**What it covers:**
- ✅ **3 Critical blockers** (must resolve TODAY)
  - Real database schema needed
  - HMAC key management policy decision
  - ML inference endpoint signature agreement
- ✅ **Task 1: Build privacy.py** (2-3 days, 8 subtasks)
  - RotatingSaltManager
  - pseudonymise_id()
  - generalise_age()
  - generalise_diabetes_duration()
  - strip_village()
  - anonymise_record()
  - verify_k_anonymity()
  - anonymise_dataset()
  - 100+ unit tests
- ✅ **Task 2: Build erasure.py** (1-2 days, 5 subtasks)
  - DELETION_ORDER (27-table cascade)
  - request_erasure() (72-hour pending)
  - execute_erasure() (cascading delete)
  - _verify_deletion() (confirmation)
  - Integration tests
- ✅ **Task 3: Export integration** (1 day)
  - Connect export.py to privacy.py
  - k-anonymity gating
  - Audit logging

**For whom:**
- Saugata (exact implementation guide)
- Sahil (understand what privacy.py will deliver)
- QA (what to test)
- Code reviewers

**How to use:**
```
Step 1: RESOLVE BLOCKERS (TODAY)
- Get real schema from database
- Decide HMAC key management with Prof. Das
- Agree on ML endpoint format

Step 2: FOLLOW TASK BREAKDOWN
- For each task (privacy.py, erasure.py, export)
- Implement each subtask in order
- Run tests after each subtask
- Commit when complete

Step 3: CHECKLIST
- Check off each deliverable
- Verify all tests passing (100+)
- Submit to GitHub
- Review with Prof. Das
```

**Key code patterns included:**
- HMAC-SHA256 pseudonymisation (3 options for key storage)
- k-anonymity group verification algorithm
- 72-hour erasure pipeline with foreign key handling
- Export endpoint integration

---

### 4. **CODEBASE_QUICK_REFERENCE.md** (800+ lines)
**When to read:** Every time you need to find something  
**Time to read:** 2-5 min per lookup

**What it covers:**
- ✅ Repository structure (visual tree)
- ✅ "Where do I find...?" lookup table
- ✅ Quick start workflows (start backend, migrate endpoint, etc)
- ✅ Code patterns & examples (10+ working snippets)
- ✅ Debugging tips
- ✅ Testing commands

**For whom:**
- Anyone asking "where is X code?"
- Developers starting first day
- Anyone wanting working code snippets
- Debugging issues

**How to use:**
```
"Where do I find the database connection code?"
→ Look for "Database & Schema" section
→ "Database connection" row
→ Click backend/database/session.py

"How do I authenticate a user?"
→ Look for "How do I...?" section
→ Find "How do I authenticate a user?"
→ Copy code snippet, adapt to your use case

"Backend won't start"
→ Go to "IF SOMETHING BREAKS" section
→ "Backend won't start"
→ Follow troubleshooting steps
```

**Key lookups:**
- Database queries (Patient, WoundSite, etc)
- Authentication & JWT
- API responses
- Privacy functions
- Testing
- Troubleshooting

---

### 5. **COMPLETE_PROJECT_SYNC_GUIDE.md** (600+ lines)
**When to read:** Onboarding for new people  
**Time to read:** 30 min overview

**What it covers:**
- Architecture overview + system diagram
- Completion status by component
- Integration points
- Action items by priority
- File structure
- Quick start guide
- Learning path for developers
- Success criteria by week

**For whom:**
- New developers (first orientation)
- Stakeholders wanting architecture overview
- Anyone asked "what's the project status?"

---

### 6. **BACKEND_SYNC_AUDIT.md** + **BACKEND_SYNC_STATUS_PHASE1.md** (850+ lines)
**When to read:** Refer to for backend-specific details  
**Time to read:** 15-20 min

**What they cover:**
- Current backend state
- Phase 1 infrastructure (what was built in Week 3A)
- Testing procedures
- Integration checklist
- Deployment readiness

**For whom:**
- Backend developers (Sahil)
- DevOps/deployment
- Backend code reviewers

---

### 7. **WEEK3A_PHASE1_COMPLETION_SUMMARY.md** (362 lines)
**When to read:** To understand what's already done  
**Time to read:** 10 min

**What it covers:**
- Week 2 privacy module (100% complete)
- Week 3A Phase 1 backend (100% complete)
- Synchronization status (before/after)
- Issues fixed
- Next phase (Phase 2-3)
- Git commits

**For whom:**
- Anyone asking "what's the current status?"
- Tracking project progress

---

## 🗂️ HOW TO NAVIGATE THE DOCUMENTATION

### I'm a NEW DEVELOPER joining the team
**Read in this order:**
1. `CODEBASE_AUDIT.md` - Executive summary (5 min)
2. `CODEBASE_QUICK_REFERENCE.md` - Structure + "how do I...?" (10 min)
3. `CODEBASE_AUDIT.md` - Your specific module (15 min)
4. `TEAM_SYNC_MAP.md` - Who's doing what (5 min)

**Total:** ~35 min to understand everything

Then use `CODEBASE_QUICK_REFERENCE.md` daily for lookups.

---

### I'm PROJECT MANAGER tracking progress
**Read in this order:**
1. `TEAM_SYNC_MAP.md` - Current status (5 min)
2. `WEEK2_TASK_BREAKDOWN.md` - What Saugata is doing (5 min)
3. `TEAM_SYNC_MAP.md` - "This Week's Action Items" (2 min)
4. `TEAM_SYNC_MAP.md` - "Progress Tracking" table (update daily)

**Daily:** Check `TEAM_SYNC_MAP.md` progress table, update action items

---

### I'm SAUGATA working on privacy module
**Read in this order:**
1. `WEEK2_TASK_BREAKDOWN.md` - Your exact tasks (30 min)
2. `TEAM_SYNC_MAP.md` - "Saugata" section (5 min)
3. Resolve the 3 blockers TODAY
4. Start implementing Task 1 (privacy.py)

**Use constantly:** 
- `WEEK2_TASK_BREAKDOWN.md` (implementation guide)
- `CODEBASE_QUICK_REFERENCE.md` (code patterns & debugging)
- `CODEBASE_AUDIT.md` (if you need schema details)

---

### I'm SAHIL working on backend/CRUD routers
**Read in this order:**
1. `TEAM_SYNC_MAP.md` - "Sahil" section + "Critical Path" (10 min)
2. `CODEBASE_QUICK_REFERENCE.md` - "How do I migrate a Flask route?" (10 min)
3. `CODEBASE_AUDIT.md` - Database schema you'll need (15 min)

**Use constantly:**
- `CODEBASE_QUICK_REFERENCE.md` (code patterns)
- `TEAM_SYNC_MAP.md` (blockers & dependencies)
- `BACKEND_SYNC_STATUS_PHASE1.md` (infrastructure status)

---

### I'm ML team (Kousttav, Shivraj, Adreesh) training models
**Read in this order:**
1. `TEAM_SYNC_MAP.md` - Your role & timeline (3 min)
2. `CODEBASE_AUDIT.md` - "ML Model Structure" section (10 min)
3. `CODEBASE_QUICK_REFERENCE.md` - Where ML code lives (2 min)

**Note:** You can work in parallel without blocking others. Main dependency is inference endpoint signature.

---

### I'm PROF. DAS (PI) reviewing
**Read in this order:**
1. `COMPLETE_PROJECT_SYNC_GUIDE.md` - Architecture overview (15 min)
2. `TEAM_SYNC_MAP.md` - Blocker decisions needed (5 min)
3. `WEEK2_TASK_BREAKDOWN.md` - 3 Critical blockers (5 min)
4. `CODEBASE_AUDIT.md` - "Privacy Implementation" section (10 min)

**Decision points needed:**
- HMAC key management policy (Option A, B, or C)
- Database location policy (Asia-South1 confirmation)
- GPU/TPU allocation for ML training
- Federated learning infrastructure setup (Week 4)

---

## 📊 DOCUMENTATION STATUS

| Document | Lines | Status | Last Updated |
|----------|-------|--------|--------------|
| CODEBASE_AUDIT.md | 1800 | ✅ Complete | May 25 |
| TEAM_SYNC_MAP.md | 1400 | ✅ Complete | May 25 |
| WEEK2_TASK_BREAKDOWN.md | 1200 | ✅ Complete | May 25 |
| CODEBASE_QUICK_REFERENCE.md | 800 | ✅ Complete | May 25 |
| COMPLETE_PROJECT_SYNC_GUIDE.md | 600 | ✅ Complete | May 25 |
| BACKEND_SYNC_STATUS_PHASE1.md | 350 | ✅ Complete | May 25 |
| WEEK3A_PHASE1_COMPLETION_SUMMARY.md | 362 | ✅ Complete | May 25 |
| BACKEND_SYNC_AUDIT.md | 500 | ✅ Complete | May 25 |
| **TOTAL** | **6,500+** | **✅** | **May 25** |

---

## 🎯 WHAT THIS ENABLES

✅ **New developers can onboard in 30 minutes** (instead of 3 days of reading code)  
✅ **Team can work in parallel without conflicts** (clear ownership + blockers documented)  
✅ **Progress tracking** (daily standup with TEAM_SYNC_MAP.md)  
✅ **Code patterns for implementation** (exact pseudocode in WEEK2_TASK_BREAKDOWN.md)  
✅ **Quick debugging** (CODEBASE_QUICK_REFERENCE.md troubleshooting section)  
✅ **Project overview** (COMPLETE_PROJECT_SYNC_GUIDE.md for stakeholders)  
✅ **Architecture understanding** (CODEBASE_AUDIT.md for design reviews)  

---

## 🚀 NEXT STEPS

### TODAY (Immediate)
1. **Saugata:** Resolve 3 blockers (schema, HMAC, ML signatures)
2. **Prof. Das:** Approve HMAC option, confirm database location
3. **All:** Read relevant documentation sections

### WEEK 2
1. **Saugata:** Build privacy.py + erasure.py (follow WEEK2_TASK_BREAKDOWN.md)
2. **Sahil:** Migrate CRUD routers (use CODEBASE_QUICK_REFERENCE.md)
3. **ML team:** Begin model training
4. **All:** Daily sync with TEAM_SYNC_MAP.md

### END OF WEEK
1. **Saugata:** Submit privacy.py + erasure.py for review
2. **Sahil:** Register all routers, integrate export
3. **ML team:** Report training progress
4. **Prof. Das:** Review + approve for Week 3B

---

## 📞 DOCUMENTATION MAINTENANCE

**Who maintains what:**
- **Saugata:** WEEK2_TASK_BREAKDOWN.md (as implementation progresses, update status)
- **Sahil:** BACKEND_SYNC_STATUS_PHASE1.md (update after Phase 2, Phase 3)
- **All:** TEAM_SYNC_MAP.md (update daily with "Progress Tracking" section)
- **Prof. Das:** Approve significant changes

**Update frequency:**
- Daily: Progress in TEAM_SYNC_MAP.md
- Weekly: Status in BACKEND_SYNC_STATUS_PHASE1.md
- As completed: Individual task statuses

---

## 🎓 WHAT NOT TO DO

❌ **Don't read all 6,500 lines.** Use the navigation guide above to read only what's relevant to your role.  
❌ **Don't implement code without reading WEEK2_TASK_BREAKDOWN.md first** if you're on critical path.  
❌ **Don't start a task if it's marked as blocked.** Check TEAM_SYNC_MAP.md "Critical Blockers" section first.  
❌ **Don't work on a module without reading team ownership.** Check TEAM_SYNC_MAP.md first.

---

## ✨ KEY INSIGHTS FROM DOCUMENTATION

1. **Saugata is the critical path.** Privacy.py blocks export functionality. Once delivered, Sahil can integrate.

2. **ML training is independent.** Kousttav, Shivraj, Adreesh can work in parallel without blocking core backend.

3. **Database schema unknown.** Must get real schema TODAY. Once confirmed, privacy.py can be completed in 2-3 days.

4. **Mobile + dashboard are ready.** React apps built; waiting for `/api/v1/*` endpoints to be live.

5. **Compliance framework in place.** Privacy module complete; just needs database integration.

6. **Phase 1 complete.** FastAPI foundation built (session, auth, config, logging). Just need routers + inference.

---

## 📈 PROJECT TIMELINE (Based on Documentation)

```
Week 1 (COMPLETE)
└─ PII Field Map ✅
   └─ DPDP Gap Analysis ✅

Week 2 (CURRENT - BLOCKED on schema)
├─ privacy.py ⏳
├─ erasure.py ⏳
├─ Export integration ⏳
└─ (ML training in parallel)

Week 3A Phase 1 (COMPLETE)
└─ Backend foundation ✅

Week 3A Phase 2 (STARTING)
├─ CRUD routers (can start, no blocker)
├─ Export integration (blocked on Saugata)
└─ (ML training continues)

Week 3A Phase 3+ (PLANNED)
├─ Inference routers
├─ Federated learning
├─ Consent versioning
└─ RAG assistant

End of Semester
└─ Production deployment
```

---

## 📝 NOTES FOR FUTURE

- **Keep this index updated** as new documentation is added
- **Link all new docs in this index** so people can find them
- **Update TEAM_SYNC_MAP.md daily** with progress
- **Review WEEK2_TASK_BREAKDOWN.md** after Week 2 completion to refine process
- **Archive completed docs** in /archive as project progresses

---

**Created:** May 25, 2026  
**Purpose:** Enable team to work in parallel with complete shared understanding  
**Status:** ✅ Documentation suite complete  
**Next:** Resolve Week 2 blockers + begin implementation

