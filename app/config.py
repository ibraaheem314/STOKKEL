"""
Configuration centrale pour Stokkel MVP
Gère tous les paramètres de l'application
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration de l'application"""
    
    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_token: str = "stokkel_mvp_token_2024"
    api_title: str = "Stokkel API"
    api_version: str = "1.0.0"
    api_description: str = "API de prévision des ventes et optimisation des stocks pour PME"
    
    # Model Settings
    default_forecast_horizon: int = 30
    default_service_level: int = 95
    default_lead_time: int = 7
    min_data_points: int = 7
    confidence_interval: float = 0.80
    
    # Forecasting Settings
    prophet_changepoint_prior_scale: float = 0.05
    prophet_seasonality_prior_scale: float = 10.0
    prophet_interval_width: float = 0.80
    
    # Data Storage
    data_dir: str = "./data"
    models_dir: str = "./models"
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Instance globale des settings
settings = Settings()


# Création des répertoires nécessaires
os.makedirs(settings.data_dir, exist_ok=True)
os.makedirs(settings.models_dir, exist_ok=True)