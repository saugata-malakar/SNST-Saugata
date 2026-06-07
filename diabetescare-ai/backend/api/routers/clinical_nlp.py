"""
Clinical NLP API Router
Week 4 - Saugata Malakar

Extracts structured entities from doctor's free-text consultation notes using spaCy.

Entities extracted:
- wound_location: Where the wound is located
- infection_sign: Signs of infection observed
- treatment_recommendation: Recommended treatments

Endpoints:
- POST /api/v1/nlp/extract - Extract entities from single note
- POST /api/v1/nlp/extract-batch - Batch extraction from multiple notes
- GET /api/v1/nlp/note/{note_id} - Retrieve stored note with NLP output

Owner: Saugata Malakar
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging
import uuid

from ml.clinical_nlp.clinical_nlp_pipeline import ClinicalNLPPipeline
from backend.database.models import ClinicalNote, Patient, MonitoringSession
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/nlp", tags=["clinical_nlp"])


# Pydantic models for request/response

class NLPExtractRequest(BaseModel):
    """Request for NLP entity extraction"""
    note_text: str = Field(..., min_length=10, max_length=10000, description="Clinical note text")
    patient_id: Optional[str] = Field(None, description="Patient UUID")
    session_id: Optional[str] = Field(None, description="Monitoring session UUID")
    doctor_id: Optional[str] = Field(None, description="Doctor UUID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "note_text": """Patient presents with ulcer on left foot, plantar surface. 
Signs of cellulitis with purulent discharge and foul odor noted.
Erythema extending 3cm beyond wound margins. Patient is febrile.

