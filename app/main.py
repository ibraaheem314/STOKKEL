"""
API FastAPI pour Stokkel MVP
Exposé tous les endpoints pour la prévision et l'optimisation des stocks
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, status, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, Dict, List
import pandas as pd
import logging
from datetime import datetime
import tempfile
import os

from .config import settings
from .schemas import (
    ForecastResponse,
    RecommendationResponse,
    BatchRecommendationRequest,
    BatchRecommendationResponse,
    UploadResponse,
    HealthResponse,
    ProductInfo,
    ErrorResponse
)
from .data_manager import data_manager
from .forecasting import forecast_engine
from .optimization import stock_optimizer
from .auth import auth_router, get_current_active_user, require_admin
from .exceptions import (
    InsufficientDataError, 
    InvalidProductError, 
    DataValidationError,
    ForecastError,
    OptimizationError,
    handle_stokkel_exception
)
from fastapi.responses import JSONResponse
from .validators import DataValidator
from .logging_config import setup_logging, get_logger, log_api_request, log_forecast_request, log_forecast_result
from .monitoring import metrics_collector, start_metrics_server

# Configuration du logging structuré
setup_logging()
logger = get_logger("stokkel.main")

# Démarrage du serveur de métriques
start_metrics_server(port=9090)

# Création de l'application FastAPI
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion du router d'authentification
app.include_router(auth_router)

# Gestionnaires d'exceptions globales
@app.exception_handler(InsufficientDataError)
async def insufficient_data_handler(request, exc):
    http_exc = handle_stokkel_exception(exc)
    return JSONResponse(
        status_code=http_exc.status_code,
        content=http_exc.detail
    )

@app.exception_handler(InvalidProductError)
async def invalid_product_handler(request, exc):
    http_exc = handle_stokkel_exception(exc)
    return JSONResponse(
        status_code=http_exc.status_code,
        content=http_exc.detail
    )

@app.exception_handler(DataValidationError)
async def data_validation_handler(request, exc):
    http_exc = handle_stokkel_exception(exc)
    return JSONResponse(
        status_code=http_exc.status_code,
        content=http_exc.detail
    )

@app.exception_handler(ForecastError)
async def forecast_error_handler(request, exc):
    http_exc = handle_stokkel_exception(exc)
    return JSONResponse(
        status_code=http_exc.status_code,
        content=http_exc.detail
    )

@app.exception_handler(OptimizationError)
async def optimization_error_handler(request, exc):
    http_exc = handle_stokkel_exception(exc)
    return JSONResponse(
        status_code=http_exc.status_code,
        content=http_exc.detail
    )


# Dépendance pour l'authentification simple
async def verify_token(authorization: Optional[str] = Header(None)):
    """Vérifie le token d'authentification"""
    
    # Si auth désactivée, laisser passer
    if not settings.auth_enabled:
        logger.info("⚠️ Auth désactivée (mode dev)")
        return "dev_mode"
    
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token d'authentification manquant"
        )
    
    # Extraction du token
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Format d'authentification invalide. Utilisez: Bearer <token>"
        )
    
    # Vérification du token (simple pour le MVP)
    if token != settings.api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token d'authentification invalide"
        )
    
    return token


# Gestionnaire d'erreurs global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Gestionnaire global des exceptions"""
    logger.error(f"Erreur non gérée: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Erreur interne du serveur",
            detail=str(exc)
        ).dict()
    )


# ==================== ENDPOINTS ====================

