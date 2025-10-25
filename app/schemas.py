"""
Schémas de données Pydantic pour Stokkel
Définit la structure des données échangées via l'API
"""

from typing import List, Dict, Optional, Literal
from datetime import date as Date, datetime
from pydantic import BaseModel, Field, field_validator


class SalesDataPoint(BaseModel):
    """Point de données de vente"""
    product_id: str = Field(..., description="Identifiant unique du produit")
    date: Date = Field(..., description="Date de la vente")
    quantity: float = Field(..., gt=0, description="Quantité vendue (doit être positive)")
    
    @field_validator('quantity')
    @classmethod
    def quantity_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('La quantité doit être positive')
        return v


class ForecastPoint(BaseModel):
    """Point de prévision de vente"""
    date: str = Field(..., description="Date de la prévision")
    p10: float = Field(..., description="Quantile 10% (pessimiste)")
    p50: float = Field(..., description="Quantile 50% (médiane)")
    p90: float = Field(..., description="Quantile 90% (optimiste)")


class ForecastResponse(BaseModel):
    """Réponse complète de prévision"""
    product_id: str
    forecasts: List[ForecastPoint]
    metadata: Dict = Field(default_factory=dict)
    generated_at: datetime = Field(default_factory=datetime.now)


class RecommendationRequest(BaseModel):
    """Paramètres pour la recommandation d'approvisionnement"""
    product_id: str
    current_stock: float = Field(..., ge=0, description="Stock actuel (unités)")
    lead_time_days: int = Field(..., gt=0, le=90, description="Délai de livraison (jours)")
    service_level_percent: int = Field(..., ge=80, le=99, description="Niveau de service cible (%)")


class RecommendationResponse(BaseModel):
    """Réponse de recommandation d'approvisionnement"""
    product_id: str
    recommendation_action: Literal["Commander", "Stock suffisant", "Surveiller"]
    quantity_to_order: float = Field(..., ge=0)
    reorder_point: float = Field(..., ge=0)
    dynamic_safety_stock: float = Field(..., ge=0)
    current_stock_status: str
    days_until_stockout: Optional[int] = None
    metadata: Dict = Field(default_factory=dict)
    generated_at: datetime = Field(default_factory=datetime.now)


class BatchRecommendationRequest(BaseModel):
    """Paramètres pour recommandations en batch"""
    lead_time_days: int = Field(default=7, gt=0, le=90)
    service_level_percent: int = Field(default=95, ge=80, le=99)
    stock_levels: Optional[Dict[str, float]] = Field(
        default=None,
        description="Dictionnaire product_id: current_stock"
    )


class BatchRecommendationResponse(BaseModel):
    """Réponse des recommandations en batch"""
    recommendations: List[RecommendationResponse]
    summary: Dict = Field(default_factory=dict)
    generated_at: datetime = Field(default_factory=datetime.now)


class ProductInfo(BaseModel):
    """Informations sur un produit"""
    product_id: str
    data_points: int
    date_range_start: Optional[Date] = None
    date_range_end: Optional[Date] = None
    average_daily_sales: Optional[float] = None
    total_sales: Optional[float] = None


class UploadResponse(BaseModel):
    """Réponse après upload de données"""
    message: str
    products_count: int
    total_records: int
    date_range: Dict[str, str]


class HealthResponse(BaseModel):
    """Réponse du health check"""
    status: Literal["healthy", "degraded", "unhealthy"]
    version: str
    timestamp: datetime = Field(default_factory=datetime.now)
    details: Optional[Dict] = None


class ErrorResponse(BaseModel):
    """Réponse d'erreur standardisée"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)