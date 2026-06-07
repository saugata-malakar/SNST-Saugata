"""
Multimodal AI Module
Week 4 - Saugata Malakar

Combines image + clinical data for richer severity assessment using Gemini 1.5 Pro Vision.
"""

from .gemini_multimodal import GeminiMultimodalAPI, MultimodalAnalysisRequest, MultimodalAnalysisResponse

__all__ = ["GeminiMultimodalAPI", "MultimodalAnalysisRequest", "MultimodalAnalysisResponse"]
