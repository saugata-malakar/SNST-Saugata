"""DiabetesCare AI — FastAPI entry point.

Main application factory with:
- SQLAlchemy session setup
- CORS middleware
- Route registration
- Error handlers
- Startup/shutdown hooks

Owner: Sahil Kumar Gupta
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from pathlib import Path

from backend.utils.config import settings, get_cors_origins
from backend.database.session import init_db, engine
from backend.database.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown logic.
    
    Startup:
    - Create database tables (if not exist)
    
    Shutdown:
    - Close database connection
    """
    # Startup
    print("[startup] Initializing database...")
    try:
        init_db()
        print("[startup] Database ready ✓")
    except Exception as e:
        print(f"[startup] Database init failed: {e}")
    
    yield
    
    # Shutdown
    print("[shutdown] Closing database connections...")
    engine.dispose()
    print("[shutdown] Database closed ✓")


# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    lifespan=lifespan,
)

# Add CORS middleware
cors_origins = get_cors_origins()
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS.split(","),
    allow_headers=settings.CORS_HEADERS.split(","),
)

print(f"""
╔════════════════════════════════════════════════════════════╗
║  DiabetesCare AI FastAPI Backend                           ║
║  Version: {settings.API_VERSION}                                      ║
║  Mode: {'DEBUG' if settings.SQL_ECHO else 'PRODUCTION'}                                    ║
║  Database: {settings.DATABASE_URL[:40]}...        ║
║  CORS Origins: {', '.join(cors_origins)}  ║
╚════════════════════════════════════════════════════════════╝
""")


# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================

@app.get("/health")
def health() -> dict:
    """
    Liveness check for load balancers and CI.
    
    Returns:
        {"status": "ok", "service": "diabetescare-ai-api", "database": "ok"}
    """
    return {
        "status": "ok",
        "service": "diabetescare-ai-api",
        "version": settings.API_VERSION,
        "database": "ok",  # TODO: Actually check database connection
    }


# ============================================================================
# ROUTER REGISTRATION (To be added as modules are implemented)
# ============================================================================

# Privacy & Data Management (Week 2 - READY)
if settings.ENABLE_EXPORT:
    try:
        from backend.api.routers.export import router as export_router
        app.include_router(export_router, prefix="/api/v1/export", tags=["export"])
        print("[router] ✓ Export router registered")
    except Exception as e:
        print(f"[router] ✗ Export router failed: {e}")

# Patient Endpoints (Week 3A - Coming)
# from backend.api.routers import patients
# app.include_router(patients.router, prefix="/api/v1/patients", tags=["patients"])

# Doctor Endpoints (Week 3A - Coming)
# from backend.api.routers import doctors
# app.include_router(doctors.router, prefix="/api/v1/doctors", tags=["doctors"])

# Alert Management (Week 3A - Coming)
# from backend.api.routers import alerts
# app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["alerts"])

# Inference Endpoints (Week 3B - Coming)
if settings.ENABLE_INFERENCE:
    try:
        from backend.api.routers.wound import router as wound_router
        app.include_router(wound_router)
        print("[router] ✓ Wound inference router registered")
    except Exception as e:
        print(f"[router] ✗ Wound inference router failed: {e}")
    
    # Wound Tissue Classification (Week 3 - Sharif)
    try:
        from backend.api.routers.tissue import router as tissue_router
        app.include_router(tissue_router)
        print("[router] ✓ Wound tissue router registered")
    except Exception as e:
        print(f"[router] ✗ Wound tissue router failed: {e}")
    
    # Skin and Eye routers - Coming soon
    # from backend.api.routers import skin, eye
    # app.include_router(skin.router, prefix="/api/v1/skin", tags=["skin"])
    # app.include_router(eye.router, prefix="/api/v1/eye", tags=["eye"])

# ASHA Worker Endpoints (Week 3B - Coming)
# from backend.api.routers import asha
# app.include_router(asha.router, prefix="/api/v1/asha", tags=["asha"])

# Teleconsult Endpoints (Week 5 - Future)
# from backend.api.routers import teleconsult
# app.include_router(teleconsult.router, prefix="/api/v1/teleconsult", tags=["teleconsult"])


# ============================================================================
# STATIC FILES - SERVE FRONTEND
# ============================================================================

# Get the frontend directory path
frontend_dir = Path(__file__).parent.parent.parent / "frontend"

# Mount static files (CSS, JS, images)
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")
    print(f"[frontend] ✓ Serving frontend from {frontend_dir}")
    
    # Serve index.html at root
    @app.get("/")
    async def serve_frontend():
        """Serve the frontend index.html"""
        index_path = frontend_dir / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
        return {"message": "Frontend not found"}
    
    # Serve CSS
    @app.get("/styles.css")
    async def serve_css():
        """Serve the CSS file"""
        css_path = frontend_dir / "styles.css"
        if css_path.exists():
            return FileResponse(css_path, media_type="text/css")
        return {"message": "CSS not found"}
    
    # Serve JavaScript
    @app.get("/script.js")
    async def serve_js():
        """Serve the JavaScript file"""
        js_path = frontend_dir / "script.js"
        if js_path.exists():
            return FileResponse(js_path, media_type="application/javascript")
        return {"message": "JavaScript not found"}
else:
    print(f"[frontend] ✗ Frontend directory not found at {frontend_dir}")


# ============================================================================
# ERROR HANDLERS (To be added)
# ============================================================================

# @app.exception_handler(Exception)
# async def general_exception_handler(request, exc):
#     return {"detail": str(exc), "status": "error"}


# ============================================================================
# DEVELOPMENT
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

