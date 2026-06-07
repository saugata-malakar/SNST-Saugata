"""
Multimodal AI Analysis API Router
Week 4 - Saugata Malakar

Combines wound photograph + clinical data (HbA1c, diabetes duration, BP)
using Gemini 1.5 Pro Vision for richer severity assessment.

Endpoints:
- POST /api/v1/multimodal/analyze - Single case analysis
- POST /api/v1/multimodal/analyze-batch - Batch analysis (up to 20 cases)
- GET /api/v1/multimodal/analysis/{analysis_id} - Retrieve stored analysis

Owner: Saugata Malakar
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from PIL import Image
import io
import logging
import uuid

from ml.multimodal.gemini_multimodal import (
    GeminiMultimodalAPI, 
    MultimodalAnalysisRequest, 
    MultimodalAnalysisResponse
)
from backend.utils.config import get_settings
from backend.database.models import MultimodalAnalysis, Patient, MonitoringSession
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/multimodal", tags=["multimodal"])


# Pydantic models for request/response

class MultimodalAnalyzeRequest(BaseModel):
    """Request for multimodal analysis"""
    patient_id: str = Field(..., description="Patient UUID")
    session_id: Optional[str] = Field(None, description="Monitoring session UUID")
    hba1c: float = Field(..., ge=4.0, le=15.0, description="HbA1c level (%) - range 4-15")
    diabetes_duration: int = Field(..., ge=0, le=60, description="Years with diabetes")
    systolic_bp: int = Field(..., ge=70, le=250, description="Systolic BP (mmHg)")
    diastolic_bp: int = Field(..., ge=40, le=150, description="Diastolic BP (mmHg)")
    age: Optional[int] = Field(None, ge=0, le=120, description="Patient age")
    gender: Optional[str] = Field(None, description="Patient gender")
    
    class Config:
        json_schema_extra = {
            "example": {
                "patient_id": "123e4567-e89b-12d3-a456-426614174000",
                "session_id": "223e4567-e89b-12d3-a456-426614174001",
                "hba1c": 9.2,
                "diabetes_duration": 12,
                "systolic_bp": 145,
                "diastolic_bp": 92,
                "age": 58,
                "gender": "male"
            }
        }


class MultimodalAnalyzeResponse(BaseModel):
    """Response from multimodal analysis"""
    analysis_id: str
    patient_id: str
    session_id: Optional[str]
    
    # Assessment results
    severity_grade: int
    severity_label: str
    confidence: float
    tissue_assessment: str
    infection_risk: str
    healing_prognosis: str
    
    # Clinical insights
    clinical_insights: List[str]
    risk_factors: List[str]
    immediate_actions: List[str]
    
    follow_up_days: int
    specialist_referral: bool
    
    timestamp: str
    model_name: str = "gemini-1.5-pro"
    
    class Config:
        json_schema_extra = {
            "example": {
                "analysis_id": "323e4567-e89b-12d3-a456-426614174002",
                "patient_id": "123e4567-e89b-12d3-a456-426614174000",
                "session_id": "223e4567-e89b-12d3-a456-426614174001",
                "severity_grade": 3,
                "severity_label": "Grade 3: Deep ulcer with abscess or osteomyelitis",
                "confidence": 0.87,
                "tissue_assessment": "Mixed granulation and necrotic tissue with signs of infection",
                "infection_risk": "high",
                "healing_prognosis": "poor",
                "clinical_insights": [
                    "HbA1c of 9.2% indicates poor glycemic control",
                    "Long diabetes duration of 12 years increases complication risk",
                    "Elevated blood pressure suggests vascular complications"
                ],
                "risk_factors": [
                    "Elevated HbA1c",
                    "Long-standing diabetes",
                    "Hypertension"
                ],
                "immediate_actions": [
                    "Start IV antibiotics immediately",
                    "Surgical debridement required",
                    "Optimize glycemic control"
                ],
                "follow_up_days": 3,
                "specialist_referral": True,
                "timestamp": "2024-01-15T10:30:00Z",
                "model_name": "gemini-1.5-pro"
            }
        }


class BatchAnalyzeRequest(BaseModel):
    """Request for batch analysis (multiple cases)"""
    cases: List[MultimodalAnalyzeRequest] = Field(..., max_length=20, description="Up to 20 cases")
    
    class Config:
        json_schema_extra = {
            "example": {
                "cases": [
                    {
                        "patient_id": "123e4567-e89b-12d3-a456-426614174000",
                        "hba1c": 9.2,
                        "diabetes_duration": 12,
                        "systolic_bp": 145,
                        "diastolic_bp": 92,
                        "age": 58,
                        "gender": "male"
                    }
                ]
            }
        }


# Dependency: Get Gemini API instance

def get_gemini_api():
    """Get Gemini multimodal API instance"""
    settings = get_settings()
    api = GeminiMultimodalAPI(api_key=settings.GEMINI_API_KEY)
    return api


# Dependency: Get database session (mock for now)

def get_db():
    """Get database session - to be implemented with proper DB connection"""
    # TODO: Implement proper database session
    # For now, return None - will implement database storage later
    return None


# Endpoints

@router.post("/analyze", response_model=MultimodalAnalyzeResponse)
async def analyze_multimodal(
    image: UploadFile = File(..., description="Wound photograph (JPEG/PNG)"),
    patient_id: str = Form(...),
    hba1c: float = Form(..., ge=4.0, le=15.0),
    diabetes_duration: int = Form(..., ge=0, le=60),
    systolic_bp: int = Form(..., ge=70, le=250),
    diastolic_bp: int = Form(..., ge=40, le=150),
    session_id: Optional[str] = Form(None),
    age: Optional[int] = Form(None),
    gender: Optional[str] = Form(None),
    gemini_api: GeminiMultimodalAPI = Depends(get_gemini_api),
    db: Session = Depends(get_db)
):
    """
    Perform multimodal analysis on wound photograph + clinical data.
    
    **Input:**
    - image: Wound photograph file
    - patient_id: Patient UUID
    - hba1c: HbA1c level (%)
    - diabetes_duration: Years with diabetes
    - systolic_bp: Systolic blood pressure (mmHg)
    - diastolic_bp: Diastolic blood pressure (mmHg)
    - session_id: Optional monitoring session UUID
    - age: Optional patient age
    - gender: Optional patient gender
    
    **Output:**
    - Comprehensive severity assessment
    - Tissue analysis
    - Infection risk
    - Healing prognosis
    - Clinical insights and recommendations
    
    **Week 4 - Saugata Malakar**
    """
    try:
        # Validate image format
        if image.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid image format: {image.content_type}. Use JPEG or PNG."
            )
        
        # Read and parse image
        image_bytes = await image.read()
        pil_image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if needed
        if pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")
        
        logger.info(f"Processing multimodal analysis for patient {patient_id}")
        
        # Build request
        request = MultimodalAnalysisRequest(
            image=pil_image,
            hba1c=hba1c,
            diabetes_duration=diabetes_duration,
            systolic_bp=systolic_bp,
            diastolic_bp=diastolic_bp,
            patient_id=patient_id,
            age=age,
            gender=gender
        )
        
        # Call Gemini API
        result = await gemini_api.analyze_multimodal(request)
        
        # Generate analysis ID
        analysis_id = str(uuid.uuid4())
        
        # TODO: Store in database
        # if db:
        #     db_analysis = MultimodalAnalysis(
        #         analysis_id=uuid.UUID(analysis_id),
        #         patient_id=uuid.UUID(patient_id),
        #         session_id=uuid.UUID(session_id) if session_id else None,
        #         hba1c=hba1c,
        #         diabetes_duration_years=diabetes_duration,
        #         systolic_bp=systolic_bp,
        #         diastolic_bp=diastolic_bp,
        #         severity_grade=result.severity_grade,
        #         severity_label=result.severity_label,
        #         confidence=result.confidence,
        #         tissue_assessment=result.tissue_assessment,
        #         infection_risk=result.infection_risk,
        #         healing_prognosis=result.healing_prognosis,
        #         clinical_insights=result.clinical_insights,
        #         risk_factors=result.risk_factors,
        #         immediate_actions=result.immediate_actions,
        #         follow_up_days=result.follow_up_days,
        #         specialist_referral=result.specialist_referral,
        #         raw_response=result.raw_response
        #     )
        #     db.add(db_analysis)
        #     db.commit()
        
        # Build response
        response = MultimodalAnalyzeResponse(
            analysis_id=analysis_id,
            patient_id=patient_id,
            session_id=session_id,
            severity_grade=result.severity_grade,
            severity_label=result.severity_label,
            confidence=result.confidence,
            tissue_assessment=result.tissue_assessment,
            infection_risk=result.infection_risk,
            healing_prognosis=result.healing_prognosis,
            clinical_insights=result.clinical_insights,
            risk_factors=result.risk_factors,
            immediate_actions=result.immediate_actions,
            follow_up_days=result.follow_up_days,
            specialist_referral=result.specialist_referral,
            timestamp=result.timestamp
        )
        
        logger.info(f"✓ Multimodal analysis complete: {analysis_id}")
        
        return response
        
    except Exception as e:
        logger.error(f"Multimodal analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/analysis/{analysis_id}")
async def get_analysis(
    analysis_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve stored multimodal analysis by ID.
    
    **Input:**
    - analysis_id: UUID of stored analysis
    
    **Output:**
    - Complete analysis result
    
    **Week 4 - Saugata Malakar**
    """
    # TODO: Implement database retrieval
    # For now, return not implemented
    raise HTTPException(
        status_code=501, 
        detail="Analysis retrieval not yet implemented. Database integration pending."
    )


