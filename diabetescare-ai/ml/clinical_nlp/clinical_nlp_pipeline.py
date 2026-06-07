"""
Clinical NLP Pipeline using spaCy
Week 4 - Saugata Malakar

Extracts structured entities from free-text doctor consultation notes:
- wound_location
- infection_sign
- treatment_recommendation

Uses custom entity ruler with medical terminology patterns.
"""

import spacy
from spacy.pipeline import EntityRuler
from spacy.tokens import Doc, Span
from typing import Dict, List, Optional, Any
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Custom entity patterns for diabetic wound notes
WOUND_LOCATION_PATTERNS = [
    # Specific anatomical locations
    {"label": "WOUND_LOCATION", "pattern": [{"LOWER": "left"}, {"LOWER": "foot"}]},
    {"label": "WOUND_LOCATION", "pattern": [{"LOWER": "right"}, {"LOWER": "foot"}]},
    {"label": "WOUND_LOCATION", "pattern": [{"LOWER": "left"}, {"LOWER": "toe"}]},
    {"label": "WOUND_LOCATION", "pattern": [{"LOWER": "right"}, {"LOWER": "toe"}]},
    {"label": "WOUND_LOCATION", "pattern": [{"LOWER": "left"}, {"LOWER": "heel"}]},
    {"label": "WOUND_LOCATION", "pattern": [{"LOWER": "right"}, {"LOWER": "heel"}]},
    {"label": "WOUND_LOCATION", "pattern": [{"LOWER": "plantar"}, {"LOWER": "surface"}]},
    {"label": "WOUND_LOCATION", "pattern": [{"LOWER": "dorsal"}, {"LOWER": "surface"}]},
    {"label": "WOUND_LOCATION", "pattern": [{"LOWER": "medial"}, {"LOWER": "malleolus"}]},
    {"label": "WOUND_LOCATION", "pattern": [{"LOWER": "lateral"}, {"LOWER": "malleolus"}]},
    
    # Toes
    {"label": "WOUND_LOCATION", "pattern": [{"LOWER": "first"}, {"LOWER": "toe"}]},
    {"label": "WOUND_LOCATION", "pattern": [{"LOWER": "second"}, {"LOWER": "toe"}]},
    {"label": "WOUND_LOCATION", "pattern": [{"LOWER": "third"}, {"LOWER": "toe"}]},
    {"label": "WOUND_LOCATION", "pattern": [{"LOWER": "fourth"}, {"LOWER": "toe"}]},
    {"label": "WOUND_LOCATION", "pattern": [{"LOWER": "fifth"}, {"LOWER": "toe"}]},
    {"label": "WOUND_LOCATION", "pattern": [{"LOWER": "great"}, {"LOWER": "toe"}]},
    {"label": "WOUND_LOCATION", "pattern": [{"LOWER": "big"}, {"LOWER": "toe"}]},
    
    # Regions
    {"label": "WOUND_LOCATION", "pattern": [{"LOWER": "forefoot"}]},
    {"label": "WOUND_LOCATION", "pattern": [{"LOWER": "midfoot"}]},
    {"label": "WOUND_LOCATION", "pattern": [{"LOWER": "hindfoot"}]},
    {"label": "WOUND_LOCATION", "pattern": [{"LOWER": "ankle"}]},
    {"label": "WOUND_LOCATION", "pattern": [{"LOWER": "heel"}]},
    {"label": "WOUND_LOCATION", "pattern": [{"LOWER": "sole"}]},
    {"label": "WOUND_LOCATION", "pattern": [{"LOWER": "instep"}]},
    
    # With side indicators
    {"label": "WOUND_LOCATION", "pattern": [{"LOWER": "left"}, {"LOWER": "lateral"}, {"LOWER": "foot"}]},
    {"label": "WOUND_LOCATION", "pattern": [{"LOWER": "right"}, {"LOWER": "medial"}, {"LOWER": "foot"}]},
]


