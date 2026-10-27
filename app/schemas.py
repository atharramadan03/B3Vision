"""
Definisi skema Pydantic untuk kontrak data REST API FastAPI.
"""

from typing import Dict, List
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Skema respon pengecekan status server dan model (/health)."""
    status: str = Field(..., example="ok")
    model_loaded: bool = Field(..., example=True)
    model_version: str = Field(..., example="v1.0-mobilenetv2")
    total_classes: int = Field(..., example=7)


class ClassProbability(BaseModel):
    """Skema data probabilitas untuk setiap kelas limbah."""
    class_id: str
    name: str
    full_name: str
    category: str
    confidence: float
    ratio: float


class PredictionResponse(BaseModel):
    """Skema respon lengkap inferensi klasifikasi limbah B3 (/api/v1/predict)."""
    status: str = "success"
    filename: str
    label: str
    class_name: str
    short_name: str
    category: str
    hazard_level: str
    score: float
    confidence: float
    is_confident: bool
    status_state: str
    model_version: str = "v1.0-mobilenetv2"
    latency_ms: float
    probabilities: Dict[str, float]
    distribution: List[ClassProbability]
    description: str
    environmental_impact: str
    sop_actions: List[str]
    prohibitions: List[str]