@router.post("/analyze-batch")
async def analyze_batch(
    request: BatchAnalyzeRequest,
    gemini_api: GeminiMultimodalAPI = Depends(get_gemini_api)
):
    """
    Batch analysis for multiple cases (up to 20).
    
    **Note:** This endpoint requires images to be sent separately.
    For testing purposes, use the single analyze endpoint.
    
    **Input:**
    - cases: List of analysis requests (without images)
    
    **Output:**
    - List of analysis results
    
    **Week 4 - Saugata Malakar**
    """
    raise HTTPException(
        status_code=501,
        detail="Batch analysis endpoint not fully implemented. Use /analyze for single cases."
    )


@router.get("/health")
async def health_check(gemini_api: GeminiMultimodalAPI = Depends(get_gemini_api)):
    """
    Check if multimodal API is ready.
    
    **Output:**
    - status: "ready" or "mock_mode"
    - gemini_available: boolean
    - model_initialized: boolean
    """
    return {
        "status": "ready" if gemini_api.model else "mock_mode",
        "gemini_available": gemini_api.model is not None,
        "model_initialized": gemini_api.model is not None,
        "model_name": "gemini-1.5-pro" if gemini_api.model else "mock",
        "message": "Multimodal API is operational" if gemini_api.model else "Running in mock mode (GEMINI_API_KEY not set)"
    }