Recommendations:
- Start IV antibiotics immediately
- Surgical debridement of necrotic tissue
- Daily dressing changes with silver foam dressing
- Offloading with cast boot
- Refer to vascular surgery for assessment
- X-ray foot to rule out osteomyelitis""",
                "patient_id": "123e4567-e89b-12d3-a456-426614174000",
                "session_id": "223e4567-e89b-12d3-a456-426614174001",
                "doctor_id": "323e4567-e89b-12d3-a456-426614174002"
            }
        }


class NLPExtractResponse(BaseModel):
    """Response from NLP extraction"""
    note_id: str
    patient_id: Optional[str]
    session_id: Optional[str]
    doctor_id: Optional[str]
    
    # Original text
    original_text: str
    
    # Extracted entities
    wound_locations: List[str]
    infection_signs: List[str]
    treatment_recommendations: List[str]
    
    # Metadata
    entity_count: Dict[str, int]
    extracted_at: str
    nlp_model_version: str = "en_core_web_sm"
    
    class Config:
        json_schema_extra = {
            "example": {
                "note_id": "423e4567-e89b-12d3-a456-426614174003",
                "patient_id": "123e4567-e89b-12d3-a456-426614174000",
                "session_id": "223e4567-e89b-12d3-a456-426614174001",
                "doctor_id": "323e4567-e89b-12d3-a456-426614174002",
                "original_text": "Patient presents with ulcer on left foot...",
                "wound_locations": [
                    "left foot",
                    "plantar surface"
                ],
                "infection_signs": [
                    "cellulitis",
                    "purulent discharge",
                    "foul odor",
                    "fever"
                ],
                "treatment_recommendations": [
                    "IV antibiotics",
                    "Surgical debridement",
                    "daily dressing changes",
                    "cast boot",
                    "vascular surgery consult",
                    "X-ray foot"
                ],
                "entity_count": {
                    "wound_locations": 2,
                    "infection_signs": 4,
                    "treatment_recommendations": 6
                },
                "extracted_at": "2024-01-15T10:30:00Z",
                "nlp_model_version": "en_core_web_sm"
            }
        }


class BatchNLPRequest(BaseModel):
    """Request for batch NLP extraction"""
    notes: List[NLPExtractRequest] = Field(..., max_length=50, description="Up to 50 notes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "notes": [
                    {
                        "note_text": "Patient presents with ulcer on left foot...",
                        "patient_id": "123e4567-e89b-12d3-a456-426614174000"
                    }
                ]
            }
        }


class BatchNLPResponse(BaseModel):
    """Response from batch NLP extraction"""
    total_notes: int
    successful: int
    failed: int
    results: List[NLPExtractResponse]


# Dependency: Get NLP pipeline instance

_nlp_pipeline = None

def get_nlp_pipeline():
    """Get or create NLP pipeline instance (singleton)"""
    global _nlp_pipeline
    if _nlp_pipeline is None:
        logger.info("Initializing Clinical NLP pipeline...")
        _nlp_pipeline = ClinicalNLPPipeline()
        logger.info("✓ Clinical NLP pipeline ready")
    return _nlp_pipeline


# Dependency: Get database session (mock for now)

def get_db():
    """Get database session - to be implemented with proper DB connection"""
    # TODO: Implement proper database session
    # For now, return None - will implement database storage later
    return None


# Endpoints

@router.post("/extract", response_model=NLPExtractResponse)
async def extract_entities(
    request: NLPExtractRequest,
    nlp: ClinicalNLPPipeline = Depends(get_nlp_pipeline),
    db: Session = Depends(get_db)
):
    """
    Extract structured entities from clinical note.
    
    **Input:**
    - note_text: Free-text clinical note (10-10,000 characters)
    - patient_id: Optional patient UUID
    - session_id: Optional monitoring session UUID
    - doctor_id: Optional doctor UUID
    
    **Output:**
    - Extracted entities:
      - wound_location: Where the wound is located
      - infection_sign: Signs of infection
      - treatment_recommendation: Recommended treatments
    - Entity counts
    - Metadata
    
    **Week 4 - Saugata Malakar**
    """
    try:
        logger.info(f"Processing NLP extraction for note (length: {len(request.note_text)})")
        
        # Extract entities
        result = nlp.process_note(request.note_text)
        
        # Generate note ID
        note_id = str(uuid.uuid4())
        
        # TODO: Store in database
        # if db:
        #     db_note = ClinicalNote(
        #         note_id=uuid.UUID(note_id),
        #         patient_id=uuid.UUID(request.patient_id) if request.patient_id else None,
        #         session_id=uuid.UUID(request.session_id) if request.session_id else None,
        #         doctor_id=uuid.UUID(request.doctor_id) if request.doctor_id else None,
        #         original_text=request.note_text,
        #         wound_locations=result["extracted_entities"]["wound_location"],
        #         infection_signs=result["extracted_entities"]["infection_sign"],
        #         treatment_recommendations=result["extracted_entities"]["treatment_recommendation"],
        #         extracted_at=datetime.utcnow(),
        #         nlp_model_version="en_core_web_sm"
        #     )
        #     db.add(db_note)
        #     db.commit()
        
        # Build response
        response = NLPExtractResponse(
            note_id=note_id,
            patient_id=request.patient_id,
            session_id=request.session_id,
            doctor_id=request.doctor_id,
            original_text=request.note_text,
            wound_locations=result["extracted_entities"]["wound_location"],
            infection_signs=result["extracted_entities"]["infection_sign"],
            treatment_recommendations=result["extracted_entities"]["treatment_recommendation"],
            entity_count={
                "wound_locations": len(result["extracted_entities"]["wound_location"]),
                "infection_signs": len(result["extracted_entities"]["infection_sign"]),
                "treatment_recommendations": len(result["extracted_entities"]["treatment_recommendation"])
            },
            extracted_at=result["timestamp"]
        )
        
        logger.info(f"✓ NLP extraction complete: {note_id}")
        logger.info(f"  - Wound locations: {len(response.wound_locations)}")
        logger.info(f"  - Infection signs: {len(response.infection_signs)}")
        logger.info(f"  - Treatment recommendations: {len(response.treatment_recommendations)}")
        
        return response
        
    except Exception as e:
        logger.error(f"NLP extraction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")


@router.post("/extract-batch", response_model=BatchNLPResponse)
async def extract_batch(
    request: BatchNLPRequest,
    nlp: ClinicalNLPPipeline = Depends(get_nlp_pipeline),
    db: Session = Depends(get_db)
):
    """
    Batch NLP extraction from multiple notes (up to 50).
    
    **Input:**
    - notes: List of clinical notes with optional metadata
    
    **Output:**
    - total_notes: Number of notes processed
    - successful: Number of successful extractions
    - failed: Number of failed extractions
    - results: List of extraction results
    
    **Week 4 - Saugata Malakar**
    """
    try:
        logger.info(f"Processing batch NLP extraction for {len(request.notes)} notes")
        
        results = []
        successful = 0
        failed = 0
        
        for note_req in request.notes:
            try:
                # Extract entities for each note
                result = nlp.process_note(note_req.note_text)
                note_id = str(uuid.uuid4())
                
                response = NLPExtractResponse(
                    note_id=note_id,
                    patient_id=note_req.patient_id,
                    session_id=note_req.session_id,
                    doctor_id=note_req.doctor_id,
                    original_text=note_req.note_text,
                    wound_locations=result["extracted_entities"]["wound_location"],
                    infection_signs=result["extracted_entities"]["infection_sign"],
                    treatment_recommendations=result["extracted_entities"]["treatment_recommendation"],
                    entity_count={
                        "wound_locations": len(result["extracted_entities"]["wound_location"]),
                        "infection_signs": len(result["extracted_entities"]["infection_sign"]),
                        "treatment_recommendations": len(result["extracted_entities"]["treatment_recommendation"])
                    },
                    extracted_at=result["timestamp"]
                )
                
                results.append(response)
                successful += 1
                
            except Exception as e:
                logger.error(f"Failed to process note: {e}")
                failed += 1
        
        logger.info(f"✓ Batch NLP extraction complete: {successful} successful, {failed} failed")
        
        return BatchNLPResponse(
            total_notes=len(request.notes),
            successful=successful,
            failed=failed,
            results=results
        )
        
    except Exception as e:
        logger.error(f"Batch NLP extraction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Batch extraction failed: {str(e)}")


@router.get("/note/{note_id}")
async def get_note(
    note_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve stored clinical note with NLP output by ID.
    
    **Input:**
    - note_id: UUID of stored note
    
    **Output:**
    - Complete note with extracted entities
    
    **Week 4 - Saugata Malakar**
    """
    # TODO: Implement database retrieval
    # For now, return not implemented
    raise HTTPException(
        status_code=501,
        detail="Note retrieval not yet implemented. Database integration pending."
    )


@router.get("/health")
async def health_check(nlp: ClinicalNLPPipeline = Depends(get_nlp_pipeline)):
    """
    Check if Clinical NLP API is ready.
    
    **Output:**
    - status: "ready"
    - model_loaded: boolean
    - model_name: spaCy model name
    - pattern_count: Number of custom entity patterns
    """
    return {
        "status": "ready",
        "model_loaded": nlp.nlp is not None,
        "model_name": "en_core_web_sm",
        "pattern_count": len(nlp.nlp.get_pipe("entity_ruler").patterns) if "entity_ruler" in nlp.nlp.pipe_names else 0,
        "message": "Clinical NLP API is operational"
    }


@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """
    Get statistics about stored clinical notes.
    
    **Output:**
    - total_notes: Total notes processed
    - notes_with_locations: Notes with wound locations
    - notes_with_infections: Notes with infection signs
    - notes_with_treatments: Notes with treatment recommendations
    
    **Week 4 - Saugata Malakar**
    """
    # TODO: Implement database statistics
    # For now, return not implemented
    raise HTTPException(
        status_code=501,
        detail="Statistics not yet implemented. Database integration pending."
    )
