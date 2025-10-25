"""
Configuration centrale pour Stokkel MVP
Version: 1.1.0 - Améliorée avec auth optionnelle et cache
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration de l'application"""
    
    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_title: str = "Stokkel API"
    api_version: str = "1.1.0"
    api_description: str = "API de prévision des ventes et optimisation des stocks pour PME"
    
    # Security
    auth_enabled: bool = True  # ⬅️ NOUVEAU: désactiver l'auth en dev
    api_token: str = "stokkel_mvp_token_2024"
    
    # Model Settings
    default_forecast_horizon: int = 30
    default_service_level: int = 95
    default_lead_time: int = 7
    default_current_stock: float = 0.0  # ⬅️ NOUVEAU
    min_data_points: int = 7
    max_forecast_horizon: int = 365  # ⬅️ NOUVEAU
    confidence_interval: float = 0.80
    
    # Forecasting Settings (Prophet)
    prophet_changepoint_prior_scale: float = 0.05
    prophet_seasonality_prior_scale: float = 10.0
    prophet_interval_width: float = 0.80
    
    # Data Storage
    data_dir: str = "./data"
    models_dir: str = "./models"
    metrics_dir: str = "./metrics"  # ⬅️ NOUVEAU
    
    # Cache
    redis_url: Optional[str] = None  # ⬅️ NOUVEAU: None = dict cache
    cache_ttl_seconds: int = 3600
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # ⬅️ NOUVEAU
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Instance globale des settings
settings = Settings()


# Création des répertoires nécessaires
for directory in [settings.data_dir, settings.models_dir, settings.metrics_dir]:
    os.makedirs(directory, exist_ok=True)