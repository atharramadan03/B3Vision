# Skema data Pydantic untuk REST API

from typing import Dict, List
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    # Respon status server (/health)
    status: str = Field(..., example="ok")
    model_loaded: bool = Field(..., example=True)
    model_version: str = Field(..., example="v2.0-mobilenetv2-12class")
    total_classes: int = Field(..., example=12)


class ClassProbability(BaseModel):
    # Probabilitas per kelas limbah
    class_id: str
    name: str
    full_name: str
    category: str
    confidence: float
    ratio: float


class PredictionResponse(BaseModel):
    # Respon inferensi prediksi (/api/v1/predict)
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
    model_version: str = "v2.0-mobilenetv2-12class"
    latency_ms: float
    probabilities: Dict[str, float]
    distribution: List[ClassProbability]
    description: str
    environmental_impact: str
    sop_actions: List[str]
    prohibitions: List[str]
