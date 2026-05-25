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
from contextlib import asynccontextmanager

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
    print("[router] Inference routers (wound, skin, eye) - Coming in Week 3B")
    # from backend.api.routers import wound, skin, eye
    # app.include_router(wound.router, prefix="/api/v1/wound", tags=["wound"])
    # app.include_router(skin.router, prefix="/api/v1/skin", tags=["skin"])
    # app.include_router(eye.router, prefix="/api/v1/eye", tags=["eye"])

# ASHA Worker Endpoints (Week 3B - Coming)
# from backend.api.routers import asha
# app.include_router(asha.router, prefix="/api/v1/asha", tags=["asha"])

# Teleconsult Endpoints (Week 5 - Future)
# from backend.api.routers import teleconsult
# app.include_router(teleconsult.router, prefix="/api/v1/teleconsult", tags=["teleconsult"])


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