INFECTION_SIGN_PATTERNS = [
    # Direct infection terms
    {"label": "INFECTION_SIGN", "pattern": [{"LOWER": "cellulitis"}]},
    {"label": "INFECTION_SIGN", "pattern": [{"LOWER": "erythema"}]},
    {"label": "INFECTION_SIGN", "pattern": [{"LOWER": "purulent"}, {"LOWER": "discharge"}]},
    {"label": "INFECTION_SIGN", "pattern": [{"LOWER": "pus"}]},
    {"label": "INFECTION_SIGN", "pattern": [{"LOWER": "abscess"}]},
    {"label": "INFECTION_SIGN", "pattern": [{"LOWER": "necrosis"}]},
    {"label": "INFECTION_SIGN", "pattern": [{"LOWER": "gangrene"}]},
    {"label": "INFECTION_SIGN", "pattern": [{"LOWER": "osteomyelitis"}]},
    
    # Descriptive signs
    {"label": "INFECTION_SIGN", "pattern": [{"LOWER": "foul"}, {"LOWER": "smelling"}]},
    {"label": "INFECTION_SIGN", "pattern": [{"LOWER": "foul"}, {"LOWER": "odor"}]},
    {"label": "INFECTION_SIGN", "pattern": [{"LOWER": "malodorous"}]},
    {"label": "INFECTION_SIGN", "pattern": [{"LOWER": "spreading"}, {"LOWER": "redness"}]},
    {"label": "INFECTION_SIGN", "pattern": [{"LOWER": "warmth"}]},
    {"label": "INFECTION_SIGN", "pattern": [{"LOWER": "hot"}, {"LOWER": "to"}, {"LOWER": "touch"}]},
    {"label": "INFECTION_SIGN", "pattern": [{"LOWER": "fluctuant"}]},
    {"label": "INFECTION_SIGN", "pattern": [{"LOWER": "indurated"}]},
    
    # Systemic signs
    {"label": "INFECTION_SIGN", "pattern": [{"LOWER": "fever"}]},
    {"label": "INFECTION_SIGN", "pattern": [{"LOWER": "elevated"}, {"LOWER": "wbc"}]},
    {"label": "INFECTION_SIGN", "pattern": [{"LOWER": "leukocytosis"}]},
    {"label": "INFECTION_SIGN", "pattern": [{"LOWER": "sepsis"}]},
    
    # Visual signs
    {"label": "INFECTION_SIGN", "pattern": [{"LOWER": "eschar"}]},
    {"label": "INFECTION_SIGN", "pattern": [{"LOWER": "black"}, {"LOWER": "tissue"}]},
    {"label": "INFECTION_SIGN", "pattern": [{"LOWER": "necrotic"}, {"LOWER": "tissue"}]},
    {"label": "INFECTION_SIGN", "pattern": [{"LOWER": "slough"}]},
]


TREATMENT_RECOMMENDATION_PATTERNS = [
    # Antibiotics
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "start"}, {"LOWER": "antibiotics"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "continue"}, {"LOWER": "antibiotics"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "iv"}, {"LOWER": "antibiotics"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "oral"}, {"LOWER": "antibiotics"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "broad"}, {"LOWER": "spectrum"}, {"LOWER": "antibiotics"}]},
    
    # Debridement
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "debridement"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "sharp"}, {"LOWER": "debridement"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "surgical"}, {"LOWER": "debridement"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "debride"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "remove"}, {"LOWER": "necrotic"}, {"LOWER": "tissue"}]},
    
    # Wound care
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "wound"}, {"LOWER": "dressing"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "daily"}, {"LOWER": "dressing"}, {"LOWER": "change"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "hydrogel"}, {"LOWER": "dressing"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "foam"}, {"LOWER": "dressing"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "silver"}, {"LOWER": "dressing"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "negative"}, {"LOWER": "pressure"}, {"LOWER": "therapy"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "vac"}, {"LOWER": "therapy"}]},
    
    # Offloading
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "offloading"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "total"}, {"LOWER": "contact"}, {"LOWER": "cast"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "cast"}, {"LOWER": "boot"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "wheelchair"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "non"}, {"LOWER": "weight"}, {"LOWER": "bearing"}]},
    
    # Glycemic control
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "optimize"}, {"LOWER": "glycemic"}, {"LOWER": "control"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "insulin"}, {"LOWER": "adjustment"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "tighten"}, {"LOWER": "glucose"}, {"LOWER": "control"}]},
    
    # Referrals
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "refer"}, {"LOWER": "to"}, {"LOWER": "vascular"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "vascular"}, {"LOWER": "surgery"}, {"LOWER": "consult"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "podiatry"}, {"LOWER": "referral"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "infectious"}, {"LOWER": "disease"}, {"LOWER": "consult"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "admit"}, {"LOWER": "to"}, {"LOWER": "hospital"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "hospitalization"}]},
    
    # Imaging
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "x-ray"}, {"LOWER": "foot"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "mri"}, {"LOWER": "scan"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "bone"}, {"LOWER": "scan"}]},
    
    # Amputation
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "amputation"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "toe"}, {"LOWER": "amputation"}]},
    {"label": "TREATMENT_REC", "pattern": [{"LOWER": "below"}, {"LOWER": "knee"}, {"LOWER": "amputation"}]},
]


