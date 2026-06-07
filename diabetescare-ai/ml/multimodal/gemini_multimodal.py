"""
Multimodal Gemini 1.5 Pro Vision Integration
Week 4 - Saugata Malakar

Combines wound photograph + clinical data (HbA1c, diabetes duration, BP) 
for richer severity assessment.

Returns structured JSON with enhanced clinical insights.
"""

import os
import json
import base64
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
import logging
from pathlib import Path
from PIL import Image
import io

# Google Gemini imports
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logging.warning("google-generativeai not installed. Install: pip install google-generativeai")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class MultimodalAnalysisRequest:
    """Request for multimodal wound analysis"""
    image: Image.Image
    hba1c: float  # HbA1c level (%)
    diabetes_duration: int  # Years with diabetes
    systolic_bp: int  # Systolic blood pressure (mmHg)
    diastolic_bp: int  # Diastolic blood pressure (mmHg)
    patient_id: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None


@dataclass
class MultimodalAnalysisResponse:
    """Structured response from multimodal analysis"""
    severity_grade: int  # 0-5 Wagner grade
    severity_label: str
    confidence: float  # 0-1
    tissue_assessment: str
    infection_risk: str  # low/moderate/high/critical
    healing_prognosis: str  # excellent/good/fair/poor/very_poor
    clinical_insights: List[str]
    risk_factors: List[str]
    immediate_actions: List[str]
    follow_up_days: int
    specialist_referral: bool
    raw_response: str
    timestamp: str


class GeminiMultimodalAPI:
    """
    Multimodal AI using Gemini 1.5 Pro Vision
    
    Combines:
    - Wound photograph (visual analysis)
    - HbA1c (glycemic control indicator)
    - Diabetes duration (chronicity risk)
    - Blood pressure (vascular health)
    
    Returns: Structured JSON with comprehensive assessment
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini multimodal API.
        
        Args:
            api_key: Google AI API key (or use GEMINI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        
        if not GEMINI_AVAILABLE:
            logger.error("Gemini not available. Install: pip install google-generativeai")
            self.model = None
            return
        
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not set. Using mock mode.")
            self.model = None
            return
        
        try:
            genai.configure(api_key=self.api_key)
            
            # Use Gemini 1.5 Pro Vision
            self.model = genai.GenerativeModel('gemini-1.5-pro')
            
            logger.info("✓ Gemini 1.5 Pro Vision initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {e}")
            self.model = None
    
    def _build_prompt(self, request: MultimodalAnalysisRequest) -> str:
        """
        Build comprehensive multimodal prompt.
        
        Combines clinical context with image analysis request.
        """
        prompt = f"""You are an expert diabetologist and wound care specialist. Analyze this diabetic foot wound photograph along with the patient's clinical data.

**PATIENT CLINICAL DATA:**
- HbA1c: {request.hba1c}% (target <7.0% for diabetics)
- Diabetes Duration: {request.diabetes_duration} years
- Blood Pressure: {request.systolic_bp}/{request.diastolic_bp} mmHg
- Age: {request.age if request.age else 'Unknown'}
- Gender: {request.gender if request.gender else 'Unknown'}

**ANALYSIS REQUIRED:**

1. **Wound Severity**: Classify using Wagner grading (0-5):
   - Grade 0: Intact skin, no open lesion
   - Grade 1: Superficial ulcer
   - Grade 2: Deep ulcer to tendon, bone, or joint
   - Grade 3: Deep ulcer with abscess or osteomyelitis
   - Grade 4: Gangrene of forefoot
   - Grade 5: Gangrene of entire foot

2. **Tissue Assessment**: Describe dominant tissue types visible:
   - Granulation (healthy pink/red)
   - Slough (yellow fibrinous)
   - Eschar/Necrotic (black/brown)
   - Signs of infection (cellulitis, pus, inflammation)

3. **Infection Risk**: Based on visual signs + clinical data:
   - Low: Clean wound, well-controlled diabetes (HbA1c <7%)
   - Moderate: Some inflammation, moderate control (HbA1c 7-9%)
   - High: Clear infection signs, poor control (HbA1c >9%)
   - Critical: Extensive infection, multi-organ involvement

4. **Healing Prognosis**: Consider:
   - Wound characteristics
   - Glycemic control (HbA1c)
   - Disease duration
   - Vascular health (BP)
   
   Rate as: excellent/good/fair/poor/very_poor

5. **Clinical Insights**: List 3-5 key observations about:
   - Wound progression stage
   - Impact of elevated HbA1c
   - Vascular complications evident
   - Neuropathy indicators

6. **Risk Factors**: Identify modifiable and non-modifiable risks

7. **Immediate Actions**: 3-5 urgent clinical recommendations

8. **Follow-up**: Recommend days until next assessment (1-30 days)

9. **Specialist Referral**: Does this case need:
   - Vascular surgeon
   - Infectious disease specialist
   - Podiatrist
   - Hospital admission

**OUTPUT FORMAT (JSON):**
Return ONLY valid JSON with this exact structure:

{{
  "severity_grade": <int 0-5>,
  "severity_label": "<string: e.g., 'Grade 2: Deep ulcer'>",
  "confidence": <float 0-1>,
  "tissue_assessment": "<string: describe tissue types>",
  "infection_risk": "<string: low/moderate/high/critical>",
  "healing_prognosis": "<string: excellent/good/fair/poor/very_poor>",
  "clinical_insights": [
    "<insight 1>",
    "<insight 2>",
    "<insight 3>"
  ],
  "risk_factors": [
    "<risk 1>",
    "<risk 2>"
  ],
  "immediate_actions": [
    "<action 1>",
    "<action 2>",
    "<action 3>"
  ],
  "follow_up_days": <int 1-30>,
  "specialist_referral": <boolean>
}}