@app.get("/", tags=["Info"])
async def root():
    """Endpoint racine avec informations de l'API"""
    return {
        "name": settings.api_title,
        "version": settings.api_version,
        "description": settings.api_description,
        "status": "running",
        "documentation": "/docs",
        "endpoints": {
            "health": "/health",
            "upload": "/upload_sales",
            "forecast": "/forecast/{product_id}",
            "recommendation": "/recommendation/{product_id}",
            "products": "/products"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Info"])
async def health_check():
    """
    Vérification de l'état de santé de l'API
    """
    has_data = data_manager.has_data()
    
    health_status = "healthy" if has_data else "degraded"
    
    details = {
        "data_loaded": has_data,
        "products_count": len(data_manager.products_cache) if has_data else 0,
        "models_cached": len(forecast_engine.trained_models)
    }
    
    return HealthResponse(
        status=health_status,
        version=settings.api_version,
        details=details
    )


@app.post("/upload_sales", response_model=UploadResponse, tags=["Data"])
async def upload_sales_data(
    file: UploadFile = File(...),
    current_user = Depends(get_current_active_user)
):
    """
    Upload des données historiques de ventes
    
    Le fichier CSV doit contenir les colonnes:
    - product_id: Identifiant du produit
    - date: Date de la vente (format YYYY-MM-DD)
    - quantity: Quantité vendue (nombre positif)
    """
    logger.info(f"Réception d'un fichier: {file.filename}")
    
    # Vérification du type de fichier
    if not file.filename.endswith(('.csv', '.xlsx')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Format de fichier non supporté. Utilisez CSV ou XLSX"
        )
    
    try:
        # Sauvegarde temporaire du fichier
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Chargement des données
        stats = data_manager.load_sales_data(temp_file_path)
        
        # Nettoyage du fichier temporaire
        os.unlink(temp_file_path)
        
        logger.info(f"Données chargées avec succès: {stats['products_count']} produits")
        
        return UploadResponse(**stats)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Erreur lors de l'upload: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du traitement du fichier: {str(e)}"
        )


@app.get("/products", response_model=Dict[str, List[ProductInfo]], tags=["Data"])
async def get_products(token: str = Depends(verify_token)):
    """
    Récupère la liste de tous les produits avec leurs métadonnées
    """
    if not data_manager.has_data():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucune donnée disponible. Veuillez d'abord uploader des données."
        )
    
    try:
        products = data_manager.get_all_products()
        return {"products": products}
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des produits: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get("/forecast/{product_id}", response_model=ForecastResponse, tags=["Forecasting"])
async def get_forecast(
    product_id: str,
    horizon_days: int = 30,
    current_user = Depends(get_current_active_user)
):
    """
    Génère une prévision probabiliste pour un produit
    
    Args:
        product_id: Identifiant du produit
        horizon_days: Nombre de jours à prévoir (1-365)
        current_user: Utilisateur authentifié
        
    Returns:
        ForecastResponse: Prévisions avec intervalles de confiance
    """
    # Validation des paramètres
    is_valid, error_msg = DataValidator.validate_forecast_request(product_id, horizon_days)
    if not is_valid:
        raise DataValidationError(error_msg)
    
    # Vérifier que le produit existe
    products = data_manager.get_products()
    if product_id not in products:
        raise InvalidProductError(product_id, products)
    logger.info(f"Demande de prévision pour {product_id} sur {horizon_days} jours")
    log_forecast_request(product_id, horizon_days, current_user.username)
    
    # Validation des données
    if not data_manager.has_data():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucune donnée disponible. Veuillez d'abord uploader des données."
        )
    
    # Validation du produit
    is_valid, message = data_manager.validate_product(product_id)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation échouée pour {product_id}: {message}"
        )
    
    # Validation de l'horizon
    if horizon_days < 1 or horizon_days > 90:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'horizon de prévision doit être entre 1 et 90 jours"
        )
    
    try:
        # Préparation des données
        historical_data = data_manager.prepare_forecast_data(product_id)
        
        # Génération de la prévision
        forecast_points, metadata = forecast_engine.generate_forecast(
            product_id=product_id,
            historical_data=historical_data,
            horizon_days=horizon_days
        )
        
        # Construction de la réponse
        response = ForecastResponse(
            product_id=product_id,
            forecasts=forecast_points,
            metadata=metadata
        )
        
        logger.info(f"Prévision générée avec succès pour {product_id}")
        
        return response
        
    except Exception as e:
        logger.error(f"Erreur lors de la génération de prévision: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get("/recommendation/{product_id}", response_model=RecommendationResponse, tags=["Optimization"])
async def get_recommendation(
    product_id: str,
    current_stock: float = 0,
    lead_time_days: int = settings.default_lead_time,
    service_level_percent: int = settings.default_service_level,
    current_user = Depends(get_current_active_user)
):
    """
    Génère une recommandation d'approvisionnement pour un produit
    
    Args:
        product_id: Identifiant du produit
        current_stock: Stock actuel en unités (défaut: 0)
        lead_time_days: Délai de livraison fournisseur en jours (défaut: 7)
        service_level_percent: Niveau de service cible en % (défaut: 95)
        
    Returns:
        Recommandation avec quantité à commander, point de commande, stock de sécurité
    """
    logger.info(f"Demande de recommandation pour {product_id}")
    
    # Validation des données
    if not data_manager.has_data():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucune donnée disponible. Veuillez d'abord uploader des données."
        )
    
    # Validation des paramètres
    if current_stock < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le stock actuel ne peut pas être négatif"
        )
    
    if lead_time_days < 1 or lead_time_days > 90:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le délai de livraison doit être entre 1 et 90 jours"
        )
    
    if service_level_percent < 80 or service_level_percent > 99:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le niveau de service doit être entre 80% et 99%"
        )
    
    try:
        # Génération de la prévision (nécessaire pour la recommandation)
        historical_data = data_manager.prepare_forecast_data(product_id)
        forecast_points, _ = forecast_engine.generate_forecast(
            product_id=product_id,
            historical_data=historical_data,
            horizon_days=lead_time_days * 2  # Horizon = 2x lead time
        )
        
        # Conversion des forecast_points en DataFrame
        forecast_df = pd.DataFrame([fp.dict() for fp in forecast_points])
        
        # Génération de la recommandation
        recommendation = stock_optimizer.generate_recommendation(
            product_id=product_id,
            forecast_data=forecast_df,
            current_stock=current_stock,
            lead_time_days=lead_time_days,
            service_level_percent=service_level_percent
        )
        
        logger.info(f"Recommandation générée pour {product_id}: {recommendation.recommendation_action}")
        
        return recommendation
        
    except Exception as e:
        logger.error(f"Erreur lors de la génération de recommandation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.post("/batch_recommendations", response_model=BatchRecommendationResponse, tags=["Optimization"])
async def get_batch_recommendations(
    request: BatchRecommendationRequest,
    current_user = Depends(get_current_active_user)
):
    """
    Génère des recommandations pour tous les produits
    
    Args:
        request: Paramètres de la requête batch
        
    Returns:
        Liste de toutes les recommandations avec résumé
    """
    logger.info("Demande de recommandations batch")
    
    if not data_manager.has_data():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucune donnée disponible"
        )
    
    try:
        # Récupération de tous les produits
        products = data_manager.get_all_products()
        
        # Génération des prévisions pour chaque produit
        products_forecasts = {}
        for product_info in products:
            product_id = product_info['product_id']
            
            try:
                historical_data = data_manager.prepare_forecast_data(product_id)
                forecast_points, _ = forecast_engine.generate_forecast(
                    product_id=product_id,
                    historical_data=historical_data,
                    horizon_days=request.lead_time_days * 2
                )
                
                forecast_df = pd.DataFrame([fp.dict() for fp in forecast_points])
                products_forecasts[product_id] = forecast_df
                
            except Exception as e:
                logger.warning(f"Impossible de générer la prévision pour {product_id}: {str(e)}")
                continue
        
        # Génération des recommandations
        result = stock_optimizer.calculate_batch_recommendations(
            products_forecasts=products_forecasts,
            stock_levels=request.stock_levels,
            lead_time_days=request.lead_time_days,
            service_level_percent=request.service_level_percent
        )
        
        response = BatchRecommendationResponse(
            recommendations=result['recommendations'],
            summary=result['summary']
        )
        
        logger.info(f"Recommandations batch générées: {len(response.recommendations)} produits")
        
        return response
        
    except Exception as e:
        logger.error(f"Erreur lors des recommandations batch: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.delete("/cache/{product_id}", tags=["Admin"])
async def clear_model_cache(
    product_id: Optional[str] = None,
    current_user = Depends(get_current_active_user)
):
    """
    Nettoie le cache des modèles (utile pour forcer le réentraînement)
    
    Args:
        product_id: Si spécifié, nettoie uniquement ce produit, sinon tous
    """
    forecast_engine.clear_cache(product_id)
    
    message = f"Cache nettoyé pour {product_id}" if product_id else "Cache complet nettoyé"
    logger.info(message)
    
    return {"message": message}


# Démarrage de l'application
if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Démarrage de Stokkel API v{settings.api_version}")
    
    # Tentative de chargement des données sauvegardées
    data_manager.load_saved_data()
    
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        log_level=settings.log_level.lower()
    )