class ClinicalNLPPipeline:
    """
    spaCy-based NLP pipeline for clinical notes.
    
    Extracts:
    - wound_location: Where the wound is located
    - infection_sign: Signs of infection
    - treatment_recommendation: Recommended treatments
    """
    
    def __init__(self, model_name: str = "en_core_web_sm"):
        """
        Initialize spaCy pipeline with custom entity ruler.
        
        Args:
            model_name: spaCy model to use (default: en_core_web_sm)
        """
        try:
            self.nlp = spacy.load(model_name)
            logger.info(f"✓ Loaded spaCy model: {model_name}")
        except OSError:
            logger.warning(f"Model {model_name} not found. Downloading...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", model_name])
            self.nlp = spacy.load(model_name)
        
        # Add custom entity ruler
        if "entity_ruler" not in self.nlp.pipe_names:
            ruler = self.nlp.add_pipe("entity_ruler", before="ner")
            
            # Add all patterns
            ruler.add_patterns(WOUND_LOCATION_PATTERNS)
            ruler.add_patterns(INFECTION_SIGN_PATTERNS)
            ruler.add_patterns(TREATMENT_RECOMMENDATION_PATTERNS)
            
            logger.info(f"✓ Added custom entity ruler with {len(WOUND_LOCATION_PATTERNS) + len(INFECTION_SIGN_PATTERNS) + len(TREATMENT_RECOMMENDATION_PATTERNS)} patterns")
        
        self.nlp.max_length = 2000000  # Allow longer documents
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract structured entities from clinical notes.
        
        Args:
            text: Free-text clinical notes
        
        Returns:
            Dictionary with extracted entities
        """
        doc = self.nlp(text)
        
        # Organize entities by type
        entities = {
            "wound_location": [],
            "infection_sign": [],
            "treatment_recommendation": []
        }
        
        for ent in doc.ents:
            if ent.label_ == "WOUND_LOCATION":
                if ent.text not in entities["wound_location"]:
                    entities["wound_location"].append(ent.text)
            
            elif ent.label_ == "INFECTION_SIGN":
                if ent.text not in entities["infection_sign"]:
                    entities["infection_sign"].append(ent.text)
            
            elif ent.label_ == "TREATMENT_REC":
                if ent.text not in entities["treatment_recommendation"]:
                    entities["treatment_recommendation"].append(ent.text)
        
        return entities
    
    def process_note(self, note_text: str, note_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a single clinical note.
        
        Args:
            note_text: Clinical note text
            note_id: Optional note identifier
        
        Returns:
            Structured output with original text and extracted entities
        """
        entities = self.extract_entities(note_text)
        
        return {
            "note_id": note_id or f"note_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.utcnow().isoformat(),
            "original_text": note_text,
            "extracted_entities": entities,
            "entity_count": {
                "wound_locations": len(entities["wound_location"]),
                "infection_signs": len(entities["infection_sign"]),
                "treatment_recommendations": len(entities["treatment_recommendation"])
            }
        }
    
    def process_batch(self, notes: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Process multiple clinical notes in batch.
        
        Args:
            notes: List of dicts with 'text' and optional 'note_id'
        
        Returns:
            List of structured outputs
        """
        results = []
        
        for note in notes:
            result = self.process_note(
                note_text=note["text"],
                note_id=note.get("note_id")
            )
            results.append(result)
        
        return results


def extract_from_notes(notes_text: str) -> Dict[str, List[str]]:
    """
    Convenience function to extract entities from notes.
    
    Args:
        notes_text: Clinical notes text
    
    Returns:
        Extracted entities
    """
    pipeline = ClinicalNLPPipeline()
    return pipeline.extract_entities(notes_text)


if __name__ == "__main__":
    # Quick test
    pipeline = ClinicalNLPPipeline()
    
    test_note = """
    Patient presents with ulcer on left foot, plantar surface. 
    Signs of cellulitis with purulent discharge and foul odor noted.
    Erythema extending 3cm beyond wound margins. Patient is febrile.
    
    Recommendations:
    - Start IV antibiotics immediately
    - Surgical debridement of necrotic tissue
    - Daily dressing changes with silver foam dressing
    - Offloading with cast boot
    - Refer to vascular surgery for assessment
    - X-ray foot to rule out osteomyelitis
    """
    
    result = pipeline.process_note(test_note, "TEST_001")
    print(json.dumps(result, indent=2))