**IMPORTANT**: 
- Return ONLY the JSON, no other text
- Consider the HbA1c level heavily (>9% = poor control = worse prognosis)
- Long diabetes duration (>10 years) = higher complications risk
- High BP (>140/90) = vascular complications likely
"""
        return prompt
    
    def _extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """
        Extract JSON from Gemini response.
        
        Handles cases where response includes markdown code blocks.
        """
        # Try to find JSON in markdown code blocks
        if "```json" in response_text:
            start = response_text.find("```json") + 7
            end = response_text.find("```", start)
            json_str = response_text[start:end].strip()
        elif "```" in response_text:
            start = response_text.find("```") + 3
            end = response_text.find("```", start)
            json_str = response_text[start:end].strip()
        else:
            json_str = response_text.strip()
        
        # Parse JSON
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
            logger.error(f"Response text: {json_str[:500]}")
            raise
    
    async def analyze_multimodal(
        self, 
        request: MultimodalAnalysisRequest
    ) -> MultimodalAnalysisResponse:
        """
        Perform multimodal analysis combining image + clinical data.
        
        Args:
            request: MultimodalAnalysisRequest with image and clinical data
        
        Returns:
            MultimodalAnalysisResponse with structured assessment
        """
        if self.model is None:
            # Return mock response if Gemini not available
            logger.warning("Gemini not available, returning mock response")
            return self._mock_response(request)
        
        try:
            # Build prompt
            prompt = self._build_prompt(request)
            
            # Generate response with image + text
            response = self.model.generate_content([
                prompt,
                request.image
            ])
            
            # Extract JSON from response
            response_text = response.text
            result_json = self._extract_json_from_response(response_text)
            
            # Build response
            return MultimodalAnalysisResponse(
                severity_grade=result_json["severity_grade"],
                severity_label=result_json["severity_label"],
                confidence=result_json["confidence"],
                tissue_assessment=result_json["tissue_assessment"],
                infection_risk=result_json["infection_risk"],
                healing_prognosis=result_json["healing_prognosis"],
                clinical_insights=result_json["clinical_insights"],
                risk_factors=result_json["risk_factors"],
                immediate_actions=result_json["immediate_actions"],
                follow_up_days=result_json["follow_up_days"],
                specialist_referral=result_json["specialist_referral"],
                raw_response=response_text,
                timestamp=datetime.utcnow().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Multimodal analysis failed: {e}")
            raise
    
    def _mock_response(self, request: MultimodalAnalysisRequest) -> MultimodalAnalysisResponse:
        """Generate mock response for testing without Gemini API"""
        
        # Simple risk assessment based on clinical data
        high_hba1c = request.hba1c > 9.0
        long_duration = request.diabetes_duration > 10
        high_bp = request.systolic_bp > 140
        
        risk_count = sum([high_hba1c, long_duration, high_bp])
        
        if risk_count >= 2:
            severity = 3
            infection_risk = "high"
            prognosis = "poor"
            follow_up = 3
            referral = True
        elif risk_count == 1:
            severity = 2
            infection_risk = "moderate"
            prognosis = "fair"
            follow_up = 7
            referral = False
        else:
            severity = 1
            infection_risk = "low"
            prognosis = "good"
            follow_up = 14
            referral = False
        
        return MultimodalAnalysisResponse(
            severity_grade=severity,
            severity_label=f"Grade {severity} (Mock Assessment)",
            confidence=0.75,
            tissue_assessment="Mixed granulation and slough tissue observed (mock)",
            infection_risk=infection_risk,
            healing_prognosis=prognosis,
            clinical_insights=[
                f"HbA1c of {request.hba1c}% indicates {'poor' if high_hba1c else 'adequate'} glycemic control",
                f"Diabetes duration of {request.diabetes_duration} years {'increases' if long_duration else 'presents moderate'} complication risk",
                f"Blood pressure {request.systolic_bp}/{request.diastolic_bp} suggests {'impaired' if high_bp else 'adequate'} vascular health"
            ],
            risk_factors=[
                "Elevated HbA1c" if high_hba1c else "Diabetes duration",
                "High blood pressure" if high_bp else "Peripheral neuropathy risk"
            ],
            immediate_actions=[
                "Improve glycemic control" if high_hba1c else "Continue current management",
                "Wound debridement if slough present",
                "Monitor for infection signs"
            ],
            follow_up_days=follow_up,
            specialist_referral=referral,
            raw_response="Mock response - Gemini API not configured",
            timestamp=datetime.utcnow().isoformat()
        )
    
    def analyze_batch(
        self, 
        requests: List[MultimodalAnalysisRequest]
    ) -> List[MultimodalAnalysisResponse]:
        """
        Analyze multiple cases in batch.
        
        Args:
            requests: List of MultimodalAnalysisRequest
        
        Returns:
            List of MultimodalAnalysisResponse
        """
        results = []
        
        for idx, request in enumerate(requests):
            logger.info(f"Processing case {idx+1}/{len(requests)}")
            
            try:
                # Note: In real async, we'd use asyncio.gather
                # For now, process sequentially
                import asyncio
                result = asyncio.run(self.analyze_multimodal(request))
                results.append(result)
                
            except Exception as e:
                logger.error(f"Failed to analyze case {idx+1}: {e}")
                results.append(None)
        
        return results


# Export for convenience
def create_gemini_api(api_key: Optional[str] = None) -> GeminiMultimodalAPI:
    """Factory function to create Gemini API instance"""
    return GeminiMultimodalAPI(api_key=api_key)


if __name__ == "__main__":
    # Quick test
    print("Gemini Multimodal API")
    print(f"Gemini available: {GEMINI_AVAILABLE}")
    
    api = create_gemini_api()
    print(f"Model initialized: {api.model is not None}")
